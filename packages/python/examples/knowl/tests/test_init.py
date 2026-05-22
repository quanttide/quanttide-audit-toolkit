from examples.knowl import ReportRepository, render_report, run


class TestInit:
    def test_exports_run(self):
        assert callable(run)

    def test_exports_render_report(self):
        assert callable(render_report)

    def test_exports_report_repository(self):
        assert ReportRepository is not None
