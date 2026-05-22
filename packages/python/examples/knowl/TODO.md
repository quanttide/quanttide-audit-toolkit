# examples/knowl 重构 TODO

目标：用工具包 `AuditReport` 替代 knowl 自造的 `Report`，剥离垃圾代码。

- [x] **`models.py` — `AuditReport` 改名 `AuditIssues`**
- [x] **`report.py` — 删掉 `Report` 类**
- [x] **`report.py` — 渲染改为纯函数 `render_report()`**
- [x] **`report.py` — `ReportRepository.save_report()` 接受 `AuditReport` + `AuditIssues`**
- [x] **`service.py` — `AuditIssue` → `AuditFinding`，`AuditReport` 构造**
- [x] **全量测试通过：84 + 39 = 123**
