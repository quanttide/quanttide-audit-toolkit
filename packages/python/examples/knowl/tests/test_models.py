import pytest
from pathlib import Path

from examples.knowl.models import (
    AuditDiff,
    AuditIssue,
    AuditIssues,
    AuditMode,
    KnowledgeBaseStats,
)


class TestAuditMode:
    def test_values(self):
        assert AuditMode.SIMPLE.value == "simple"
        assert AuditMode.FULL.value == "full"

    def test_missing_match_by_value(self):
        assert AuditMode._missing_("simple") is AuditMode.SIMPLE
        assert AuditMode._missing_("full") is AuditMode.FULL

    def test_missing_unknown(self):
        assert AuditMode._missing_("unknown") is None

    def test_missing_non_string(self):
        assert AuditMode._missing_(123) is None


class TestAuditIssue:
    def test_issue_key(self):
        issue = AuditIssue(category="a", group="g", label="l")
        assert issue.issue_key() == "a|g|l"

    def test_action_default(self):
        issue = AuditIssue(category="a", group="g", label="l")
        assert issue.action == ""

    def test_frozen(self):
        issue = AuditIssue(category="a", group="g", label="l")
        with pytest.raises(AttributeError):
            issue.category = "b"


class TestAuditDiff:
    def test_compute_all_categories(self):
        prev = [AuditIssue(category="c", group="g", label="fixed")]
        curr = [AuditIssue(category="c", group="g", label="new")]
        diff = AuditDiff.compute(prev, curr, "2026-01-01")
        assert diff.fixed == frozenset({"c|g|fixed"})
        assert diff.new == frozenset({"c|g|new"})
        assert diff.pending == frozenset()
        assert diff.previous_timestamp == "2026-01-01"

    def test_compute_pending(self):
        shared = AuditIssue(category="c", group="g", label="both")
        diff = AuditDiff.compute([shared], [shared])
        assert diff.fixed == frozenset()
        assert diff.new == frozenset()
        assert diff.pending == frozenset({"c|g|both"})

    def test_has_changes_true_when_fixed(self):
        prev = [AuditIssue(category="c", group="g", label="x")]
        curr = []
        assert AuditDiff.compute(prev, curr).has_changes is True

    def test_pending_only_means_no_changes(self):
        shared = [AuditIssue(category="c", group="g", label="x")]
        diff = AuditDiff.compute(shared, shared)
        assert diff.has_changes is False
        assert diff.is_identical is True

    def test_no_previous_timestamp(self):
        diff = AuditDiff.compute([], [])
        assert diff.previous_timestamp is None


class TestKnowledgeBaseStats:
    def test_domain_count(self):
        stats = KnowledgeBaseStats(data_dir=Path("/x"), domains=["a", "b"], ontology_count=3, instance_count=5)
        assert stats.domain_count == 2

    def test_has_domains_true(self):
        stats = KnowledgeBaseStats(data_dir=Path("/x"), domains=["a"], ontology_count=0, instance_count=0)
        assert stats.has_domains is True

    def test_has_domains_false(self):
        stats = KnowledgeBaseStats(data_dir=Path("/x"), domains=[], ontology_count=0, instance_count=0)
        assert stats.has_domains is False

    def test_fields(self):
        d = Path("/data")
        stats = KnowledgeBaseStats(data_dir=d, domains=["x"], ontology_count=1, instance_count=2)
        assert stats.data_dir == d
        assert stats.ontology_count == 1
        assert stats.instance_count == 2


class TestAuditIssues:
    def test_from_raw_full(self):
        nc = [AuditIssue(category="need_confirm", group="g", label="nc")]
        af = [AuditIssue(category="auto_fixable", group="g", label="af")]
        sg = [AuditIssue(category="suggestions", group="g", label="sg")]
        r = AuditIssues.from_raw(nc, af, sg, AuditMode.FULL)
        assert r.need_confirm == nc
        assert r.auto_fixable == af
        assert r.suggestions == sg

    def test_from_raw_simple(self):
        nc = [AuditIssue(category="need_confirm", group="g", label="nc")]
        af = [AuditIssue(category="auto_fixable", group="g", label="af")]
        sg = [AuditIssue(category="suggestions", group="g", label="sg")]
        r = AuditIssues.from_raw(nc, af, sg, AuditMode.SIMPLE)
        assert r.need_confirm == af
        assert r.auto_fixable == []
        assert nc[0] in r.suggestions
        assert sg[0] in r.suggestions
