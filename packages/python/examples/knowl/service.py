from datetime import datetime
from uuid import uuid4

from quanttide_audit import AuditFinding, AuditReport


def run(findings: list[AuditFinding], mode: str = "full") -> AuditReport:
    if mode not in ("simple", "full"):
        raise ValueError(f"不支持的审计模式 '{mode}'，仅支持 simple / full")

    return AuditReport(
        id=uuid4(), name="knowl-audit-demo", title="知识库审计示例",
        findings=findings,
        created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat(),
    )
