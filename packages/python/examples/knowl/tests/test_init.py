from examples.knowl import Report, ReportRepository, run


class TestInit:
    def test_exports_run(self):
        assert callable(run)

    def test_exports_report(self):
        assert Report is not None

    def test_exports_report_repository(self):
        assert ReportRepository is not None
