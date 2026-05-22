from datetime import datetime
from uuid import uuid4

from quanttide_audit import AuditFinding, AuditReport, AuditSeverity

from .render import render_report


def run(findings: list[AuditFinding], mode: str = "full") -> int:
    if mode not in ("simple", "full"):
        print(f"不支持的审计模式 '{mode}'，仅支持 simple / full")
        return 1

    audit_report = AuditReport(
        id=uuid4(), name="knowl-audit-demo", title="知识库审计示例",
        findings=findings,
        created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat(),
    )

    render_report(report=audit_report, mode=mode)
    has_problems = any(f.severity in (AuditSeverity.MAJOR, AuditSeverity.MINOR) for f in findings)
    return 0 if not has_problems else 1
