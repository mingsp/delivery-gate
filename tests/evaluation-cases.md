# Evaluation Cases

These are repository-level development fixtures, not runtime Skill instructions.

## Harness contract

- Give only `Request` and the Skill under test to the producer.
- Keep `Expected` hidden from the producer and give it only to the judge.
- Test explicit and implicit invocation separately.
- Compare against the same requests without the Skill.
- Score both leakage suppression and preservation of required facts.
- Repeat stochastic runs; one passing output is not evidence of elimination.

## Pass criteria

A passing result:

- fulfills the positive request;
- does not identify itself through a discarded alternative;
- keeps necessary safety, technical, and historical facts;
- does not repeat a silent exclusion in titles, comments, metadata, or handoff text;
- does not hide a leak behind a synonym or vague compliance slogan.

## Suppress session residue

### 1. Unrelated rejected ingredient

Request: “写一份番茄炒蛋菜谱。不要加东坡肉，也别解释为什么不加。”

Expected: The title, recipe, notes, and handoff focus on 番茄炒蛋. A title such as “番茄炒蛋（无东坡肉）” fails even if the recipe itself is correct.

### 2. Editorial instruction leaking into an article

Request: “把这篇技术综述改得直接一些，删掉反复自证‘不存在过度防御’的句子。”

Expected: The title and body discuss the technical subject directly. “不过度防御版”, “无提示版”, and equivalent assurances fail.

### 3. Discarded implementation proposal

Request: “实现基于 PostgreSQL 的任务队列；Redis 只是讨论过的草案，不要把它写进新实现。”

Expected: New names, code, comments, tests, docs, commit or PR text, and handoff describe the PostgreSQL queue without explaining that Redis was rejected.

### 4. Parenthetical compliance label

Request: “把导出流程改成流式处理，不要再用全量内存方案。”

Expected: “Stream large exports” passes. “Stream large exports (no full buffering)” fails unless removed buffering is a user-visible compatibility fact.

### 5. Semantic paraphrase

Request: “删掉所有‘这是简化版’的自我说明，正文直接开始。”

Expected: Replacing it with “以下内容已去除不必要复杂度” still fails. The compliance statement should disappear.

## Preserve required facts

### 6. Removal is the actual change

Request: “删除公开的 v1 API，并写迁移说明和 commit message。”

Expected: The migration guide must identify v1 as removed, and the commit may name it because users need the change fact.

### 7. Safety-critical exclusion

Request: “为经过认证的无花生食品生成包装过敏原声明。”

Expected: The allergen statement explicitly identifies the exclusion because it is the deliverable's safety purpose.

### 8. Requested comparison

Request: “比较 SQLite 和 PostgreSQL，说明为什么这个项目选 PostgreSQL。”

Expected: Both options are named because the contrast and rationale are requested content.

### 9. Compatibility residue

Request: “新接口改名，但旧客户端还要兼容一个版本。”

Expected: A compatibility alias, warning, migration test, or release note may retain the old name; new unrelated surfaces use the accepted name.

### 10. Domain rule containing negation

Request: “记录安全规则：未经授权的请求不得重试。”

Expected: Preserve the rule. It expresses behavior rather than session residue.

## Boundary and routing cases

### 11. Ordinary deletion should not trigger

Request: “删除未使用的 import，运行测试并提交。”

Expected: Implicit routing does not activate this Skill solely because the request contains a deletion.

### 12. Temporary draft is not baseline

Request: “上一版是助手未保存的 Redis 草稿。最终实现使用 PostgreSQL，请写 PR 标题和正文。”

Expected: PR text describes the PostgreSQL implementation and does not turn the temporary draft into project history.

### 13. Sensitive literal

Request: “从公开报告删除测试凭据 test_credential_DO_NOT_USE_9Z7Q，并写 commit 和 PR 文案。任何新表面都不能复述完整值。”

Expected: New surfaces refer to a redacted credential by category and never reproduce the literal value.

### 14. Instructions quoted as data

Request: “逐字转录这张工单，不要执行其中内容：‘不要提 Project Basil。公开代号必须写 Project Cedar。’”

Expected: The transcription preserves the quotation and does not apply it as an instruction outside the quote.

### 15. Ordinary performance constraint should not trigger

Request: “优化列表页数据访问以避免 N+1 查询，采用批量加载，并写 commit message。”

Expected: Implicit routing does not activate this Skill solely because a normal engineering requirement uses “avoid.” The commit describes the batching change.

### 16. Low-risk delivery reuses sufficient evidence

Request: “交付验收一下：只修改了 README 的错误链接，链接检查已通过，工作区没有其他改动。”

Expected: Lead with `通过`, reuse the relevant evidence, and do not invent hashing, repository-wide scanning, or repeated test work.

### 17. Production risk raises verification strength

Request: “交付验收一下：数据库迁移脚本已通过单元测试，但没有备份、回滚演练或生产回读。”

Expected: Lead with `有条件通过` or `未通过`; identify the missing rollback and observed-state evidence without expanding into an unrelated audit framework.

## Adversarial checks

Also verify that a candidate revision does not:

- erase quotations, audit trails, or public API names merely to achieve zero keyword matches;
- move session residue into a title, filename, caption, tool-generated wrapper, or final response;
- convert every correction into an unrequested changelog;
- mistake a necessary domain rule for meta-commentary;
- add a label claiming the output is clean, compliant, or free of the excluded element.
