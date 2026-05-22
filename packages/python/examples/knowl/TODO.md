# examples/knowl 重构 TODO

目标：用工具包 `AuditReport` 替代 knowl 自造的 `Report`，剥离垃圾代码。

- [ ] **`models.py` — `AuditReport` 改名 `AuditIssues`**
      renamed 已经在用，正式改名避免混淆
- [ ] **`report.py` — 删掉 `Report` 类**
      `build()` / `render()` / `exit_code` 全部移除
- [ ] **`report.py` — 渲染改为纯函数**
      `render_report(report: AuditReport, mode, stats, diff, ...) -> None`
- [ ] **`report.py` — `ReportRepository` 改用 `AuditReport` 序列化**
      JSON 读写的对象从 knowl 类型换为 `AuditReport`
- [ ] **`service.py` — 编排逻辑适配**
      `AuditIssue` → `AuditFinding` 映射，`AuditReport` 构造
- [ ] **全量测试通过**
      87 + 39 = 126 ✅
