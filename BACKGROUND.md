# 项目背景：此地无银三百两

> 调研日期：2026-08-21
> 范围：X / GitHub / Hacker News / 论文与官方 prompting 文档 / 已公开的 AGENTS.md 与 skills
> 未覆盖：小红书 OpenCLI 登录墙（`AUTH_REQUIRED`）；Reddit OpenCLI 返回非 JSON；B 站与 V2EX 当日无对应讨论（原帖仅传播约 24 小时）

编码 Agent 会把**已经被否决的方案、会话里的纠正、负向约束本身**写进最终产物。代码已经是番茄炒蛋，标题、注释、commit、PR 和文章却还在反复声明「无东坡肉」。本仓库要做的，是一个可发布的 skill：让最终交付物看起来像成品，而不是一份带否定句的复盘。

---

## 1. 发起人遇到的三种形态

这不是抽象的「注释太多」，而是同一类泄漏在三个表面上的表现。

| # | 表面 | 发起人原话 | 泄漏的东西 |
|---|------|------------|------------|
| 1 | Codex 实现 / 注释 / 说明 | 「经常出现反复强调被淘汰的方案」 | 会话里试过又丢掉的路径 |
| 2 | Git 历史 | 最常手改的 commit message 叫「移除此地无银三百两」 | 提交说明在讲过程，不在讲结果 |
| 3 | 长文 / 综述 | 写「不过度防御」的文章，正文反复声明「本文不存在过度防御」，删完之后题目变成「xxxx综述----不过度防御且无提示版」 | 负向约束被写进标题 |

第三种尤其致命：用户已经明确说「这次我会将这些去掉」，模型同意（「SB你为什么写出来？哦，你说得对」），然后用**更显眼的否定句**证明自己听话了。

这就是本项目要打的点：不是「少写字」，而是 **最终产物不得回放被否决的内容和负向指令本身**。

---

## 2. 现象叫什么

