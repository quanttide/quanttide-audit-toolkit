use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// 审计标准：定义检查规则。
///
/// 作为「标尺」独立存在，不引用证据或发现。
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct AuditCriteria {
    /// 全局唯一标识。
    pub id: Uuid,
    /// 标准唯一名称，slug 风格，如 `line-length`。
    pub name: String,
    /// 标准可读标题，如「行长度检查」。
    pub title: String,
    /// 规则详细说明，如「每行不应超过 88 个字符」。
    pub description: String,
    /// 标准创建时间。
    pub created_at: DateTime<Utc>,
    /// 标准最后更新时间。
    pub updated_at: DateTime<Utc>,
}
