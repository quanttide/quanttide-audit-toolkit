from pathlib import Path

from examples.knowl.models import AuditDiff, AuditIssue, AuditIssues, AuditMode
from examples.knowl.report import DEFAULT_REPORT_TEMPLATE, ReportRepository


def _make_issues(**kw):
    nc = [AuditIssue(category="need_confirm", group="g", label="x")]
    data = dict(mode=AuditMode.FULL, need_confirm=nc, auto_fixable=[], suggestions=[])
    data.update(kw)
    return AuditIssues.from_raw(**data)


class TestReportRepository:
    def test_load_no_state(self, tmp_path):
        repo = ReportRepository(tmp_path)
        assert repo.load_previous_state() is None

    def test_save_then_load(self, tmp_path):
        issues = _make_issues()
        repo = ReportRepository(tmp_path)
        report = _dummy_audit_report()
        repo.save_report(report, issues)

        loaded = repo.load_previous_state()
        assert loaded is not None
        assert loaded.mode == AuditMode.FULL

    def test_load_with_mode_mismatch(self, tmp_path):
        issues = _make_issues(mode=AuditMode.SIMPLE)
        repo = ReportRepository(tmp_path)
        repo.save_report(_dummy_audit_report(), issues)
        assert repo.load_previous_state(mode=AuditMode.FULL) is None

    def test_load_corrupted_file(self, tmp_path):
        repo = ReportRepository(tmp_path)
        (tmp_path / "audit.json").write_text("not json", encoding="utf-8")
        assert repo.load_previous_state() is None


class TestReportTemplate:
    def test_sections_for_full(self):
        assert DEFAULT_REPORT_TEMPLATE.sections_for(AuditMode.FULL) == DEFAULT_REPORT_TEMPLATE.sections_full

    def test_sections_for_simple(self):
        assert DEFAULT_REPORT_TEMPLATE.sections_for(AuditMode.SIMPLE) == DEFAULT_REPORT_TEMPLATE.sections_simple

    def test_tail_for_simple(self):
        t = DEFAULT_REPORT_TEMPLATE.tail_for(AuditMode.SIMPLE, has_confirm=True, has_fixable=True)
        assert "快速检查模式" in t

    def test_tail_for_need_confirm(self):
        t = DEFAULT_REPORT_TEMPLATE.tail_for(AuditMode.FULL, has_confirm=True, has_fixable=False)
        assert "需要你确认" in t

    def test_tail_for_auto_fixable(self):
        t = DEFAULT_REPORT_TEMPLATE.tail_for(AuditMode.FULL, has_confirm=False, has_fixable=True)
        assert "自动修复" in t

    def test_tail_for_no_issues(self):
        t = DEFAULT_REPORT_TEMPLATE.tail_for(AuditMode.FULL, has_confirm=False, has_fixable=False)
        assert t == ""


def _dummy_audit_report():
    from uuid import uuid4
    from quanttide_audit import AuditReport
    return AuditReport(
        id=uuid4(), name="dummy", title="Dummy",
        findings=[], created_at="2026-01-01T00:00:00", updated_at="2026-01-01T00:00:00",
    )
