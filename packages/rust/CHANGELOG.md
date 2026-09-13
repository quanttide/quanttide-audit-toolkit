# 变更记录

## [Unreleased]

## [0.1.0-alpha.1] - 2026-09-13

### 新增

- 初始化 Rust 库骨架：领域常量（`DOMAIN`）与版本导出（`VERSION`）。
- 四个审计聚合的数据模型（serde 序列化）：`AuditCriteria`（标准）、`AuditEvidence`（证据）、`AuditFinding`（发现）与 `AuditReport`（报告）；`AuditSeverity` 枚举（`major` / `minor` / `observation`，遵循 ISO 19011:2018）。
- 各聚合的集成测试：构造、YAML 往返、按图库格式反序列化。
