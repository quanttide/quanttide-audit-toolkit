import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from quanttide_audit import AuditReport

from .models import AuditIssues, AuditIssue, AuditMode, KnowledgeBaseStats


# ── render ──────────────────────────────────────────────────────────────────


def render_report(
    *,
    report: AuditReport,
    mode: AuditMode,
    stats: KnowledgeBaseStats,
    issues: AuditIssues,
    diff: Optional["AuditDiff"] = None,
    previous_timestamp: Optional[str] = None,
) -> None:
    _print_stats(stats)
    print("=" * 60)
    print("  检测结果")
    print("=" * 60)
    print()
    _print_diff(diff, previous_timestamp)
    _print_report_to_stdout(issues)


def _print_stats(stats: KnowledgeBaseStats) -> None:
    print("=" * 60)
    print("  知识库概览")
    print("=" * 60)
    print(f"\n  数据目录: {stats.data_dir}")
    print(f"  领域数量: {stats.domain_count}")
    print(f"  本体数量: {stats.ontology_count}")
    print(f"  实例数量: {stats.instance_count}")
    print()
    if stats.has_domains:
        print("  领域清单:")
        for domain in stats.domains:
            print(f"    {str(domain.id):<20} {domain.name:<12}")
        print()


def _print_diff(diff: Optional["AuditDiff"], previous_timestamp: Optional[str]) -> None:
    if not diff:
        return
    prev_time = (previous_timestamp or "未知")[:10]
    if diff.has_changes:
        parts = []
        if diff.fixed:
            parts.append(f"✅ 已修复 {len(diff.fixed)} 项")
        if diff.new:
            parts.append(f"🆕 新增 {len(diff.new)} 项")
        if diff.pending:
            parts.append(f"⏳ 待处理 {len(diff.pending)} 项")
        print(f"相比上次审计（{prev_time}）：{' / '.join(parts)}")
    else:
        print(f"✓ 与上次审计一致，无新增问题（{prev_time}）")
    print()


# ── repository ──────────────────────────────────────────────────────────────

JSON_FILE = "audit.json"


class ReportRepository:
    def __init__(self, state_home: Path):
        self._path = state_home / JSON_FILE

    def load_previous_state(self, mode: Optional[AuditMode] = None) -> Optional[tuple]:
        if not self._path.exists():
            return None
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            if mode and data.get("mode") != mode.value:
                return None
            issues = [
                AuditIssue(category=i["category"], group=i["group"], label=i["label"], action=i.get("action", ""))
                for i in data.get("issues", [])
            ]
            return (issues, data.get("timestamp", ""), AuditMode(data["mode"]))
        except Exception:
            return None

    def save_report(self, report: AuditReport, issues: AuditIssues) -> None:
        data = {
            "timestamp": datetime.now().isoformat(),
            "mode": issues.mode.value,
            "issues": [
                {"category": i.category, "group": i.group, "label": i.label, "action": i.action}
                for i in (issues.need_confirm + issues.auto_fixable + issues.suggestions)
            ],
        }
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ── rendering helpers ───────────────────────────────────────────────────────

DEFAULT_REPORT_TEMPLATE = {
    "sections_full": [
        ("need_confirm", "需要你确认的问题", "以下问题平台无法自动判断，需要你决定如何处理。"),
        ("auto_fixable", "平台发现的问题", "以下问题平台已识别，可通过自动修复处理。"),
    ],
    "sections_simple": [
        ("need_confirm", "建议关注", "以下问题可由平台自动修复，无需手动处理。"),
        ("auto_fixable", "平台发现的问题", "以下问题平台已识别，可通过自动修复处理。"),
    ],
    "clean_message": "✓ 未发现问题，知识库结构良好。",
    "summary_header": "  汇总",
    "tail_messages": {
        "simple": "当前为快速检查模式，运行 qtcloud-knowl audit --mode full 进行全面审计。",
        "need_confirm": "请先处理「需要你确认的问题」，其他问题可并行处理。",
        "auto_fixable": "运行 qtcloud-knowl auto-fix 自动修复平台发现的问题。",
    },
}


def _group_issues(issues):
    groups = {}
    for i in issues:
        groups.setdefault(i.group, []).append(i)
    return list(groups.items())


def _print_group(title: str, issues: list) -> None:
    print(f"  {title}")
    for issue in issues:
        print(f"    {issue.label}")
        if issue.action:
            print(f"    → {issue.action}")
    print()


def _print_section(header: str, desc: str, groups: list) -> None:
    if not groups:
        return
    print(f"━━━ {header} ━━━")
    print(f"{desc}\n")
    for name, issues in groups:
        _print_group(name, issues)


def _tail_message(template, mode, has_confirm, has_fixable):
    if mode == AuditMode.SIMPLE:
        return template["tail_messages"].get("simple", "")
    if has_confirm:
        return template["tail_messages"].get("need_confirm", "")
    if has_fixable:
        return template["tail_messages"].get("auto_fixable", "")
    return ""


def _print_report_to_stdout(issues: AuditIssues, template=None) -> None:
    template = template or DEFAULT_REPORT_TEMPLATE
    has_problems = bool(issues.need_confirm or issues.auto_fixable)
    sections = template["sections_simple"] if issues.mode == AuditMode.SIMPLE else template["sections_full"]

    if has_problems:
        for key, header, desc in sections:
            source = {"need_confirm": issues.need_confirm, "auto_fixable": issues.auto_fixable}.get(key)
            groups = _group_issues(source) if source else []
            if groups:
                _print_section(header, desc, groups)

        print("=" * 60)
        print(template["summary_header"])
        print("=" * 60)
        print(f"  · 需要你确认: {len(issues.need_confirm)} 项")
        print(f"  · 平台可修复: {len(issues.auto_fixable)} 项")
        print(f"  · 建议关注:   {len(issues.suggestions)} 项")
        print()
        tail = _tail_message(template, issues.mode, bool(issues.need_confirm), bool(issues.auto_fixable))
        if tail:
            print(tail)

    if issues.suggestions:
        _print_section(
            "建议关注",
            "以下优化建议在全面审计模式下提供。" if issues.mode.value == "full"
            else "以下问题在快速模式下仅供参考，切换到 --mode full 进行全面审计。",
            _group_issues(issues.suggestions),
        )

    if not has_problems and not issues.suggestions:
        print(template["clean_message"])
