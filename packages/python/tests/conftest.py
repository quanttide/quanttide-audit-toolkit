import uuid

from quanttide_audit import (
    AuditCriteria,
    AuditEvidence,
    AuditFinding,
    AuditReport,
    AuditSeverity,
)

TS = "2026-01-01T00:00:00"


def criteria(**kw):
    data = dict(
        id=uuid.uuid4(),
        name="line-length",
        title="Line length check",
        description="Lines should not exceed 88 characters",
        created_at=TS,
        updated_at=TS,
    )
    data.update(kw)
    return AuditCriteria(**data)


def evidence(**kw):
    data = dict(
        id=uuid.uuid4(),
        name="ev-1",
        title="Line 42 exceeds limit",
        description="Line has 92 chars, max is 88",
        created_at=TS,
        updated_at=TS,
    )
    data.update(kw)
    return AuditEvidence(**data)


def finding(**kw):
    data = dict(
        id=uuid.uuid4(),
        name="f-1",
        criterion=criteria(),
        evidence=[evidence()],
        title="Line too long",
        description="Break into multiple lines",
        severity=AuditSeverity.MAJOR,
        created_at=TS,
        updated_at=TS,
    )
    data.update(kw)
    return AuditFinding(**data)


def report(**kw):
    data = dict(
        id=uuid.uuid4(),
        name="rep-1",
        title="Audit #1",
        created_at=TS,
        updated_at=TS,
    )
    data.update(kw)
    return AuditReport(**data)
