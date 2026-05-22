# quanttide-audit-toolkit

量潮审计工具箱，提供跨平台的审计领域数据模型。

## 包

| 平台 | 状态 | 路径 |
|------|------|------|
| Python | ✅ v0.1.0 | [packages/python](packages/python) |

## 数据模型

```
AuditFinding
  ├── criterion: AuditCriteria    # 被违反的标准
  └── evidence: AuditEvidence[]   # 触发该发现的证据

AuditReport
  └── findings: AuditFinding[]    # 审计发现列表
```

## 开发

参见各语言包目录下的 `README.md`。
