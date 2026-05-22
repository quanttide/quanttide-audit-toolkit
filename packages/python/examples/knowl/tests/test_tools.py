from examples.knowl.tools import _FakeTool, all_detection_tools


class TestFakeTool:
    def test_name(self):
        t = _FakeTool("validate")
        assert t.name == "validate"

    def test_execute_returns_string(self):
        t = _FakeTool("validate")
        result = t.execute({"data_dir": "/tmp"})
        assert isinstance(result, str)
        assert len(result) > 0

    def test_execute_unknown_tool(self):
        t = _FakeTool("nonexistent")
        assert t.execute({}) == ""


class TestAllDetectionTools:
    def test_returns_list(self):
        tools = all_detection_tools("full")
        assert len(tools) > 0

    def test_each_tool_has_name(self):
        for t in all_detection_tools("full"):
            assert hasattr(t, "name")

    def test_each_tool_has_execute(self):
        for t in all_detection_tools("full"):
            assert hasattr(t, "execute")

    def test_execute_all_return_strings(self):
        for t in all_detection_tools("full"):
            result = t.execute({"data_dir": "/tmp"})
            assert isinstance(result, str)
