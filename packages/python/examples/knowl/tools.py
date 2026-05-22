_SAMPLE_OUTPUT = {
    "validate": """\
=== engineering ===
[MISS] ontologies.json
[FAIL] JSON 格式错误: instances.json 第 5 行缺少逗号
=== finance ===
[MISS] domain.json
""",
    "find-undefined-terms": """\
=== engineering ===
在 domain ontology 中使用了术语 "深度学习"
在 domain ontology 中使用了术语 "知识图谱"
""",
    "fusion-check": """\
=== finance ===
【需人确认】引用不存在的实例 "budget-2024"
""",
    "check-abstraction": """\
=== engineering ===
[检测到] 具体值 "MySQL" 应抽象为变量
""",
    "cross-domain-report": """\
=== engineering ===
跨领域关系覆盖率: 65%
=== finance ===
跨领域关系覆盖率: 42%
""",
}


class _FakeTool:
    def __init__(self, name: str):
        self.name = name

    def execute(self, inp: dict) -> str:
        return _SAMPLE_OUTPUT.get(self.name, "")


def all_detection_tools(mode: str):
    return [
        _FakeTool("validate"),
        _FakeTool("find-undefined-terms"),
        _FakeTool("fusion-check"),
        _FakeTool("check-abstraction"),
        _FakeTool("cross-domain-report"),
    ]
