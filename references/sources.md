# 参考：各份规范的要点

每条只记能直接拿来判句子的规则。原文以链接为准。

## Ant Design 文案

<https://ant.design/docs/spec/copywriting-cn/>

- **明确表述立足点**：以用户为主体写，关注用户能用产品做什么，而不是产品为用户做了什么。
- **精简语句**：省略无用词汇，不重复用户已知的事实；绝大多数交互场景不必描述全部细节，提供简短、易于快速获取的内容。
- 使用用户熟悉的语言；表述一致；重要的信息放在显著位置；完整、直接地阐述信息；用词精准完整。
- 语气：精简、友好、正面。
- 标点：标签、标题、输入框下的提示、悬停提示、表格中的句子单独出现时，可以省略句末标点。

## Microsoft

<https://learn.microsoft.com/en-us/windows/apps/design/style/writing-style>
<https://learn.microsoft.com/en-us/power-platform/well-architected/experience-optimization/user-interface-content>
<https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/s/sorry>

- concise 不等于 limited，而是 efficient：用尽量少的字保住意思。
- 按钮文字最多两三个短词，一眼读完就知道它做什么。
- 报错：去掉多余信息，给一个用户能做的动作；不说用户不需要知道的事。报错标题描述问题，不描述要做的动作。
- 每句不超过 25 个英文词（中文可按一句不超过 30 字左右把握）。
- 「sorry」只用在给用户造成了严重问题的报错里。

## Material Design

<https://m1.material.io/style/writing.html>
<https://codelabs.developers.google.com/codelabs/material-communication-guidance>

- 写短小、可扫读的段落，一段只讲少数几件事。
- 关键词前置（front-load）：标题、列表项的开头几个字就说明它是什么。
- 用简单直接的语言；写完问一句「有没有更简单的说法」。

## Nielsen Norman Group：报错

<https://www.nngroup.com/videos/error-message-communication-guidelines/>

- 报错要清楚、简洁、礼貌、精确、有建设性、像人话。
- 结构：受影响的操作或对象 + 问题 + 下一步；和用户的工作有没有保存有关时，再说保存状态。不是每条都要四件齐。
- 不责怪用户；不用没解释过的术语，也不用泛泛的套话；不在让人沮丧的时刻开玩笑。

## Shopify Polaris

<https://polaris.shopify.com/components/empty-state>

- 可扫读：删掉不必要的词。
- 按钮以强动词开头。
- 空状态：说清这个功能能帮用户做什么，给出下一步。

## Arco Design（设计原则）

<https://arco.design/>

- 报错用语言表达，不直接给「404」这类代码；准确反映问题，给出建设性的解决办法。
- 预防错误胜过报错：在用户做出错误选择之前就挡住。
- 术语、功能、操作在整个系统里保持一致。

## 中文文案排版指北

<https://github.com/sparanoid/chinese-copywriting-guidelines>

- 中英文之间、中文与数字之间加空格；数字与单位之间加空格（度、百分号除外）。
- 用全角中文标点；不重复使用标点；数字用半角。

## no-ai-slop

<https://github.com/petergyang/no-ai-slop>

- 取它「删什么」的那一半：元话语、二元对比、冒号揭晓、装饰性加粗、拿破折号当节奏、同义词轮换、套话收尾、营销腔禁词。
- 不取「保住作者的声音」那一半：界面文案要的是全站一致，同类句子统一成一个说法。

## 我们自己踩出来的（不在任何一份规范里）

- 没有回执的动作只能说「已发出」。
- 纯文本面上的 `**` 会原样显示；模型写的字要在读数据的那一处统一去星号。
- 同一句话前后端各存一份会漂移：后端发信号，句子只放在前端。
- 测试、门禁、探针锚着文案原文；反向断言在旧句子改掉后会悄悄失效。
- 前端改动要重建镜像后才上线，`docker cp` 源码进容器不算。
- 判据成本不对称：负向判据（「必须不存在」）锚宽了会一直红，每次跑都要有人看；正向判据（「必须存在」）锚宽了只会漏报。所以负向判据锚定义形态（`^NAME *=`），不锚名字出现，名字会出现在讲历史的注释和 docstring 里。
- 门禁锚着的功能名、口径词往往是用户裁决过的叫法，改名先问，不当普通文案改。
- 「只修了一半」靠自己挑的用例抓不到：做输入校验、截断、归一化的地方，拿一张畸形输入清单（空、超长、emoji、NUL、换行、全角字母和数字、SQL 注入形、通配符）无差别跑一遍。
- 失败不是空，截断不是总数：2026-09-30 的评测里，两组审查在同一页上各漏了一处「失败显示成空」。逐句读是读不出来的，要按状态去看代码渲染了什么。
- 说明文字里的数字会过时：同一次评测查出说明里写的行数和代码对不上。写数字之前先看代码里的值。
- 反向断言失效时，断言精确值（`toBe("")`）比换一个新短语稳：新短语下次改文案还会失效。这是评测里不带技能那组的做法，比技能原来教的好。
- 报错可以带用户认得的对象名，只去掉路径和异常原文。同样来自评测里不带技能那组。
- 报错的下一步要对症：权限、超限、格式不支持这类重试好不了的，不写「请重试」。第二轮评测里不带技能那组这么做，带技能那组套了全站统一句式，反而没想到。
- 交给别的应用去做的事（mailto 打开邮箱、调起下载），页面收不到任何结果：「已发送」「已打开」都不能写；「已发出」在邮件语境里读起来就是信已寄出，也不能用。只写页面做到的那一步和用户还要做的。
- 门禁按源码 grep 时，把锚限定在字符串字面量里（`grep -qE '"[^"]*片段[^"]*"'`），比「挑一个注释里没有的片段」稳：后者下次有人改注释就又失效了。来自第二轮评测不带技能那组。
- 评测里技能丢的唯一一分出在它自己的例子上：例子把一句和裁决过的内容重合的话直接改写保留了，模型照着做。例子和规则一样要审。

## 2026-10 补充（去 AI 腔）

- stop-slop：https://github.com/hardikpandya/stop-slop
- humanizer（Wikipedia「Signs of AI writing」）：https://github.com/Aparnabuilds/humanizer
- renhua（中文去 AI 味，先结构后用词）：https://github.com/huangserva/renhua
- shuorenhua 说人话（改写不许变的东西）：https://github.com/MrGeDiao/shuorenhua
- quaiwei-skill（去多余引号）：https://github.com/nezhazheng/quaiwei-skill
- 「说白了已经是新AI味了」：https://post.smzdm.com/p/apqm42p7/
- vale-ai-tells（按密度判，不按单句判）：https://github.com/tbhb/vale-ai-tells
- humbleteam/ux-writing：https://github.com/humbleteam/ux-writing
- no-ai-slop 2026-08 后的规则（可移植性测试、解读型元话语、重要性吹捧、模糊归因）：https://github.com/petergyang/no-ai-slop/blob/main/skills/no-ai-slop/SKILL.md
- shuorenhua v2.5（按作用判断而不按词表命中、保住责任主体和下一步、改不准就撤销）：https://github.com/MrGeDiao/shuorenhua
- speak-human-tw（38 种痕迹、台湾在地化用语、保护清单）：https://github.com/Raymondhou0917/speak-human-tw
