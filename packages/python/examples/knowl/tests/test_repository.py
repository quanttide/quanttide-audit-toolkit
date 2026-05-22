from pathlib import Path

from examples.knowl.repository import ReportRepository


class TestReportRepository:
    def test_load_no_state(self, tmp_path):
        repo = ReportRepository(tmp_path)
        assert repo.load_previous_state() is None

    def test_save_then_load(self, tmp_path):
        report = _dummy_audit_report()
        repo = ReportRepository(tmp_path)
        repo.save_report(report, "full")

        loaded = repo.load_previous_state()
        assert loaded is not None
        assert loaded[1] is not None

    def test_load_with_mode_mismatch(self, tmp_path):
        repo = ReportRepository(tmp_path)
        repo.save_report(_dummy_audit_report(), "simple")
        assert repo.load_previous_state(mode="full") is None

    def test_load_corrupted_file(self, tmp_path):
        repo = ReportRepository(tmp_path)
        (tmp_path / "audit.json").write_text("not json", encoding="utf-8")
        assert repo.load_previous_state() is None


def _dummy_audit_report():
    from uuid import uuid4
    from quanttide_audit import AuditReport
    return AuditReport(
        id=uuid4(), name="dummy", title="Dummy",
        findings=[], created_at="2026-01-01T00:00:00", updated_at="2026-01-01T00:00:00",
    )
