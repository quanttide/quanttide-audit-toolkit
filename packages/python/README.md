# quanttide-audit

量潮审计 Python SDK，基于量潮标准字段（`quanttide`）提供审计领域数据模型。

## 安装

```bash
pip install quanttide-audit
```

## 数据模型

```
AuditFinding
  ├── criterion: AuditCriteria    # 被违反的标准
  └── evidence: AuditEvidence[]   # 触发该发现的证据

AuditReport
  └── findings: AuditFinding[]    # 审计发现列表，每条自包含 criterion + evidence
```

| 模型 | 字段 | 标准字段类型 |
|------|------|-------------|
| `AuditCriteria` | id, name, title, description, created_at, updated_at | IdField, NameField, TitleField, DescriptionField, CreatedAtField, UpdatedAtField |
| `AuditEvidence` | id, name, title, description, created_at, updated_at | IdField, NameField, TitleField, DescriptionField, CreatedAtField, UpdatedAtField |
| `AuditFinding` | id, name, title, criterion, evidence[], description, severity, created_at, updated_at | IdField, NameField, TitleField, DescriptionField, CreatedAtField, UpdatedAtField |
| `AuditReport` | id, name, title, description, findings[], created_at, updated_at | IdField, NameField, TitleField, DescriptionField, CreatedAtField, UpdatedAtField |

- `AuditFinding.criterion` — 直接持有 `AuditCriteria` 对象引用
- `AuditFinding.evidence` — 直接持有 `AuditEvidence` 对象列表
- `AuditReport` 仅持有 `findings` 列表，每条 finding 自包含全部上下文
- `AuditSeverity` — MAJOR / MINOR / OBSERVATION，遵循 ISO 19011:2018

## 快速开始

```python
from uuid import uuid4
from quanttide_audit import (
    AuditCriteria, AuditEvidence, AuditFinding,
    AuditReport, AuditSeverity,
)

now = "2026-01-01T00:00:00"

criterion = AuditCriteria(
    id=uuid4(), name="line-length", title="Line length check",
    description="Lines should not exceed 88 characters",
    created_at=now, updated_at=now,
)

evidence = AuditEvidence(
    id=uuid4(), name="ev-1",
    title="Line 42 exceeds limit",
    description="Line has 92 chars, max is 88",
    created_at=now, updated_at=now,
)

finding = AuditFinding(
    id=uuid4(), name="f-1",
    criterion=criterion, evidence=[evidence],
    title="Line too long",
    severity=AuditSeverity.MAJOR,
    created_at=now, updated_at=now,
)

report = AuditReport(
    id=uuid4(), name="rep-1", title="Code Audit #1",
    findings=[finding],
    created_at=now, updated_at=now,
)
```

## 开发

```bash
uv sync --dev
uv run pytest --cov=src/
uv run ruff check src/ tests/
```
