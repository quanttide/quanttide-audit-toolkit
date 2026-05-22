import re
from uuid import uuid4
from datetime import datetime
from pathlib import Path
from typing import Optional

from quanttide_audit import AuditCriteria, AuditFinding, AuditReport, AuditSeverity

from .tools import all_detection_tools
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

_TOOL_MAP = {
    "validate": ("文件结构问题", AuditSeverity.MINOR),
    "find-undefined-terms": ("未定义术语", AuditSeverity.MAJOR),
    "fusion-check": ("名称冲突或引用断裂", AuditSeverity.MAJOR),
    "check-abstraction": ("本体抽象度不足", AuditSeverity.OBSERVATION),
    "cross-domain-report": ("跨领域关系覆盖率", AuditSeverity.OBSERVATION),
}


def _slug(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)[:48]


def _to_finding(label: str, action: str, group: str, severity: AuditSeverity) -> AuditFinding:
    criterion = _CRITERIA[group]
    return AuditFinding(
        id=uuid4(),
        name=f"{criterion.name}-{_slug(label)[:40]}",
        title=label,
        criterion=criterion,
        evidence=[],
        severity=severity,
        description=action or None,
        created_at=TS,
        updated_at=TS,
    )


def _finding_key(f: AuditFinding) -> str:
    return f"{f.severity.value}|{f.criterion.name}|{f.title}|{f.description or ''}"


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
    return (domains, ontology_count, instance_count)


def _run_tools(ddir, mode):
    parser = ToolOutputParser()
    tools = all_detection_tools(mode)
    findings = []
    for tool in tools:
        inp = {"data_dir": str(ddir)}
        output = tool.execute(inp)
        raw = parser.parse(output, str(ddir))
        if not raw and parser.has_issue(output):
            raw = [{"label": "检测到异常但无法解析具体位置", "action": "请查看上方原始日志确认问题"}]
        entry = _TOOL_MAP.get(tool.name)
        if not entry:
            continue
        group, severity = entry
        for issue in raw:
            findings.append(_to_finding(issue["label"], issue["action"], group, severity))
    return findings


def _validate_args(ddir):
    if not ddir.exists():
        print("审计中止：数据目录不存在")
        print(f"  当前路径: {ddir}")
        print("请确认 QTCLOUD_KNOWL_DATA_HOME 环境变量已正确设置，或传入 data_dir 参数。")
        return False
    return True


def run(data_dir: Optional[str] = None, mode: str = "full") -> int:
    if mode not in ("simple", "full"):
        print(f"错误: 不支持的审计模式 '{mode}'，仅支持 simple / full")
        return 1

    ddir = Path(data_dir) if data_dir else settings.data_home
    if not _validate_args(ddir):
        return 1

    stats = _collect_stats(ddir)
    findings = _run_tools(ddir, mode)

    audit_report = AuditReport(
        id=uuid4(), name=f"knowl-audit-{datetime.now().isoformat()[:10]}", title="知识库审计报告",
        findings=findings,
        created_at=TS, updated_at=TS,
    )

    repo = ReportRepository(settings.state_home)
    previous = repo.load_previous_state(mode=mode)
    diff = None
    prev_ts = None
    if previous:
        prev_findings, prev_ts = previous
        prev_keys = frozenset(f.finding_key() for f in prev_findings)
        curr_keys = frozenset(_finding_key(f) for f in findings)
        diff = (prev_keys - curr_keys, curr_keys - prev_keys, prev_keys & curr_keys)
        prev_ts = prev_ts

    repo.save_report(audit_report, mode)
    render_report(report=audit_report, mode=mode, stats=stats, diff=diff, previous_timestamp=prev_ts)
    has_problems = any(f.severity in (AuditSeverity.MAJOR, AuditSeverity.MINOR) for f in findings)
    return 0 if not has_problems else 1
