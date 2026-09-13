# quanttide-audit

量潮审计 Rust SDK，提供跨平台的审计领域数据模型。

## 安装

在 `Cargo.toml` 中添加：

```toml
[dependencies]
quanttide-audit = "0.1.0"
```

## 使用

```rust
use quanttide_audit::{DOMAIN, VERSION};

println!("{DOMAIN} v{VERSION}");
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
