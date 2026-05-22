from quanttide_audit import AuditReport, AuditSeverity


def render_report(
    *,
    report: AuditReport,
    mode: str,
) -> None:
    print("=" * 60)
    print("  检测结果")
    print("=" * 60)
    print()
    _print_report_to_stdout(report, mode)


DEFAULT_REPORT_TEMPLATE = {
    "sections_full": [
        ("major", "需要你确认的问题", "以下问题平台无法自动判断，需要你决定如何处理。"),
        ("minor", "平台发现的问题", "以下问题平台已识别，可通过自动修复处理。"),
    ],
    "sections_simple": [
        ("major", "建议关注", "以下问题可由平台自动修复，无需手动处理。"),
        ("minor", "平台发现的问题", "以下问题平台已识别，可通过自动修复处理。"),
    ],
    "clean_message": "✓ 未发现问题，知识库结构良好。",
    "summary_header": "  汇总",
    "tail_messages": {
        "simple": "当前为快速检查模式，运行 qtcloud-knowl audit --mode full 进行全面审计。",
        "major": "请先处理「需要你确认的问题」，其他问题可并行处理。",
        "minor": "运行 qtcloud-knowl auto-fix 自动修复平台发现的问题。",
    },
}


def _print_report_to_stdout(report: AuditReport, mode: str, template=None) -> None:
    print(f"  {title}")
    for f in findings:
        print(f"    {f.title}")
        if f.description:
            print(f"    → {f.description}")
    print()


def _print_group(title: str, findings: list) -> None:
    print(f"  {title}")
    for f in findings:
        print(f"    {f.title}")
        if f.description:
            print(f"    → {f.description}")
    print()


def _print_section(header: str, desc: str, groups: list) -> None:
    if not groups:
        return
    print(f"━━━ {header} ━━━")
    print(f"{desc}\n")
    for name, items in groups:
        _print_group(name, items)


def _tail_message(template, mode, has_major, has_minor):
    if mode == "simple":
        return template["tail_messages"].get("simple", "")
    if has_major:
        return template["tail_messages"].get("major", "")
    if has_minor:
        return template["tail_messages"].get("minor", "")
    return ""


def _print_report_to_stdout(report: AuditReport, mode: str, template=None) -> None:
    template = template or DEFAULT_REPORT_TEMPLATE
    major = [f for f in report.findings if f.severity == AuditSeverity.MAJOR]
    minor = [f for f in report.findings if f.severity == AuditSeverity.MINOR]
    obs = [f for f in report.findings if f.severity == AuditSeverity.OBSERVATION]

    sections = template["sections_simple"] if mode == "simple" else template["sections_full"]

    if mode == "simple":
        obs = major + obs
        major = minor
        minor = []

    has_problems = bool(major or minor)

    if has_problems:
        for sev_key, header, desc in sections:
            source = {"major": major, "minor": minor}.get(sev_key, [])
            groups = {}
            for f in source:
                groups.setdefault(f.criterion.name, []).append(f)
            groups = list(groups.items())
            if groups:
                _print_section(header, desc, groups)

        print("=" * 60)
        print(template["summary_header"])
        print("=" * 60)
        print(f"  · 需要你确认: {len(major)} 项")
        print(f"  · 平台可修复: {len(minor)} 项")
        print(f"  · 建议关注:   {len(obs)} 项")
        print()
        tail = _tail_message(template, mode, bool(major), bool(minor))
        if tail:
            print(tail)

    if obs:
        _groups = {}
        for f in obs:
            _groups.setdefault(f.criterion.name, []).append(f)
        _print_section(
            "建议关注",
            "以下优化建议在全面审计模式下提供。" if mode == "full" else "以下问题在快速模式下仅供参考，切换到 --mode full 进行全面审计。",
            list(_groups.items()),
        )

    if not has_problems and not obs:
        print(template["clean_message"])
