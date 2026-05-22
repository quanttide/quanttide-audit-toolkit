import uuid

from conftest import TS, criteria, evidence, finding

from quanttide_audit import AuditCriteria, AuditEvidence, AuditSeverity


class TestAuditFinding:
    def test_id(self):
        val = uuid.uuid4()
        f = finding(id=val)
        assert f.id == val

    def test_id_from_str(self):
        val = "00000000-0000-0000-0000-000000000001"
        f = finding(id=val)
        assert f.id == uuid.UUID(val)

    def test_name(self):
        f = finding(name="f-1")
        assert f.name == "f-1"

    def test_title(self):
        f = finding(title="Line too long")
        assert f.title == "Line too long"

    def test_criterion(self):
        c = criteria(name="complexity-check")
        f = finding(criterion=c)
        assert f.criterion.name == "complexity-check"
        assert isinstance(f.criterion, AuditCriteria)

    def test_evidence(self):
        e = evidence(name="ev-loc1")
        f = finding(evidence=[e])
        assert len(f.evidence) == 1
        assert f.evidence[0].name == "ev-loc1"
        assert isinstance(f.evidence[0], AuditEvidence)

    def test_evidence_default_empty(self):
        f = finding(evidence=[])
        assert f.evidence == []

    def test_description(self):
        f = finding(description="Use shorter variable names")
        assert f.description == "Use shorter variable names"

    def test_description_optional(self):
        f = finding(description=None)
        assert f.description is None

    def test_severity(self):
        f = finding(severity=AuditSeverity.MAJOR)
        assert f.severity == AuditSeverity.MAJOR

    def test_severity_minor(self):
        f = finding(severity=AuditSeverity.MINOR)
        assert f.severity == AuditSeverity.MINOR

    def test_severity_observation(self):
        f = finding(severity=AuditSeverity.OBSERVATION)
        assert f.severity == AuditSeverity.OBSERVATION

    def test_created_at(self):
        f = finding(created_at=TS)
        assert f.created_at is not None

    def test_updated_at(self):
        f = finding(updated_at=TS)
        assert f.updated_at is not None
