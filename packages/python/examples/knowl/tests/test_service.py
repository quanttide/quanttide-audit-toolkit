from pathlib import Path

from examples.knowl.models import AuditMode, KnowledgeBaseStats
from examples.knowl.service import _categorize_issues, _collect_stats, _validate_args, run


class TestCategorizeIssues:
    def test_full_mapping(self):
        raw = [
            ("validate", [FakeIssue(label="v1")]),
            ("find-undefined-terms", [FakeIssue(label="t1")]),
            ("fusion-check", [FakeIssue(label="f1")]),
            ("check-abstraction", [FakeIssue(label="a1")]),
            ("cross-domain-report", [FakeIssue(label="c1")]),
        ]
        nc, af, sg = _categorize_issues(raw, AuditMode.FULL)
        assert len(af) == 1
        assert len(nc) == 2
        assert len(sg) == 2

    def test_unknown_tool_skipped(self):
        raw = [("unknown-tool", [FakeIssue(label="x")])]
        nc, af, sg = _categorize_issues(raw, AuditMode.FULL)
        assert nc == []
        assert af == []
        assert sg == []

    def test_empty_issues_skipped(self):
        raw = [("validate", [])]
        nc, af, sg = _categorize_issues(raw, AuditMode.FULL)
        assert nc == [] and af == [] and sg == []

    def test_issue_category_overrides(self):
        raw = [("validate", [FakeIssue(label="x", category="auto_fixable")])]
        nc, af, sg = _categorize_issues(raw, AuditMode.FULL)
        assert len(af) == 1
        assert af[0].category == "auto_fixable"
        assert af[0].group == "文件结构问题"


class TestCollectStats:
    def test_with_domains(self):
        ddir = Path("/tmp")
        stats = _collect_stats(ddir)
        assert isinstance(stats, KnowledgeBaseStats)
        assert stats.domain_count >= 0

    def test_with_invalid_dir(self):
        ddir = Path("/nonexistent-12345")
        stats = _collect_stats(ddir)
        assert stats.domain_count == 2


class TestValidateArgs:
    def test_existing_dir(self, tmp_path):
        assert _validate_args(tmp_path, AuditMode.FULL) is True

    def test_nonexistent_dir(self):
        d = Path("/nonexistent-xyz-98765")
        assert _validate_args(d, AuditMode.FULL) is False


class TestRun:
    def test_full_mode(self, tmp_path):
        code = run(data_dir=str(tmp_path), mode="full")
        assert code == 1

    def test_simple_mode(self, tmp_path):
        code = run(data_dir=str(tmp_path), mode="simple")
        assert code == 1

    def test_invalid_mode(self, tmp_path):
        code = run(data_dir=str(tmp_path), mode="unknown")
        assert code == 1

    def test_nonexistent_dir(self):
        code = run(data_dir="/nonexistent-xyz-98765", mode="full")
        assert code == 1


class FakeIssue:
    def __init__(self, label="x", category="auto_fixable"):
        self.label = label
        self.action = ""
        self.category = category
