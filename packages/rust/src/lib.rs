//! 量潮审计工具箱（Rust）。
//!
//! 提供**不因平台而变**的审计领域数据模型：审计标准（`AuditCriteria`）、
//! 审计证据（`AuditEvidence`）、审计发现（`AuditFinding`）与审计报告（`AuditReport`）。
//! 一个聚合一个模块；各端（命令行、平台）向它对齐，不各写一份。
//!
//! 审计领域模型以 Python SDK（`packages/python`）为准；Rust 库与之同名同义。

pub mod criteria;
pub mod evidence;
pub mod finding;
pub mod report;

pub use criteria::*;
pub use evidence::*;
pub use finding::*;
pub use report::*;

/// 领域英文名。
pub const DOMAIN: &str = "audit";

/// 包版本（与 Cargo.toml 保持一致）。
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
