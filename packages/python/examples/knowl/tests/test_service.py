from pathlib import Path

from examples.knowl.service import _collect_stats, _run_tools, _validate_args, run


class TestCollectStats:
    def test_with_domains(self, tmp_path):
        stats = _collect_stats(tmp_path)
        domains, oc, ic = stats
        assert isinstance(domains, list)

    def test_with_invalid_dir(self):
        ddir = Path("/nonexistent-12345")
        stats = _collect_stats(ddir)
        domains, oc, ic = stats
        assert len(domains) == 2


class TestValidateArgs:
    def test_existing_dir(self, tmp_path):
        assert _validate_args(tmp_path) is True

    def test_nonexistent_dir(self):
        d = Path("/nonexistent-xyz-98765")
        assert _validate_args(d) is False


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
