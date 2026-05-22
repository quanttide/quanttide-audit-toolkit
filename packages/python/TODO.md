# TODO

## v0.1.x — 通过 examples/knowl 验证模型并完善细节

- [ ] **审计运行器** — 执行检测工具并解析结果为模型实例
  - [ ] 定义 `AuditRunner` 接口（invoke → list[AuditFinding]）
  - [ ] 实现 ruff/lizard 等代码分析工具的 runner
  - [ ] knowl 场景：对接知识库检测工具的 runner
  - [ ] `ToolOutputParser` 重构：输出 → AuditFinding 映射
- [ ] **报告渲染器** — 将 AuditReport 输出为可读格式
  - [ ] 终端输出（`report.render()` → stdout）
  - [ ] Markdown 渲染
  - [ ] JSON 序列化
  - [ ] Diff 比较（增量审计）
- [ ] **examples/knowl 适配** — 使用 quanttide_audit 模型而非 `app.*`
  - [ ] 模型替换：AuditIssue → quanttide_audit 对应模型
  - [ ] 服务重构：service.py 依赖注入 quanttide_audit 组件
  - [ ] 端到端验证：运行 knowl 示例通过
- [ ] **细节完善**（基于验证反馈）
  - [ ] 模型字段补充（如 location 增强、evidence 关联）
  - [ ] 枚举扩展（如新增 AuditStatus）
  - [ ] 错误处理与边界情况

## 已完成

- [x] AuditCriteria 审计标准
- [x] AuditFinding 审计发现（解耦，包含 evidence 列表）
- [x] AuditEvidence 审计证据（location + detail）
- [x] AuditReport 审计报告（聚合 findings）
- [x] AuditSeverity / AuditStatus 枚举
- [x] 复用 base-toolkit 标准字段
