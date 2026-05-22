import re
from uuid import uuid4
from datetime import datetime
from pathlib import Path
from typing import Optional

from quanttide_audit import AuditCriteria, AuditFinding, AuditReport, AuditSeverity

from .tools import all_detection_tools
from .models import AuditDiff as _AuditDiff, AuditIssues, AuditIssue, AuditMode, KnowledgeBaseStats
from .parser import ToolOutputParser
from .report import render_report, ReportRepository
from .config import settings
from .loader import load_all_domains


TS = "2026-01-01T00:00:00"


_CRITERIA = {
    "文件结构问题": AuditCriteria(
        id=uuid4(), name="file-structure", title="文件结构检查",
        description="检查知识库文件结构是否完整", created_at=TS, updated_at=TS,
    ),
    "未定义术语": AuditCriteria(
        id=uuid4(), name="undefined-terms", title="未定义术语检查",
        description="检测领域本体中使用了未在 vocabulary 中定义的术语", created_at=TS, updated_at=TS,
    ),
    "名称冲突或引用断裂": AuditCriteria(
        id=uuid4(), name="name-conflict", title="名称冲突与引用断裂检查",
        description="检测领域间名称冲突和悬挂引用", created_at=TS, updated_at=TS,
    ),
    "本体抽象度不足": AuditCriteria(
        id=uuid4(), name="abstraction-level", title="本体抽象度检查",
        description="检测具体值应抽象为变量的情况", created_at=TS, updated_at=TS,
    ),
    "跨领域关系覆盖率": AuditCriteria(
        id=uuid4(), name="cross-domain-coverage", title="跨领域关系覆盖率",
        description="检测跨领域关系的覆盖程度", created_at=TS, updated_at=TS,
    ),
}

_SEVERITY_MAP = {
    "need_confirm": AuditSeverity.MAJOR,
    "auto_fixable": AuditSeverity.MINOR,
    "suggestions": AuditSeverity.OBSERVATION,
}


def _slug(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    s = re.sub(r"[\s_]+", "-", s)
    return s[:48]


def _to_finding(issue: AuditIssue, idx: int = 0) -> AuditFinding:
    criterion = _CRITERIA[issue.group]
    return AuditFinding(
        id=uuid4(),
        name=f"{criterion.name}-{_slug(issue.label)[:40] or idx}",
        title=issue.label,
        criterion=criterion,
        evidence=[],
        severity=_SEVERITY_MAP.get(issue.category, AuditSeverity.OBSERVATION),
        description=issue.action or None,
        created_at=TS,
        updated_at=TS,
    )


def _collect_stats(ddir):
    domains = []
    ontology_count = 0
    instance_count = 0
    try:
        for d, domain, ontologies, instances in load_all_domains(ddir):
            domains.append(domain)
            ontology_count += len(ontologies)
            instance_count += len(instances)
    except Exception:
        pass
    return KnowledgeBaseStats(data_dir=ddir, domains=domains, ontology_count=ontology_count, instance_count=instance_count)


def _categorize_issues(raw_issues, mode):
    need_confirm = []
    auto_fixable = []
    suggestions = []
    mapping = {
        "validate": ("文件结构问题", "auto_fixable"),
        "find-undefined-terms": ("未定义术语", "need_confirm"),
        "fusion-check": ("名称冲突或引用断裂", "need_confirm"),
        "check-abstraction": ("本体抽象度不足", "suggestions"),
        "cross-domain-report": ("跨领域关系覆盖率", "suggestions"),
    }
    for tool_name, issues in raw_issues:
        entry = mapping.get(tool_name)
        if not entry or not issues:
            continue
        group, category = entry
        target = {"need_confirm": need_confirm, "auto_fixable": auto_fixable, "suggestions": suggestions}
        for issue in issues:
            target[category].append(
                AuditIssue(category=category, group=group, label=issue.label, action=issue.action)
            )
    return need_confirm, auto_fixable, suggestions


def _run_tools(ddir, mode):
    parser = ToolOutputParser()
    tools = all_detection_tools(mode.value)
    raw_issues = []
    for tool in tools:
        inp = {"data_dir": str(ddir)}
        output = tool.execute(inp)
        issues = parser.parse(output, str(ddir))
        if not issues and parser.has_issue(output):
            issues.append(
                AuditIssue(
                    category="need_confirm",
                    group=tool.name,
                    label="检测到异常但无法解析具体位置",
                    action="请查看上方原始日志确认问题",
                )
            )
        raw_issues.append((tool.name, issues))
    return _categorize_issues(raw_issues, mode)


def _validate_args(ddir, mode):
    if not ddir.exists():
        print("审计中止：数据目录不存在")
        print(f"  当前路径: {ddir}")
        print("请确认 QTCLOUD_KNOWL_DATA_HOME 环境变量已正确设置，或传入 data_dir 参数。")
        return False
    return True


def run(data_dir: Optional[str] = None, mode: str = "full") -> int:
    ddir = Path(data_dir) if data_dir else settings.data_home
    try:
        mode_vo = AuditMode(mode) if isinstance(mode, str) else mode
    except ValueError:
        print(f"错误: 不支持的审计模式 '{mode}'，仅支持 simple / full")
        return 1

    if not _validate_args(ddir, mode_vo):
        return 1

    stats = _collect_stats(ddir)
    need_confirm, auto_fixable, suggestions = _run_tools(ddir, mode_vo)
    issues = AuditIssues.from_raw(need_confirm, auto_fixable, suggestions, mode_vo)
    all_raw = need_confirm + auto_fixable + suggestions

    audit_report = AuditReport(
        id=uuid4(), name=f"knowl-audit-{datetime.now().isoformat()[:10]}", title="知识库审计报告",
        findings=[_to_finding(i, idx) for idx, i in enumerate(all_raw)],
        created_at=TS, updated_at=TS,
    )

    repo = ReportRepository(settings.state_home)
    previous = repo.load_previous_state(mode=mode_vo)
    diff = None
    prev_ts = None
    if previous:
        diff = _AuditDiff.compute(previous.issues, all_raw, previous.timestamp)
        prev_ts = previous.timestamp

    repo.save_report(audit_report, issues)
    render_report(report=audit_report, mode=mode_vo, stats=stats, issues=issues, diff=diff, previous_timestamp=prev_ts)
    return issues.exit_code
