import uuid

import pytest
from conftest import TS, criteria
from pydantic import ValidationError


class TestAuditCriteria:
    def test_id(self):
        val = uuid.uuid4()
        c = criteria(id=val)
        assert c.id == val

    def test_id_from_str(self):
        val = "00000000-0000-0000-0000-000000000001"
        c = criteria(id=val)
        assert c.id == uuid.UUID(val)

    def test_name(self):
        c = criteria(name="line-length")
        assert c.name == "line-length"

    def test_rejects_long_name(self):
        with pytest.raises(ValidationError):
            criteria(name="a" * 101)

    def test_title(self):
        c = criteria(title="Line length check")
        assert c.title == "Line length check"

    def test_description(self):
        c = criteria(description="Max 88 characters per line")
        assert c.description == "Max 88 characters per line"

    def test_created_at(self):
        c = criteria(created_at=TS)
        assert c.created_at is not None

    def test_updated_at(self):
        c = criteria(updated_at=TS)
        assert c.updated_at is not None
