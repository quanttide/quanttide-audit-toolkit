# examples/knowl 尚存问题

## 行为倒灌进模型

`AuditIssues` 的 `exit_code` / `is_clean` / `section_groups` 是渲染逻辑，不应放在数据类上。移到渲染函数中内联处理。

## 为传递数据造类型

`_PreviousAudit` 和 `IssueGroup` 只是 2-3 字段的聚合，应该用元组或直接拆开传，不需要声明类。

## 把配置声明成框架

`ReportTemplate` + 方法 `sections_for()` / `tail_for()` 过度设计。用 plain dict + 内联逻辑即可。
