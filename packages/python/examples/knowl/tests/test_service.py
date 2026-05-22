from quanttide_audit import AuditSeverity

from examples.knowl.service import run, _to_finding

_SAMPLE_FINDINGS = [
    ("• 缺少文件 ontologies.json", "运行 auto-fix 自动补全缺失文件", "文件结构问题", AuditSeverity.MINOR),
    ("• JSON 格式错误: instances.json 第 5 行缺少逗号", "修复对应 JSON 文件格式", "文件结构问题", AuditSeverity.MINOR),
    ("• 缺少文件 domain.json", "运行 auto-fix 自动补全缺失文件", "文件结构问题", AuditSeverity.MINOR),
    ("• 在 domain ontology 中使用了术语 深度学习", "在 domain.json 的 vocabulary 字段中补充该术语", "未定义术语", AuditSeverity.MAJOR),
    ("• 在 domain ontology 中使用了术语 知识图谱", "在 domain.json 的 vocabulary 字段中补充该术语", "未定义术语", AuditSeverity.MAJOR),
    ("• 引用不存在的实例 budget-2024", "确认该引用是否必要", "名称冲突或引用断裂", AuditSeverity.MAJOR),
    ("• 具体值 MySQL 应抽象为变量", "重构 ontologies.json 中的 pattern", "本体抽象度不足", AuditSeverity.OBSERVATION),
]


def _make_findings():
    return [_to_finding(label, action, group, sev) for label, action, group, sev in _SAMPLE_FINDINGS]


class TestRun:
    def test_full_mode(self, tmp_path):
        code = run(_make_findings(), mode="full", state_dir=tmp_path)
        assert code == 1

    def test_simple_mode(self, tmp_path):
        code = run(_make_findings(), mode="simple", state_dir=tmp_path)
        assert code == 1

    def test_invalid_mode(self, tmp_path):
        code = run([], mode="unknown", state_dir=tmp_path)
        assert code == 1

    def test_clean_report(self, tmp_path):
        code = run([], mode="full", state_dir=tmp_path)
        assert code == 0
