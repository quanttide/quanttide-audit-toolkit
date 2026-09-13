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
│   └── lib.rs         # 出口：领域常量与版本（模型就绪后按子领域分文件）
└── tests/
    └── package.rs     # 集成测试
```

## 事实源

审计领域模型以 Python SDK（`../python`）为准；Rust 库只做表达，与之同名同义，不定义领域。
