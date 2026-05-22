import re
from uuid import uuid4
from pathlib import Path

from quanttide_audit import AuditCriteria, AuditFinding, AuditReport, AuditSeverity

from .render import render_report
from .repository import ReportRepository


TS = "2026-01-01T00:00:00"

_FIXED_CRITERIA_UUIDS = {
    "file-structure": "11111111-1111-1111-1111-111111111111",
    "undefined-terms": "22222222-2222-2222-2222-222222222222",
    "name-conflict": "33333333-3333-3333-3333-333333333333",
    "abstraction-level": "44444444-4444-4444-4444-444444444444",
    "cross-domain-coverage": "55555555-5555-5555-5555-555555555555",
}

_CRITERIA = {
    "文件结构问题": AuditCriteria(
        id=_FIXED_CRITERIA_UUIDS["file-structure"], name="file-structure", title="文件结构检查",
        description="检查知识库文件结构是否完整", created_at=TS, updated_at=TS,
    ),
    "未定义术语": AuditCriteria(
        id=_FIXED_CRITERIA_UUIDS["undefined-terms"], name="undefined-terms", title="未定义术语检查",
        description="检测领域本体中使用了未在 vocabulary 中定义的术语", created_at=TS, updated_at=TS,
    ),
    "名称冲突或引用断裂": AuditCriteria(
        id=_FIXED_CRITERIA_UUIDS["name-conflict"], name="name-conflict", title="名称冲突与引用断裂检查",
        description="检测领域间名称冲突和悬挂引用", created_at=TS, updated_at=TS,
    ),
    "本体抽象度不足": AuditCriteria(
        id=_FIXED_CRITERIA_UUIDS["abstraction-level"], name="abstraction-level", title="本体抽象度检查",
        description="检测具体值应抽象为变量的情况", created_at=TS, updated_at=TS,
    ),
    "跨领域关系覆盖率": AuditCriteria(
        id=_FIXED_CRITERIA_UUIDS["cross-domain-coverage"], name="cross-domain-coverage", title="跨领域关系覆盖率",
        description="检测跨领域关系的覆盖程度", created_at=TS, updated_at=TS,
    ),
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


def run(findings: list[AuditFinding], mode: str = "full", state_dir: Path = Path.home() / ".quanttide" / "audit") -> int:
    if mode not in ("simple", "full"):
        print(f"不支持的审计模式 '{mode}'，仅支持 simple / full")
        return 1

    audit_report = AuditReport(
        id=uuid4(), name="knowl-audit-demo", title="知识库审计示例",
        findings=findings,
        created_at=TS, updated_at=TS,
    )

    repo = ReportRepository(state_dir)
    previous = repo.load_previous_state(mode=mode)
    diff = None
    prev_ts = None
    if previous:
        prev_keys, prev_ts = previous
        curr_keys = frozenset(_finding_key(f) for f in findings)
        diff = (prev_keys - curr_keys, curr_keys - prev_keys, prev_keys & curr_keys)

    repo.save_report(audit_report, mode)
    render_report(report=audit_report, mode=mode, diff=diff, previous_timestamp=prev_ts)
    has_problems = any(f.severity in (AuditSeverity.MAJOR, AuditSeverity.MINOR) for f in findings)
    return 0 if not has_problems else 1
