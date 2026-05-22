# TODO

## v0.1.x — 通过 examples/knowl 验证模型并完善细节

- [ ] **examples/knowl 自包含化** — 剥离外部 `app.*` 依赖，使用 `quanttide_audit` 模型
  - [ ] `models.py` — 精简，复用 `quanttide_audit` 模型，保留 knowl 特有类型
  - [ ] `parser.py` — 保留（knowl CLI 私有格式），改 imports
  - [ ] `report.py` — 保留（渲染逻辑），改 imports
  - [ ] `service.py` — 替换外部依赖为本地实现（tools/loader/config stubs）
  - [ ] `__init__.py` — 暴露 `run` 入口
  - [ ] 端到端验证：`python -c "from examples.knowl import run; run(...)"` 通过
- [ ] **细节完善**（基于验证反馈）
  - [ ] 模型字段补充
  - [ ] 边界情况处理

## 已完成

- [x] AuditCriteria 审计标准
- [x] AuditFinding 审计发现（解耦，包含 evidence 列表）
- [x] AuditEvidence 审计证据（location + detail）
- [x] AuditReport 审计报告（聚合 findings）
- [x] AuditSeverity / AuditStatus 枚举
- [x] 复用 base-toolkit 标准字段
