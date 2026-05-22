from pydantic import BaseModel
from quanttide import (
    CreatedAtField,
    DescriptionField,
    IdField,
    NameField,
    TitleField,
    UpdatedAtField,
)


class AuditCriteria(BaseModel):
    """审计标准：定义检查规则。

    作为"标尺"独立存在，不引用证据或发现。

    标识:
        id: 全局唯一标识（UUID）
        name: 标准唯一名称，slug 风格，如 "line-length"
        title: 标准可读标题，如 "行长度检查"
    说明:
        description: 规则详细说明，如 "每行不应超过 88 个字符"
    时间追踪:
        created_at: 标准创建时间
        updated_at: 标准最后更新时间
    """

    # 标识
    id: IdField
    name: NameField
    title: TitleField

    # 说明
    description: DescriptionField

    # 时间追踪
    created_at: CreatedAtField
    updated_at: UpdatedAtField
