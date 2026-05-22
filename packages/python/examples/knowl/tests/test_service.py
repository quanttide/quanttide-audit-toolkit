import re
from uuid import uuid4

from quanttide_audit import AuditFinding, AuditReport, AuditSeverity, AuditCriteria

from examples.knowl.service import run

TS = "2026-01-01T00:00:00"

_CRITERIA_UUIDS = {
    "file-structure": "11111111-1111-1111-1111-111111111111",
    "undefined-terms": "22222222-2222-2222-2222-222222222222",
    "name-conflict": "33333333-3333-3333-3333-333333333333",
    "abstraction-level": "44444444-4444-4444-4444-444444444444",
    "cross-domain-coverage": "55555555-5555-5555-5555-555555555555",
}

_CRITERIA = {
    "文件结构问题": AuditCriteria(
        id=_CRITERIA_UUIDS["file-structure"], name="file-structure", title="文件结构检查",
        description="检查知识库文件结构是否完整", created_at=TS, updated_at=TS,
    ),
    "未定义术语": AuditCriteria(
        id=_CRITERIA_UUIDS["undefined-terms"], name="undefined-terms", title="未定义术语检查",
        description="检测领域本体中使用了未在 vocabulary 中定义的术语", created_at=TS, updated_at=TS,
    ),
    "名称冲突或引用断裂": AuditCriteria(
        id=_CRITERIA_UUIDS["name-conflict"], name="name-conflict", title="名称冲突与引用断裂检查",
        description="检测领域间名称冲突和悬挂引用", created_at=TS, updated_at=TS,
    ),
    "本体抽象度不足": AuditCriteria(
        id=_CRITERIA_UUIDS["abstraction-level"], name="abstraction-level", title="本体抽象度检查",
        description="检测具体值应抽象为变量的情况", created_at=TS, updated_at=TS,
    ),
    "跨领域关系覆盖率": AuditCriteria(
        id=_CRITERIA_UUIDS["cross-domain-coverage"], name="cross-domain-coverage", title="跨领域关系覆盖率",
        description="检测跨领域关系的覆盖程度", created_at=TS, updated_at=TS,
    ),
}

_SAMPLE_DEFS = [
    ("• 缺少文件 ontologies.json", "运行 auto-fix 自动补全缺失文件", "文件结构问题", AuditSeverity.MINOR),
    ("• JSON 格式错误: instances.json 第 5 行缺少逗号", "修复对应 JSON 文件格式", "文件结构问题", AuditSeverity.MINOR),
    ("• 缺少文件 domain.json", "运行 auto-fix 自动补全缺失文件", "文件结构问题", AuditSeverity.MINOR),
    ("• 在 domain ontology 中使用了术语 深度学习", "在 domain.json 的 vocabulary 字段中补充该术语", "未定义术语", AuditSeverity.MAJOR),
    ("• 在 domain ontology 中使用了术语 知识图谱", "在 domain.json 的 vocabulary 字段中补充该术语", "未定义术语", AuditSeverity.MAJOR),
    ("• 引用不存在的实例 budget-2024", "确认该引用是否必要", "名称冲突或引用断裂", AuditSeverity.MAJOR),
    ("• 具体值 MySQL 应抽象为变量", "重构 ontologies.json 中的 pattern", "本体抽象度不足", AuditSeverity.OBSERVATION),
]


def _slug(text):
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)[:48]


def _to_finding(label, action, group, severity):
    criterion = _CRITERIA[group]
    return AuditFinding(
        id=uuid4(),
        name=f"{criterion.name}-{_slug(label)[:40]}",
        title=label,
        criterion=criterion,
        evidence=[],
        severity=severity,
        description=action or None,
        created_at=TS,
        updated_at=TS,
    )


def _make_findings():
    return [_to_finding(*d) for d in _SAMPLE_DEFS]


class TestRun:
    def test_full_mode(self):
        report = run(_make_findings(), mode="full")
        assert isinstance(report, AuditReport)

    def test_simple_mode(self):
        report = run(_make_findings(), mode="simple")
        assert isinstance(report, AuditReport)

    def test_invalid_mode(self):
        import pytest
        with pytest.raises(ValueError):
            run([], mode="unknown")

    def test_clean_report(self):
        report = run([], mode="full")
        assert report.findings == []

    def test_findings_present(self):
        report = run(_make_findings(), mode="full")
        assert len(report.findings) == 7
