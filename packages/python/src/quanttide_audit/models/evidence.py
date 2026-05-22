from pydantic import BaseModel
from quanttide import (
    CreatedAtField,
    DescriptionField,
    IdField,
    NameField,
    TitleField,
    UpdatedAtField,
)


class AuditEvidence(BaseModel):
    """审计证据：描述性证据。

    独立收集，不引用标准或发现，作为素材等待被标准检验。

    标识:
        id: 全局唯一标识（UUID）
        name: 证据唯一名称，slug 风格，如 "ev-main.py-42"
        title: 证据概要标题，如 "第42行超出长度限制"
    说明:
        description: 证据详细内容，如违规行原文或具体度量值
    时间追踪:
        created_at: 证据收集时间
        updated_at: 证据最后更新时间
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
