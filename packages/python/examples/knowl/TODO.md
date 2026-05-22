# examples/knowl 重构 TODO

- [x] `models.py` — `AuditReport` 改名 `AuditIssues`
- [x] `report.py` — 删 `Report` 类，`render_report()` 纯函数
- [x] `service.py` — `_to_finding()` 映射，构造 `AuditReport`
- [x] 全量测试 84 + 39 = 123 通过

## 已完成优化

- [x] **预定义 Criteria 常量** — `_CRITERIA` 字典，5 种 group 各一个固定实例
- [x] **精简 `_to_finding()`** — 不再 new Criteria/Evidence，name 用 `{criterion.name}-{slug}`，evidence 默认空列表
