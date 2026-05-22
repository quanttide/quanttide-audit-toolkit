from examples.knowl.parser import ToolOutputParser


class TestToolOutputParser:
    def make_parser(self):
        return ToolOutputParser()

    def test_parse_empty(self):
        p = self.make_parser()
        assert p.parse("") == []
        assert p.parse("  \n  ") == []

    def test_parse_section_header(self):
        p = self.make_parser()
        issues = p.parse("=== my-domain ===")
        assert issues == []

    def test_parse_miss(self):
        p = self.make_parser()
        issues = p.parse("[MISS] missing.csv")
        assert len(issues) == 1
        assert "缺少文件" in issues[0]["label"]

    def test_parse_miss_with_domain(self):
        p = self.make_parser()
        issues = p.parse("=== eng ===\n[MISS] missing.csv", "/data")
        assert len(issues) == 1
        assert "/data/eng/missing.csv" in issues[0]["action"]

    def test_parse_fail(self):
        p = self.make_parser()
        issues = p.parse("[FAIL] syntax error")
        assert len(issues) == 1
        assert "JSON 格式错误" in issues[0]["label"]
        assert "syntax error" in issues[0]["label"]

    def test_parse_term(self):
        p = self.make_parser()
        issues = p.parse("在文件中使用了术语 机器学习")
        assert len(issues) == 1
        assert "术语" in issues[0]["label"]

    def test_parse_confirm(self):
        p = self.make_parser()
        issues = p.parse("【需人确认】引用不存在的实体 X")
        assert len(issues) == 1

    def test_parse_abstraction(self):
        p = self.make_parser()
        issues = p.parse("[检测到] 具体值 42 应抽象为变量")
        assert len(issues) == 1
        assert "42" in issues[0]["label"]

    def test_parse_multiple_issues(self):
        p = self.make_parser()
        output = "[MISS] a.json\n[FAIL] b.json 格式错误\n"
        issues = p.parse(output)
        assert len(issues) == 2

    def test_parse_mixed_with_sections(self):
        p = self.make_parser()
        output = "=== domain1 ===\n[MISS] a.json\n=== domain2 ===\n[FAIL] b.json"
        issues = p.parse(output)
        assert len(issues) == 2

    def test_parse_no_match(self):
        p = self.make_parser()
        issues = p.parse("some random line without tags")
        assert issues == []

    def test_parse_first_match_wins(self):
        p = self.make_parser()
        line = "[MISS] x [FAIL] y"
        issues = p.parse(line)
        assert len(issues) == 1
        assert "缺少文件" in issues[0]["label"]

    def test_has_issue_miss(self):
        p = self.make_parser()
        assert p.has_issue("[MISS] file") is True

    def test_has_issue_fail(self):
        p = self.make_parser()
        assert p.has_issue("[FAIL] err") is True

    def test_has_issue_detected(self):
        p = self.make_parser()
        assert p.has_issue("[检测到] pattern") is True

    def test_has_issue_term(self):
        p = self.make_parser()
        assert p.has_issue("使用了术语") is True

    def test_has_issue_confirm(self):
        p = self.make_parser()
        assert p.has_issue("需人确认") is True

    def test_has_issue_no_match(self):
        p = self.make_parser()
        assert p.has_issue("everything is fine") is False

    def test_parse_fallback_for_unparseable_content(self):
        p = self.make_parser()
        output = "[MISS] x\nsome garbage\n[FAIL] y"
        issues = p.parse(output)
        assert len(issues) == 2