中文圈已经有一个稳定的隐喻。2026-08-20，[@songkeys](https://x.com/songkeys/status/2090416137720999992) 把 GPT-5.6 的这个习惯写成了一道菜：

> gpt 5.6 最让我受不了的就是：
> 我让它做一盘番茄炒蛋，它往里还加了东坡肉。
> 我说有必要加东坡肉吗？它说你说得对，然后把东坡肉去掉。
> 我说好，你提 PR 吧。再一看，它 PR 写着「番茄炒蛋（无东坡肉）」并且注释里会写一大堆为什么本道菜不需要加东坡肉。

截至 2026-08-21 取样：

- 8,540 likes / 774 转发 / 224 引用 / 456 回复 / 1,333 收藏 / **75 万次浏览**
- 用户提供的截图来自小红书转载（小红书号 `6989937046`，标注 14.2 万查看次数）

它同时踩中四个独立故障：

1. **范围失控**：没要的东西先进来（东坡肉）。
2. **谄媚式同意**：用户一问，立刻「你说得对」，删掉。
3. **负向回声**：删完以后，标题用「（无东坡肉）」证明自己删过。
4. **过程残留**：注释里写下「为什么不需要」——把会话过程固化进仓库。

后续引用把这个笑话补全了。[@Nakotango](https://x.com/Nakotango/status/2090485305719902543)：

> 我：不需要强调东坡肉
> GPT：好的，后面我都不会再提东坡肉的事情
> 注释：这里不能提东坡肉

[@hd_nvim](https://x.com/hd_nvim/status/2090443732566884560)（213 likes）：

> 还要在注释里解释，这里不需要加酱油，之前加过的酱油我是怎么倒掉的，顺便论述下酱油对东坡肉重要，但是番茄炒蛋不需要

[@lian75864](https://x.com/lian75864/status/2090463883840422072)：

> Claude还在注释里写为什么不需要加东坡肉

[@laverya](https://x.com/laverya/status/2090470510660288566)（253 likes）直接点破这是跨语言问题：

> So I see it's not just the English world that has this problem

本 skill 的英文名 `no-negative-echo` 对应的就是第 3、第 4 步：负向约束和被淘汰方案，不能在交付物里再响一次。

---

## 3. 证据：这不是一个人的洁癖

### 3.1 中文 Codex / Claude Code 用户已经在写规则，也已经在写 skill

原帖发出约 3 小时后，[@Nominatiivi](https://x.com/Nominatiivi/status/2090464250573779338)（415 likes，458 bookmarks）贴出自己的 `AGENTS.md`：

> 我的做法是在 AGENTS.md 写明：注释只写 non-obvious reason，禁止保留 intermediate attempts；PR 描述只写最终行为，diff 里看不出来的取舍以及从未合入的状态一律不要提及
> https://github.com/liby/dotfiles/blob/main/dot_codex/AGENTS.md

对应源码原文：

> A comment states the non-obvious reason at the owning boundary. […] Do not restate the operation, **preserve intermediate attempts**, or list speculative future work.
> PR/MR text states the **final behavior** and only the material rationale or trade-off a reviewer cannot recover from the diff.

这条规则当天就被复述并复制：

- [@coder_left](https://x.com/coder_left/status/2090637888543486311) 二次传播：「让它做一盘番茄炒蛋，它往里还加了东坡肉；让他不做东坡肉，他会特地声明番茄炒蛋（无东坡肉）」
- [`southliu/south-admin-react/AGENTS.md`](https://github.com/southliu/south-admin-react/blob/main/AGENTS.md) 第 6 条几乎逐字拷贝：

  > 注释只写 non-obvious reason，禁止保留 intermediate attempts；PR/提交描述只写最终行为，diff 里看不出来的取舍与从未合入的状态一律不提。

Amazon Rufus 的 applied scientist [@lawhy_X](https://x.com/lawhy_X/status/2090641896611922103) 的反应，几乎是本项目的产品陈述：

> exactly 不管用cc还是codex都是老把一大堆莫名其妙的解释放code里 防不胜防 **还得写skill去清docstring/comment**

另一条独立吐槽证明「此地无银」已经是 Codex 用户的口头禅。[@fenny521](https://x.com/fenny521/status/2088558374371926187)（2026-08-15，早于番茄炒蛋帖）：

> 有时候真的会被codex气笑
> 我：要求隐藏ssh登录相关命令
> […]
> 我：……哥你这不是此地无银三百两吗

### 3.2 英文圈：官方级仓库已经把这条写成硬规则

[`astral-sh/ruff`](https://github.com/astral-sh/ruff)（约 4.9 万 star，Python 工具链事实标准）的 [`AGENTS.md`](https://github.com/astral-sh/ruff/blob/main/AGENTS.md)：

> Do not mention discarded alternatives, intermediate edits, private instructions, tool usage, branch or draft status, local test commands, or session history unless the reader needs that information to understand the final result. **Do not describe reverted changes as part of the final change.**
> Preserve useful human-written comments […] Before finishing, reread each changed artifact as someone with **no access to the Codex session** and remove or explain anything that would surprise or confuse that reader.

同类规则已经散落在个人 harness 里，说明这是被反复踩出来的，不是一家的风格偏好：

| 仓库 | 原文 |
|------|------|
| [casivaagustin/dotfiles `global.md`](https://github.com/casivaagustin/dotfiles/blob/main/agents-rules/agents-rules/global.md) | `Do not mention discarded approaches.` / `Do not describe what was not done.` |
| [DieInTyo/screen-switch `AGENTS.md`](https://github.com/DieInTyo/screen-switch/blob/main/AGENTS.md) | `Commit text must describe the final diff, not the assistant's turn-by-turn activity. Do not describe temporary intermediate attempts that are no longer present in the final diff.` |
| [OktayCopurlu/ai-shared `applying-coding-style`](https://github.com/OktayCopurlu/ai-shared/blob/main/skills/applying-coding-style/SKILL.md) | `"Why not" comments — don't explain why you didn't choose an alternative approach` |
| [hivemq/hivemq-edge `AI_MANDATORY_RULES.md`](https://github.com/hivemq/hivemq-edge) | `NO EXCUSES: Don't explain why you didn't do it, just do it now` |

ruff 那条尤其重要：它把「读者没有 Codex 会话」写成验收标准。发起人的手改 commit「移除此地无银三百两」，就是在补这条验收。

### 3.3 Claude Code 官方 issue：注释在泄漏会话，规则压不住

[`anthropics/claude-code#65961`](https://github.com/anthropics/claude-code/issues/65961)
标题：`[MODEL] Claude verbose code comments by default — ignores instructions to stop.`
状态：open；**+1 = 136**；报告模型含 Opus 4.8 / Opus 5 / Sonnet 5。

报告原文：

> The comments are mostly redundant, restating what the adjacent code already makes obvious or simply **making references to the chat with Claude itself, leaking its chain of thoughts**.

关键评论（节选）：

> I don't see why it should ever write something like **"removed X because of Y ..."**
> Another annoying thing is all the references to **"phases"** when using the plan mode in code comments. These comments never make sense after completion […] and merely describe **intermediary implementation steps**.
> — [ArthurVanRemoortel](https://github.com/anthropics/claude-code/issues/65961)

> I have to do **"comment review" passes** to remove most of them. I have instructions in CLAUDE.md, in skills and in memory. Opus mostly ignores these instructions.
> — MarcEspiard

> I tracked LOC and comments per PR and roughly **17% diff is just comments** before I ask to condense it during review.
> — sudopower

同一条 issue 下有人解析了 464 个本地 session + git 历史（addisonlynch）：

- 注释密度随 session 深度上升：11–30 次 tool call 时 comment 占比 12.1%；81–200 次升到 16.3%；≥8 行长注释块从每千行 0.82 涨到 4.20。
- 长注释里带内部 issue ID 的比例从 8% 涨到 33%。内容典型是「过往回归叙事」——**本该写在 commit message 里的东西，被写进了最近的源文件**。
- 255 个 ≥8 行注释块中，121 个（47%）跨多次 commit 叠出来；有一个 38 行块叠了 14 次 commit，**从来没有段落被删掉**。
- A/B：把 rationale 写进 prompt 不会催出注释；旁边已经有 16 行注释块时，同样的编辑会再加 3 行。指向系统提示里的 **「match surrounding comment density」无上限**，一旦脏了就只增不减。

相关 issue 把问题拆得更干净：

- [#85130](https://github.com/anthropics/claude-code/issues/85130)（open）：`Keep development history out of code comments/docstrings by default (put it in git, not the file)` —— 和「移除此地无银三百两」是同一诉求。
- [#61305](https://github.com/anthropics/claude-code/issues/61305)：`Generated code ignores repeated zero-comment instructions`
- [#58600](https://github.com/anthropics/claude-code/issues/58600)：请求内置 Terse output style
- [#65302](https://github.com/anthropics/claude-code/issues/65302)：请求对非技术注释做 lint / filter

结论：这已被厂商 issue tracker 当成 **model 默认行为**，不是提示词没写好这么简单。

### 3.4 Hacker News / X：从 2025 年就开始抱怨，2026 年仍在手工清

2025-05，HN 在讨论 Cursor / Claude Code 落地时已经把这当成「最让 agent 代码变丑的东西」：

> The most common thing that makes agentic code ugly is the **overuse of comments**.
> — [news.ycombinator.com/item?id=43929768](https://news.ycombinator.com/item?id=43929768)（父帖 [Notes on rolling out Cursor and Claude Code](https://news.ycombinator.com/item?id=43927914)）

同帖：

> Gemini 2.5 pro […] There are comments for nearly every line and it's like it's **thinking out loud in comments**
> if you give it small corrections it will leave nonsensical comments **referring to your small correction as if it's something everyone knows**. […] if you do corrections during development mode it does that silly thing where it **leaves comments referring to your corrections**.
> — [HN 47310225](https://news.ycombinator.com/item?id=47310225) 一带讨论

2026-07-28，HN 专帖 [Claude's code comments – too much or just enough?](https://news.ycombinator.com/item?id=49078710)：

> directed Claude to never leave comments unless strictly necessary
> Too much for sure, and **often ignores instructions** to not leave obvious comments.
> LLMs have a bad habit of **commenting like a tutorial**.

X 上同一周的工程师原话：

- [@housecor](https://x.com/housecor/status/2085125584615821723)（87 likes，1.5 万浏览）：Claude 5 注释过多，原因是新系统提示 `match its comment density`；代码一旦已经注释密集，新代码会跟着密。
- [@lucianghinda](https://x.com/lucianghinda/status/2080933682039394322)：`Excessive comments: All agents, especially Claude […] I created a skill specifically to remove most of them and still got a lot more than I would have expected in the final PR that I needed to manually delete.`
- [@lucianghinda](https://x.com/lucianghinda/status/2090139232014938210)（2026-08-19）：Opus 5 之后「too much slop (too many comments, too much complexity)」
- [@Love2Code](https://x.com/Love2Code/status/2087196528628699185)（176 likes）：`one of the biggest flaws in LLMs right now is how they can't help overexplain and overcomment`
- [@thingslist](https://x.com/thingslist/status/2089948825456976109)：`Hacker News is complaining today that AI writes too many comments in code. Nobody posted a fix.` 然后贴了自己的 `CLAUDE.md`。

OpenAI 自己也承认过这个方向。GPT-5 prompting guide 写 Cursor 的调参经验：模型会产出 **verbose status updates and post-task summaries**，打断使用流；代码工具调用里的实现又偏 telegraph。这是官方确认的「过程叙述泄漏到用户可见层」。

---

## 4. 机制：为什么「你说得对，我删掉」之后还会写出来

下面几条互相加强，不是单点 bug。

### 4.1 负向词仍然被注意（粉红大象）

告诉模型「不要提 X」，等于把 X 放进当前激活。Reddit `r/ClaudeCode` 有用户把这个写成规则文件的反模式：

> “Don't mention the lawsuit” puts “lawsuit” into the active context exactly as much as “mention the lawsuit” does. The word is now primed.

这直接解释发起人的第三种形态：文章删掉所有「不过度防御」之后，标题变成「不过度防御且无提示版」。否定句本身成了新的东坡肉。

对 skill 作者的硬约束：**不要在会进入模型输出的指令里反复点名禁词。** 写「最终产物长什么样」，不要写一篇「禁止清单」让它对着念。

### 4.2 谄媚式同意 + 证明自己听话

songkeys 原帖的中间步是标准 sycophancy：用户质疑 → 「你说得对」→ 删除。RLHF 同时奖励「承认错误」和「展示已纠正」。最便宜的展示方式，就是在标题、注释、commit 里把被删的东西再写一遍。

Nakotango 的三段对话是这个机制的最小复现。

### 4.3 多方案推理会留下被丢掉的枝

[arXiv:2608.01347](https://arxiv.org/abs/2608.01347) *Same Task, Different Work: Prompt-Induced Waste in Coding Agents*（2026-08，4,644 次有效 run）：

> Multiple approaches increases reasoning by **2.4× to 7.4×** […] and creates about **three elaborated but discarded solution branches**, while still yielding only one implemented solution and **no success gain**.

Agent 在内部展开了被淘汰方案。如果没有一条「最终产物只描述现存 diff」的闸门，这些枝会漏进注释、PR 和 commit。这就是发起人说的「反复强调被淘汰的方案」。

### 4.4 系统提示在奖励「像周围代码」和「像教程」

Cory House 指出 Claude 5 系统提示要求 match comment density。GitHub #65961 的 A/B 验证了：脏邻居比「把 rationale 写进 prompt」更能催出注释。HN 则指出训练语料里教程注释（解释 *what*）过密，模型按教程风格注释生产代码。

两者叠加的结果：过程叙述一旦写进文件，就会被后续编辑当成风格，继续长。

### 4.5 有价值的「why not」和垃圾「why not」被模型搞混

[@traits_reality](https://x.com/traits_reality/status/2089628021049164047)：

> actually, humans do this. the best code comments are the ones that answer 'why not?' […] the problem ime is that LLMs try to mimic this but do so **inappropriately due to lack of long-term context + bad RL**

ADR 文献也认为「被拒绝的替代方案」是该持久化的知识，但家在 `docs/adr/`，不在函数上方、不在 PR 标题里、不在综述标题里。本 skill 必须切开：

- **保留**：维护者以后会踩的、从 diff 看不出来的不变量（「Safari 在 iframe 里没有 ResizeObserver」）。
- **删除**：本会话试过、用户否决、从未合入、只对当时聊天有意义的否定句。

---

## 5. 现有缓解为什么不够，所以才做可发布 skill

| 做法 | 证据 | 失败方式 |
|------|------|----------|
| 在 `AGENTS.md` / `CLAUDE.md` 写「少写注释 / 不要提被淘汰方案」 | ruff、liby/dotfiles、south-admin-react、Cory House 的旧 prompt | #65961：规则 + memory + hooks 仍压不住；「Don't mention X」会 priming X |
| 事后再开一个「清注释」skill | Yuan He、Lucian Ghinda | 清完仍有残留，还要手删；commit / PR / 文章标题不在清注释范围内 |
| 人手改 commit message | 发起人最高频手改：「移除此地无银三百两」 | 不可规模化，且只覆盖 git 文案 |
| 等模型厂商改默认 | #65961 仍 open，+136；#85130 仍 open | 默认行为被当成产品问题挂了两个月以上，用户不能等 |

缺口很清楚：

1. 覆盖面不能只是代码注释。要同时管 **代码注释、docstring、commit、PR 标题/正文、文档/综述标题和开篇**。
2. 不能靠点名禁词。skill 自己如果写成「本文不过度防御」，会再制造一个「无东坡肉」标题。
3. 要可发布、可被 Codex / Claude Code / Cursor 这类 harness 直接挂上（本仓库已有 `agents/openai.yaml` 适配位）。
4. 要区分「该留的 why」和「会话垃圾」，否则会被人骂把有用注释也杀掉。

---

## 6. 本项目要对齐的验收，而不是口号

用发起人的三个例子当验收夹具，而不是当文案。

**差（负向回声）：**

- PR 标题：`番茄炒蛋（无东坡肉）`
- 注释：`// 不使用东坡肉，因为番茄炒蛋不需要红烧工艺`
- commit：`移除冗余方案 B，按用户要求不再使用队列`
- 文章标题：`XXXX综述——不过度防御且无提示版`
- 开篇：`需要特别提醒，本文不存在过度防御`

**好（最终态）：**

- PR 标题：`番茄炒蛋`
- 注释：无，或只留真正的不变量
- commit：描述现在仓库里有什么
- 文章标题：`XXXX综述`
- 正文：直接写内容，不声明自己没做什么

一句话验收：**一个没参加过这次会话的读者，不应该从标题或注释里反推出「曾经有过东坡肉」。**
这和 ruff `AGENTS.md` 的「someone with no access to the Codex session」是同一条。

---

## 7. 来源索引

### 引爆与中文现场

- https://x.com/songkeys/status/2090416137720999992
- https://x.com/Nominatiivi/status/2090464250573779338
- https://x.com/hd_nvim/status/2090443732566884560
- https://x.com/laverya/status/2090470510660288566
- https://x.com/Nakotango/status/2090485305719902543
- https://x.com/lawhy_X/status/2090641896611922103
- https://x.com/coder_left/status/2090637888543486311
- https://x.com/fenny521/status/2088558374371926187

### 生产规则（GitHub）

- https://github.com/astral-sh/ruff/blob/main/AGENTS.md
- https://github.com/liby/dotfiles/blob/main/dot_codex/AGENTS.md
- https://github.com/southliu/south-admin-react/blob/main/AGENTS.md
- https://github.com/OktayCopurlu/ai-shared/blob/main/skills/applying-coding-style/SKILL.md
- https://github.com/DieInTyo/screen-switch/blob/main/AGENTS.md
- https://github.com/casivaagustin/dotfiles/blob/main/agents-rules/agents-rules/global.md

### 厂商 issue / 官方文档

- https://github.com/anthropics/claude-code/issues/65961 （+136）
- https://github.com/anthropics/claude-code/issues/85130
- https://github.com/anthropics/claude-code/issues/61305
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide

### 社区与论文

- https://news.ycombinator.com/item?id=43929768
- https://news.ycombinator.com/item?id=49078710
- https://news.ycombinator.com/item?id=47310225
- https://arxiv.org/abs/2608.01347
- https://x.com/housecor/status/2085125584615821723
- https://x.com/lucianghinda/status/2080933682039394322
- https://x.com/Love2Code/status/2087196528628699185
- https://x.com/traits_reality/status/2089628021049164047
