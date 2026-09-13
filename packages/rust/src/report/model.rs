use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::finding::AuditFinding;

/// 审计报告：聚合审计发现。
///
/// 只持有发现列表，每条发现自包含标准与证据。
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct AuditReport {
    /// 全局唯一标识。
    pub id: Uuid,
    /// 报告唯一名称，slug 风格。
    pub name: String,
    /// 报告可读标题。
    pub title: String,
    /// 报告补充说明，如审计范围、运行环境。
    #[serde(default)]
    pub description: Option<String>,
    /// 审计发现列表。
    #[serde(default)]
    pub findings: Vec<AuditFinding>,
    /// 报告创建时间。
    pub created_at: DateTime<Utc>,
    /// 报告最后更新时间。
    pub updated_at: DateTime<Utc>,
}
