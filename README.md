# 交付门禁

一个中文优先、轻量、风险自适应的 Codex Skill。

它用于回答一个简单问题：当前结果是否已经可以交付？

## 使用

直接说：

```text
交付验收一下。
```

需要显式调用时：

```text
$delivery-gate 交付验收一下。
```

Skill 会优先给出 `通过`、`有条件通过` 或 `未通过`，随后只保留最关键的证据和下一步。

## 原则

- 普通任务只做可能改变结论的最少检查。
- 已有测试或 CI 能证明同一件事时不重复执行。
- 生产、资金、敏感数据、不可逆操作、证据冲突或测试失败时提高验证强度。
- 验收不自动授权修改、发布、部署或其他外部操作。

## 安装

让 Codex 从本仓库的 `delivery-gate` 目录安装到用户级 Skills 目录即可。已有同名目录时先保留备份，不静默覆盖。

仓库地址：<https://github.com/mingsp/delivery-gate>

## 开发

```bash
python -m unittest discover -s tests -p "test_*.py"
```

运行包只有 `SKILL.md`、OpenAI UI 元数据和图标，不包含自定义安装器、文件哈希清单或默认扫描脚本。

## 许可

本项目基于 [LB623/no-negative-echo](https://github.com/LB623/no-negative-echo) 的 MIT 许可版本二次开发，并保留原始版权与许可声明。
