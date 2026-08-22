# 安装交付门禁

从仓库 <https://github.com/mingsp/delivery-gate> 安装 `delivery-gate/` 目录。

## Codex

请让 Codex 使用内置 Skill 安装能力，把该目录安装到用户级 Skills 目录：

```text
请安装 https://github.com/mingsp/delivery-gate 中的 delivery-gate Skill。
```

已有同名目录时先保留可恢复备份，不静默覆盖用户修改。

安装后开启新任务，并确认技能列表中出现 `delivery-gate`。目录存在表示文件已复制，技能列表可见表示宿主已发现；实际使用时可直接说“交付验收一下”，或显式调用 `$delivery-gate`。

其他支持 Agent Skills 的宿主应安装到其官方用户级或项目级目录。无法确认发现机制时，只报告文件已复制，不声称已激活。
