import uuid

from conftest import TS, evidence


class TestAuditEvidence:
    def test_id(self):
        val = uuid.uuid4()
        e = evidence(id=val)
        assert e.id == val

    def test_id_from_str(self):
        val = "00000000-0000-0000-0000-000000000001"
        e = evidence(id=val)
        assert e.id == uuid.UUID(val)

    def test_name(self):
        e = evidence(name="ev-1")
        assert e.name == "ev-1"

    def test_title(self):
        e = evidence(title="Line 42 exceeds limit")
        assert e.title == "Line 42 exceeds limit"

    def test_description(self):
        e = evidence(description="Line has 92 chars, max is 88")
        assert e.description == "Line has 92 chars, max is 88"

    def test_created_at(self):
        e = evidence(created_at=TS)
        assert e.created_at is not None

    def test_updated_at(self):
        e = evidence(updated_at=TS)
        assert e.updated_at is not None
