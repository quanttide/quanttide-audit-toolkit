//! 量潮审计工具箱（Rust）。
//!
//! 提供**不因平台而变**的审计领域数据模型——审计标准（`AuditCriteria`）、
//! 审计证据（`AuditEvidence`）、审计发现（`AuditFinding`）与审计报告（`AuditReport`）。
//! 各端（命令行、平台）向它对齐，不各写一份。
//!
//! 审计领域模型以 Python SDK（`packages/python`）为准；Rust 库与之同名同义。
//! 领域模型就绪后在此按子领域分文件——现只有骨架：领域常量与版本导出。

/// 领域英文名。
pub const DOMAIN: &str = "audit";

/// 包版本（与 Cargo.toml 保持一致）。
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
