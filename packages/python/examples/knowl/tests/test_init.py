from examples.knowl import run


class TestInit:
    def test_exports_run(self):
        assert callable(run)
