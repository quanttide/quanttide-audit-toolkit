# quanttide-audit-toolkit Python SDK — 状态报告

## 当前范围

| 层 | 归属 | 状态 |
|:---|:-----|:----|
| `models` 模块（审计数据模型） | 工具包 `src/quanttide_audit/` | ✅ v0.1.0 |
| `examples/knowl`（知识库审计示例） | 消费者 `examples/knowl/` | ✅ 自包含，剥离 `app.*` 依赖 |

## 验收结果

| 检查项 | 结果 |
|:------|:----|
| API 可用 | ✅ 4 个模型 + 2 个枚举全部实现 |
| 标准字段复用 | ✅ IdField, NameField, TitleField, DescriptionField, CreatedAtField, UpdatedAtField |
| 模型关系 | ✅ Criteria → Finding(evidence) → Evidence; Report → Findings |
| 编译构建 | ✅ `hatchling build` 通过 |
| 类型标记 | ✅ `py.typed` 已放置 |
| 工具包测试 | ✅ 39 个，全部通过，覆盖率 100% |
| knowl 示例测试 | ✅ 87 个，全部通过 |
| knowl 端到端验证 | ✅ `run(data_dir=..., mode=full\|simple)` 正常输出审计报告 |

## 架构决策

| 决策 | 结论 |
|:----|:----|
| 审计运行器 | ❌ 不在工具包中抽象 —— 工具执行方式差异大，由消费者自行编排 |
| 输出解析器 | ❌ 不在工具包中抽象 —— CLI 格式是工具私有的，由消费者处理 |
| 报告渲染器 | ❌ 不在工具包中抽象 —— 复杂渲染由消费者实现，模型仅提供 `render()`/`to_json()` 轻量便利方法 |

## 已知问题

| # | 问题 | 状态 |
|---|------|------|
| 1 | 模型字段需基于 knowl 验证反馈完善（如 location 增强、evidence 关联） | 🟡 待 v0.1.x 迭代 |
| 2 | 边界情况与错误处理需补充 | 🟡 待 v0.1.x 迭代 |
