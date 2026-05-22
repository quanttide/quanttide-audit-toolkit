import re
from uuid import uuid4
from pathlib import Path
from typing import Optional

from quanttide_audit import AuditCriteria, AuditFinding, AuditReport, AuditSeverity

from .parser import ToolOutputParser
from .report import render_report, ReportRepository


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

_SAMPLE_OUTPUTS = {
    "validate": (
        "=== engineering ===\n[MISS] ontologies.json\n[FAIL] JSON 格式错误: instances.json 第 5 行缺少逗号\n"
        "=== finance ===\n[MISS] domain.json\n"
    ),
    "find-undefined-terms": "=== engineering ===\n在 domain ontology 中使用了术语 深度学习\n在 domain ontology 中使用了术语 知识图谱\n",
    "fusion-check": "=== finance ===\n【需人确认】引用不存在的实例 budget-2024\n",
    "check-abstraction": "=== engineering ===\n[检测到] 具体值 MySQL 应抽象为变量\n",
    "cross-domain-report": "=== engineering ===\n跨领域关系覆盖率: 65%\n=== finance ===\n跨领域关系覆盖率: 42%\n",
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


def run(mode: str = "full") -> int:
    if mode not in ("simple", "full"):
        print(f"不支持的审计模式 '{mode}'，仅支持 simple / full")
        return 1

    parser = ToolOutputParser()
    findings = []
    for tool_name, sample in _SAMPLE_OUTPUTS.items():
        raw = parser.parse(sample)
        group, severity = _TOOL_MAP[tool_name]
        for issue in raw:
            findings.append(_to_finding(issue["label"], issue["action"], group, severity))

    audit_report = AuditReport(
        id=uuid4(), name="knowl-audit-demo", title="知识库审计示例",
        findings=findings,
        created_at=TS, updated_at=TS,
    )

    repo = ReportRepository(Path.home() / ".quanttide" / "audit")
    previous = repo.load_previous_state(mode=mode)
    diff = None
    prev_ts = None
    if previous:
        prev_findings, prev_ts = previous
        prev_keys = frozenset(f.finding_key() for f in prev_findings)
        curr_keys = frozenset(_finding_key(f) for f in findings)
        diff = (prev_keys - curr_keys, curr_keys - prev_keys, prev_keys & curr_keys)

    repo.save_report(audit_report, mode)
    render_report(report=audit_report, mode=mode, diff=diff, previous_timestamp=prev_ts)
    has_problems = any(f.severity in (AuditSeverity.MAJOR, AuditSeverity.MINOR) for f in findings)
    return 0 if not has_problems else 1
