import uuid

from conftest import TS, finding, report


class TestAuditReport:
    def test_id(self):
        val = uuid.uuid4()
        r = report(id=val)
        assert r.id == val

    def test_id_from_str(self):
        val = "00000000-0000-0000-0000-000000000001"
        r = report(id=val)
        assert r.id == uuid.UUID(val)

    def test_name(self):
        r = report(name="rep-1")
        assert r.name == "rep-1"

    def test_title(self):
        r = report(title="Audit #1")
        assert r.title == "Audit #1"

    def test_description_optional(self):
        r = report()
        assert r.description is None

    def test_description(self):
        r = report(description="Full audit report")
        assert r.description == "Full audit report"

    def test_findings_default_empty(self):
        r = report()
        assert r.findings == []

    def test_findings(self):
        r = report(findings=[finding(name="f1"), finding(name="f2")])
        assert len(r.findings) == 2

    def test_created_at(self):
        r = report(created_at=TS)
        assert r.created_at is not None

    def test_updated_at(self):
        r = report(updated_at=TS)
        assert r.updated_at is not None
