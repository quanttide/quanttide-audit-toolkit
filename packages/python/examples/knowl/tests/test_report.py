from pathlib import Path

from examples.knowl.report import DEFAULT_REPORT_TEMPLATE, ReportRepository


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


class TestReportTemplate:
    def test_sections_for_full(self):
        assert DEFAULT_REPORT_TEMPLATE["sections_full"] is not None

    def test_sections_for_simple(self):
        assert DEFAULT_REPORT_TEMPLATE["sections_simple"] is not None

    def test_tail_message_simple(self):
        t = DEFAULT_REPORT_TEMPLATE["tail_messages"]["simple"]
        assert "快速检查模式" in t

    def test_tail_message_major(self):
        t = DEFAULT_REPORT_TEMPLATE["tail_messages"]["major"]
        assert "需要你确认" in t

    def test_tail_message_minor(self):
        t = DEFAULT_REPORT_TEMPLATE["tail_messages"]["minor"]
        assert "自动修复" in t

    def test_clean_message(self):
        assert DEFAULT_REPORT_TEMPLATE["clean_message"] != ""


def _dummy_audit_report():
    from uuid import uuid4
    from quanttide_audit import AuditReport
    return AuditReport(
        id=uuid4(), name="dummy", title="Dummy",
        findings=[], created_at="2026-01-01T00:00:00", updated_at="2026-01-01T00:00:00",
    )
