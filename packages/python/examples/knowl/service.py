from datetime import datetime
from uuid import uuid4
from pathlib import Path

from quanttide_audit import AuditFinding, AuditReport, AuditSeverity

from .render import render_report
from .repository import ReportRepository


_now = lambda: datetime.now().isoformat()


def _finding_key(f: AuditFinding) -> str:
    return f"{f.severity.value}|{f.criterion.name}|{f.title}|{f.description or ''}"


def run(findings: list[AuditFinding], mode: str = "full", state_dir: Path = Path.home() / ".quanttide" / "audit") -> int:
    if mode not in ("simple", "full"):
        print(f"不支持的审计模式 '{mode}'，仅支持 simple / full")
        return 1

    audit_report = AuditReport(
        id=uuid4(), name="knowl-audit-demo", title="知识库审计示例",
        findings=findings,
        created_at=_now(), updated_at=_now(),
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
