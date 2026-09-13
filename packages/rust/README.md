# quanttide-audit

量潮审计 Rust SDK，提供跨平台的审计领域数据模型。

## 模块

| 模块 | 说明 |
|------|------|
| `criteria` | 审计标准：id, name, title, description, created_at, updated_at |
| `evidence` | 审计证据：id, name, title, description, created_at, updated_at |
| `finding` | 审计发现：criterion, evidence[], description, severity, id, name, title, created_at, updated_at |
| `report` | 审计报告：findings[], description, id, name, title, created_at, updated_at |

`severity` 取 `major` / `minor` / `observation`，遵循 ISO 19011:2018。

## 安装

在 `Cargo.toml` 中添加：

```toml
[dependencies]
quanttide-audit = "0.1.0"
```

## 使用

```rust
use quanttide_audit::{AuditCriteria, AuditEvidence, AuditFinding, AuditReport, AuditSeverity};
```

## 开发

```bash
cargo test --locked
cargo fmt --check
cargo clippy --all-targets -- -D warnings
```

## 发布

打 `rust/v0.1.0` 标签推送到远端，由 `publish-rust.yml` 校验版本并发布到 crates.io。

## 许可

Apache-2.0
