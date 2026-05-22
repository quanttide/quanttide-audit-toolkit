from examples.knowl.render import DEFAULT_REPORT_TEMPLATE


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
