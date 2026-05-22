# 变更记录

## [0.1.0] - 2026-05-22

### 新增

- `AuditCriteria` — 审计标准（id, name, title, description, created_at, updated_at）
- `AuditEvidence` — 审计证据（id, name, title, description, created_at, updated_at）
- `AuditFinding` — 审计发现，直接持有 criterion（AuditCriteria）和 evidence（list[AuditEvidence]）对象引用
- `AuditReport` — 审计报告，仅持有 findings 列表，每条 finding 自包含全部上下文
- `AuditSeverity` — MAJOR / MINOR / OBSERVATION，遵循 ISO 19011:2018
- 所有模型使用 `quanttide` 标准字段（IdField, NameField, TitleField, DescriptionField, CreatedAtField, UpdatedAtField）
- 测试 39 个，覆盖率 100%
