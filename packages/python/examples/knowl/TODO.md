# examples/knowl

所有中间商已清除。工具包模型直出直用。

- `models.py` — 删除（含 AuditIssue, AuditIssues, AuditDiff, KnowledgeBaseStats, AuditMode）
- `parser.py` — 直出 `list[dict]`
- `service.py` — 直出 `list[AuditFinding]`
- `report.py` — 只接 `AuditReport` + 元组
- 测试 90 通过，端到端 full/simple 正常
