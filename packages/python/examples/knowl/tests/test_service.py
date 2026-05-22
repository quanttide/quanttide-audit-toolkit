from examples.knowl.service import run


class TestRun:
    def test_full_mode(self):
        code = run(mode="full")
        assert code == 1

    def test_simple_mode(self):
        code = run(mode="simple")
        assert code == 1

    def test_invalid_mode(self):
        code = run(mode="unknown")
        assert code == 1
