import json
from pathlib import Path

from examples.knowl.models import AuditIssue, AuditMode, AuditReport as AuditIssues
from examples.knowl.report import DEFAULT_REPORT_TEMPLATE, Report, ReportRepository


def _make_issues(**kw):
    nc = [AuditIssue(category="need_confirm", group="g", label="x")]
    data = dict(mode=AuditMode.FULL, need_confirm=nc, auto_fixable=[], suggestions=[])
    data.update(kw)
    return AuditIssues.from_raw(**data)


class TestReport:
    def test_build_without_previous(self):
        issues = _make_issues()
        r = Report.build(AuditMode.FULL, None, issues.need_confirm, issues.auto_fixable, issues.suggestions)
        assert r.mode == AuditMode.FULL
        assert r.diff is None
        assert r.previous_timestamp is None

    def test_build_with_previous(self):
        prev = _make_issues()
        cur = _make_issues()
        r = Report.build(
            AuditMode.FULL, None, cur.need_confirm, cur.auto_fixable, cur.suggestions,
            previous_state=_PreviousAudit(prev.need_confirm, "2026-01-01"),
        )
        assert r.diff is not None
        assert r.previous_timestamp == "2026-01-01"
        assert len(r.diff.pending) == 1
        assert len(r.diff.fixed) == 0
        assert len(r.diff.new) == 0

    def test_exit_code(self):
        r = Report.build(AuditMode.FULL, None, [], [], [])
        assert r.exit_code == 0

        dirty = _make_issues()
        r = Report.build(AuditMode.FULL, None, dirty.need_confirm, dirty.auto_fixable, dirty.suggestions)
        assert r.exit_code == 1


class TestReportRepository:
    def test_load_no_state(self, tmp_path):
        repo = ReportRepository(tmp_path)
        assert repo.load_previous_state() is None

    def test_save_then_load(self, tmp_path):
        issues = _make_issues()
        r = Report.build(AuditMode.FULL, None, issues.need_confirm, issues.auto_fixable, issues.suggestions)

        repo = ReportRepository(tmp_path)
        repo.save_report(r)

        loaded = repo.load_previous_state()
        assert loaded is not None
        assert loaded.mode == AuditMode.FULL

    def test_load_with_mode_mismatch(self, tmp_path):
        issues = _make_issues()
        r = Report.build(AuditMode.SIMPLE, None, issues.need_confirm, issues.auto_fixable, issues.suggestions)
        repo = ReportRepository(tmp_path)
        repo.save_report(r)
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


class _PreviousAudit:
    def __init__(self, issues, timestamp, mode=AuditMode.FULL):
        self.issues = issues
        self.timestamp = timestamp
        self.mode = mode
