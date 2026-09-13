# AGENTS.md - quanttide-audit Rust 库

## 项目结构

```
packages/rust/
├── AGENTS.md          # 本文件
├── CHANGELOG.md       # 版本变更记录
├── CONTRIBUTING.md    # 贡献指南
├── Cargo.toml         # Rust 包配置
├── README.md          # 项目说明
├── src/
│   ├── lib.rs         # 出口：领域常量、版本与四个聚合
│   ├── criteria/      # 审计标准
│   ├── evidence/      # 审计证据
│   ├── finding/       # 审计发现（含严重程度）
│   └── report/        # 审计报告
└── tests/
    ├── package.rs     # 领域常量与版本
    └── criteria.rs / evidence.rs / finding.rs / report.rs   # 各聚合的集成测试
```

一个聚合一个模块：模块内 `mod.rs` 声明、模型在 `model.rs`，`lib.rs` 重导出全部公共类型；新增聚合照此加一个模块与一份同名测试。

## 事实源

审计领域模型以 Python SDK（`../python`）为准；Rust 库只做表达，与之同名同义，不定义领域。
