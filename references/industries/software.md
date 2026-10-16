# 软件 / SaaS / 开发者工具界面文案风格

行业 id：`software`。覆盖 B2B SaaS、协作工具、开发者工具、云控制台、管理后台。

## 目录

1. 什么时候用这份
2. 语气和人格
3. 代表厂商和规范
4. 术语和叫法
5. 按元素写
6. 合规和硬约束
7. 高风险场景
8. 这个行业的 AI 腔和坏写法
9. 改前 → 改后
10. 审查时加查的项
11. 台港市场差异

## 1. 什么时候用这份

信号（命中任意两条就用；只命中一条时，结合用户的话判断）：

- 代码 / 依赖：`stripe` / `@stripe/stripe-js`、`@octokit/*`、`aws-sdk` / `@aws-sdk/client-*`、`@azure/*`、`@google-cloud/*`、`launchdarkly`、`@slack/web-api`、`next-auth`、`@clerk/*`、`jsonwebtoken`、`rbac`、`feature-flags`、`webhooks`
- 目录 / 文件名：`billing/`、`workspace/`、`organizations/`、`api-keys/`、`webhooks/`、`rbac/`、`permissions/`、`admin/`、`settings/`、`deploy/`、`ci/`、`audit-log/`
- 界面里的词：工作区、团队空间、组织、角色、权限、成员、邀请、套餐、用量、额度、超额、升级、API 密钥、令牌、webhook、部署、构建、环境变量、同步冲突、版本历史、回滚、审计日志、速率限制、请求 ID、错误码、工单
- 用户的话：「SaaS 后台」「开发者工具」「管理控制台」「B2B 产品」「云控制台」「工作台」「admin dashboard」

和别的行业重叠时：产品是「AI 功能 + SaaS 后台」（比如一个 AI 编码助手的管理控制台），计费、权限、删除、密钥这类场景按这份文件的硬约束；AI 对话本身的措辞（幻觉免责、模型能力边界）不在这份文件管辖范围内，按项目自己的 AI 功能文案规则来。

## 2. 语气和人格

- 一句话定调：把用户当成能自己处理问题的同行，直接、克制、不卖萌、不过度安抚；严肃场景（报错、计费、删除）不开玩笑，不严肃场景（空状态、首次引导）可以有一点克制的俏皮，但不能影响读取信息的速度。
- 人称：英文统一 "you"。中文项目里，面向普通成员的协作功能（创建文档、发消息）可以用「你」；面向企业采购方、财务、法务的场景（账单、合同条款、续费提醒）更多产品会切到「您」——这是中文 toB 产品里普遍能观察到的做法，并非某一份成文规范的强制要求，但选定后必须全站一致，写进项目自己的术语表，不要一个页面两种人称混用。
- 能不能用感叹号和 emoji：成功类 toast 最多一个感叹号；报错、警告、确认删除类文案不用感叹号，也不用 emoji（🎉✓⚠️ 这类都不用）。管理后台的危险操作用红色按钮 + 模态框文字表达严重性，不用 ⚠️ 符号代替——这和 `principles.md` 里「⚠️ 只留给不可逆场景」不同：软件行业里连「不可逆」也优先用颜色和文字，符号只在确实没有更好的视觉位置时才退而求其次。
- 和 `principles.md` 不同、要覆盖的地方：
  - `principles.md` 的报错例句带「请」（「保存失败，请重试」）；toB 控制台里很多工具型产品整句都不用「请」，直接祈使句：「重试」而不是「请重试」。两种风格都成立，但要选一种，全站一致。
  - 道歉：Microsoft Writing Style Guide 明确「sorry」只留给真的造成用户损失的报错，其他场景不道歉（<https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/s/sorry>）。中文同理：「抱歉」「非常抱歉」只留给数据丢失、服务中断、扣费错误这类真实损失，保存失败、网络超时这类可重试的错误不用。

## 3. 代表厂商和规范

| 厂商 / 规范 | 风格要点（能落到句子上的） | 出处 |
|---|---|---|
| Microsoft Writing Style Guide | 「sorry」只用于 Microsoft 产品确实出错、给用户造成真实影响的场景；其余用更轻的词 | <https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/s/sorry>（已核实） |
| Stripe 开发者文档 | 错误对象区分 `type`：只有 `card_error` 的 `message` 明确标注「可以直接显示给用户」，其余错误类型（`api_error`、`invalid_request_error`）的 message 面向开发者，不该原样进终端用户界面；`request_log_url` 是跳转到控制台请求日志的链接，不是裸露的一串 ID | <https://docs.stripe.com/api/errors>（已核实） |
| Stripe 密钥管理指南 | 密钥在控制台只显示一次；要求立刻存入密钥管理工具；明确写「Stripe 永远不会向你索要密钥」；建议用权限范围受限的 restricted key 而不是全量密钥 | <https://docs.stripe.com/keys-best-practices>（已核实） |
| AWS Cloudscape Design System | 报错按作用域分级：字段级用 inline，整页校验用 page alert，资源操作失败用 flashbar，组件渲染失败用组件内 alert，不新造错误样式；空状态标题句首大写、无句末标点，正文不用「please」「thank you」「省略号」「感叹号」；清空筛选的按钮固定写「Clear filter」 | <https://cloudscape.design/patterns/general/errors/>、<https://cloudscape.design/patterns/general/empty-states/>（已核实） |
| AWS Cloudscape（加载与刷新） | 表格优先用骨架屏而不是转圈（不打乱列宽）；手动刷新成功后显示时间戳，例句「Last updated December 21, 2023, 14:29 (UTC+01:00)」；加载文案不用冠词和句末标点，「Loading items」而不是「Loading the items.」；刷新完成要用 ARIA live region 播报 | <https://cloudscape.design/patterns/general/loading-and-refreshing/>（已核实） |
| IBM Carbon Design System | 通知按类型限长：行内通知 ≤2 行，toast ≤3 行；系统生成的通知要给背景，任务触发的通知可以更短（用户本来就在上下文里）；关键报错/错误通知不自动消失；例句「Credentials not found. Please verify your login information and try again.」 | <https://carbondesignsystem.com/patterns/notification-pattern/>（已核实） |
| IBM Carbon（空状态） | 正向措辞：用「Start by adding data assets」而不是「You don't have any data assets」；结构是标题（简短正向）+ 正文（下一步、为什么是空的）+ 一个主操作；不放多个平行选项，不引用别的功能区 | <https://carbondesignsystem.com/patterns/empty-states-pattern/>（已核实） |
| Atlassian Design System | 四类消息职责分明：错误＝告知已发生的问题和下一步；警告＝提前预告可能丢数据或出错的变化；成功＝和用户一起庆祝完成；信息＝提供有助于行动的额外信息；多数人是扫读，每个词都要有用，删掉无关细节 | <https://atlassian.design/foundations/content/designing-messages> |
| GitHub | 删除仓库走四段式确认：勾选「我想删除这个仓库」→ 勾选「我已阅读并理解这些后果」→ 输入仓库全名验证 → 按钮文字就是「Delete this repository」（不是「确定」）；这是 delete workspace / revoke key 类操作的范式 | <https://docs.github.com>（已核实，具体删除仓库文档页面未逐一核实） |
| Vercel | 环境名固定用 Production / Preview / Local，不混用「线上 / 预览 / 本地」等同义词；部署动作固定词是 Redeploy、Promote to Production、Rollback；部署状态是一套固定枚举：Queued → Initializing → Building → Ready / Error / Canceled，界面的状态标签直接对应这套枚举 | <https://vercel.com/docs/deployments>；状态枚举：<https://vercel.com/docs/rest-api/deployments/list-deployments>、<https://vercel.com/geist/deployment-status> |
| Mailchimp Content Style Guide | 核心原则「直白」：「我们把花哨去掉，把清晰看得比什么都重」；语气要跟着读者当下的情绪变化，而不是固定一种；宁可清楚也不要有趣（原话「更重要的是清楚，而不是有趣」） | <https://styleguide.mailchimp.com/voice-and-tone/>（已核实；页面没有报错 / 计费专项内容） |
| Ant Design 文案规范 | 报错措辞倾向「无法完成」而不是生硬的「失败」；以用户为主体、精简、一致的通用原则见 `references/sources.md`，这里只强调软件后台里报错不要用生硬判决式的词 | <https://ant.design/docs/spec/copywriting-cn/>（已核实，页面本身没有危险操作 / 权限报错专项内容） |
| 企业微信开发者文档 | 应用简介、推荐语「应真实准确地介绍产品功能及其特色，禁止出现'最佳''唯一''顶级'等绝对性词汇或其他夸大宣传的描述用语」——可直接套用到升级 / 付费引导文案的禁用词表 | <https://developer.work.weixin.qq.com/document/path/90569>（已核实） |
| 飞书开放平台多语言设计规范 | 只有排版空间规则，没有措辞规则：中文翻成英文等场景要给文案预留额外空间（10 字母以内的词建议预留 100%–200% 空间），优先上下结构而不是并排结构来容纳变长的文案 | <https://open.feishu.cn/document/design-specification/internationalization/multilingual-design-specification>（已核实；仅排版空间规则，不含文案措辞规则） |
| 《消费者权益保护法实施条例》第九条（国务院令第 778 号，2024 年 7 月 1 日起施行） | 以自动展期、自动续费方式提供服务的，要在消费者接受服务前和自动续费等日期前，以显著方式提请消费者注意；SaaS 的续费提醒、试用转付费提示直接受这条约束（见第 6 节） | <https://www.moj.gov.cn/pub/sfbgw/jgsz/jgszjgtj/jgtjlfej/lfejtjxw/202501/t20250102_512298.html> |

## 4. 术语和叫法

| 用 | 不用 | 说明 |
|---|---|---|
| 工作区 | 空间、Workspace（英文直出） | 产品里如果「工作区」和「项目」是两层概念，不能互换 |
| 组织 | 公司、租户 | 「租户」是开发者内部叫法（multi-tenant），不进界面 |
| 成员 | 用户 | 指团队内部的人时用「成员」，「用户」留给对外、匿名或统计语境 |
| 角色 | 权限组 | 除非产品自己的功能确实叫「权限组」 |
| 套餐 | 计划、Plan（英文直出） | 中文界面统一用「套餐」，不要「计划」和「套餐」混用 |
| 用量 | 使用量、消耗量 | 三个词选一个，全站统一 |
| 额度 | 配额、quota（英文直出） | |
| 已用尽 / 已超出 | 超限 | 「已用尽」指用到了上限，「已超出」指超过了上限（可能产生额外扣费），两种后果不同，不能都写「超限」 |
| 升级套餐 | 升级计划、Upgrade（纯英文） | |
| API 密钥 | API Key、密钥串 | 如果产品里「API 密钥」和「访问令牌」是两种不同的凭证，不能混用其中一个指代另一个 |
| 访问令牌 | Token、access token | |
| 吊销 | 撤销、作废、停用 | 「吊销密钥」是业内对「让密钥立刻失效」的通用叫法；「停用」容易被理解成「可以重新启用」，要区分清楚吊销是否可逆 |
| 工作区所有者 | 超级管理员、Owner（纯英文） | 按产品自己定义的角色体系来，不要自造新角色名 |
| 管理员 | 运营、admin | |
| 部署 | 发布 | 如果产品区分「部署」（基础设施上线）和「发布」（面向用户开放功能），两个词不能互换 |
| 构建 | 编译 | 构建包含编译、打包等多个步骤，不能用「编译」代替「构建」 |
| 生产环境 / 预发环境 / 测试环境 | 线上、线下 | 正式界面用全称，「线上 / 线下」留给内部沟通 |
| 环境变量 | 配置项、参数 | 「环境」和「环境变量」是两个概念，前者指 production/staging，后者指 env var，不要混着指 |
| 回滚 | 撤销部署、revert | |
| 同步冲突 | 版本冲突 | 如果产品里这是两种不同的状态（内容冲突 vs 版本号冲突），不能混用 |
| 请求 ID | Trace ID、日志 ID | 跟支持团队内部约定的排障字段名一致，不要随便换叫法 |
| 速率限制 | 限流、流控 | 面向用户的提示统一叫法，不要界面上一处「限流」一处「请求过于频繁」 |
| 审计日志 | 操作日志、变更记录 | 如果产品本身有专门叫「审计日志」的功能，不要和普通的操作记录混叫 |
| 只读 | 查看权限、View-only（英文直出） | |
| 已失效 | 已过期、已作废 | 区分密钥「到期自然失效」和「被手动吊销」，这两种原因对用户的下一步不同，不能都写「已失效」 |

开发者用词不进界面：tenant、RBAC、webhook payload、idempotency key（除非产品面向的就是开发者本人，这种情况下这些是正确术语，不算「开发者用词」）、队列、重试策略、熔断。

## 5. 按元素写

### 报错：权限 / 角色

说清楚「谁能解决」，不要只说「没有权限」。

- 中：没有编辑权限，请联系工作区管理员开通。
- 英：You don't have permission to edit this. Ask a workspace admin for access.
- 能定位到具体管理员时，带上名字：「请联系工作区管理员张三开通查看权限」比泛泛的「请联系管理员」更快解决问题，但名字要来自产品本来就有的数据（比如工作区设置页的 Owner 字段），不能编。

### 报错：计费 / 套餐额度

结果先说具体数字，再给路径；不写恐吓性语言，不堆感叹号。

- 中：本月 API 调用已用完（10,000 / 10,000 次）。升级到 Pro 可提升到 100,000 次。
- 英：You've used all 10,000 API calls this month. Upgrade to Pro for 100,000 calls.
- 数字必须和后端实际配置一致（本月已用量、套餐上限），不能写约数或旧版本文案里留下的数字。

### 确认框：危险 / 不可逆操作

按 GitHub 删除仓库的范式：说清删的是什么、牵连多少东西、能不能撤回；破坏力越大，确认动作越重（从点按钮到输入对象名）。

- 中：将永久删除工作区「产品组」，包含 12 个项目和 48 名成员的访问记录。此操作无法撤销。输入工作区名称以确认。
- 英：This will permanently delete the "Product Team" workspace, including 12 projects and 48 members' access. This can't be undone. Type the workspace name to confirm.
- 按钮文字写动作本身：「删除工作区」「吊销密钥」，不写「确定」。
- 破坏力分级：删除单条记录、移除一个成员 → 点一次确认即可；删除工作区、吊销生产环境密钥、清空账单历史 → 要求输入对象名或勾选「我已了解后果」。

### 按钮：触发付费义务时

按钮文字要让人一看就知道「点了会花钱」，不能用「下一步」「继续」这类看不出后果的词——这不只是风格偏好，欧盟 Consumer Rights Directive 的「按钮解决方案」把它变成了硬约束（见第 6 节）。

- 差：下一步 / Continue
- 好：立即支付 ¥99 / Pay $99 now
- 免费试用转付费的按钮同理：「开始付费订阅」比「继续」更清楚，哪怕用户已经在试用期里操作了好几步。

### 表单标签和校验：开发者配置项

字段名用产品自己 schema 里的字段名，不要另造一个更「好听」的说法，否则用户在文档和界面之间对不上；校验报错要点名具体字段，不写泛泛的「输入有误」。

- 中：Webhook 地址必须以 https:// 开头。
- 英：Webhook URL must start with https://.
- 占位符给真实格式例子，不写说明书：`https://api.example.com/v1/webhooks/order-updated` 比「请输入合法的 URL」更有用。

### 空状态：开发者工具 / 管理后台

第一次使用、被清空、筛选无结果分开写（和 `principles.md` 通用规则一致），这里补充软件行业两个常见坑：

- 还没有任何资源时，给出能直接执行的下一步，不是空泛的「暂无数据」：
  - 中：还没有创建 API 密钥。创建一个开始调用接口。
  - 英：No API keys yet. Create one to start making requests.
- 筛选 / 搜索无结果时，清空筛选的操作文字全站统一一种说法（参照 AWS Cloudscape 的「Clear filter」）：中文统一用「清除筛选条件」，不要一处写「重置筛选」一处写「清空条件」。

### API 密钥 / 令牌展示

- 创建后只显示一次，提醒语写清楚「做什么」而不是空泛的「妥善保管」：
  - 中：sk_live_••••dp7dc 已复制到剪贴板。离开此页面后将无法再次查看完整密钥，请立即保存。
  - 英：sk_live_••••dp7dc copied to clipboard. You won't be able to view this key again after leaving this page.
- 列表里展示已创建的密钥默认打码，只露最后 4 位，供用户辨认是哪一把；不提供「再次查看」的入口（Stripe 的明确原则：密钥创建后不可再读取，只能吊销重建）。
- 吊销要立刻说明后果：「吊销后，使用这把密钥的请求会立刻失败，且无法恢复。」

### 进度 / 异步任务

状态词 + 预期时长 + 完成后怎么通知用户，三者缺一就显得敷衍。

- 中：正在生成报表，通常需要 1–2 分钟，完成后会通知你。
- 英：Generating report, usually takes 1–2 minutes. We'll notify you when it's done.
- 刷新、重试类操作成功后显示时间戳，带时区（跨时区团队必须）：「最后更新于 2026 年 10 月 16 日 14:29（UTC+8）」。
- 加载态文案不用冠词和句末标点（参照 AWS Cloudscape）：「正在加载」而不是「正在加载数据中……」。

### 状态标签：版本 / 部署 / 同步

- 部署状态用一套固定的阶段词，不同阶段不用近义词替换：构建中 → 部署中 → 已上线 → 部署失败 → 已回滚（对应 Building → Deploying → Live → Failed → Rolled back）。「处理中」这种笼统词不能同时指代构建、部署、排队三种不同阶段。
- 同步冲突要说清楚冲突双方和解决路径，不是冒号揭晓机制：
  - 中：这份文档已被他人修改，你的更改尚未保存。保留你的版本，或先查看对方的改动。
  - 英：This document was changed by someone else. Your edits haven't been saved. Keep your version, or review their changes first.

### 设置项说明

开关、字段下的说明只写「打开后会发生什么」，不讲实现机制；需要更高权限才能改的设置要说明谁能改。

- 中：开启后，新成员默认拥有只读权限，可在成员页单独调整。
- 英：When enabled, new members get read-only access by default. You can adjust this per member.
- 锁定的设置项：「仅组织管理员可修改」而不是把控件直接置灰却不说明原因。

### CLI / 终端消息

成功、警告、报错各一种前缀，不混用；报错要带对象名和能跑的下一步命令，不是干巴巴的「出错了」。

- 差：`Error occurred`
- 好：`Error: config file "config.yaml" not found. Run "myapp init" to create one.`
- 成功只回一行结果，不加表情或多余的祝贺语：`Deployed to production (https://app.example.com)`。

### 错误码 / 请求 ID：什么时候给用户看

默认不放在报错正文第一行；只在「需要联系支持」时才需要用户提供，所以放在次要位置（报错下方小字、或「查看详情」展开里）。

- 中：保存失败，请重试；多次失败请联系支持并提供错误码 ERR_8872。
- 英：Save failed. Try again, or contact support with error code ERR_8872 if this keeps happening.
- 异常原文、服务器路径、堆栈这些永远不进界面，只进日志；这条和 `principles.md` 的通用报错规则一致，这里强调的是「错误码本身可以给，但位置要次要、要配上下一步」。

### 升级 / 付费引导

只说能解锁什么，不造假稀缺、不用反问句劝退关闭动作。

- 中：升级到 Team 版，解锁无限成员和审计日志。
- 英：Upgrade to Team for unlimited members and audit logs.
- 关闭 / 跳过升级弹窗的按钮写「暂不升级」「以后再说」，不写「不，我不想要更好的产品」这类自我矮化式按钮（confirmshaming，见第 6 节）。

### 通知 / 推送：任务完成、异常告警

异步任务结束后，通知文案要和发起时的提示用同一套叫法，用户隔了几分钟回来不会对不上号；渠道按影响程度分级，不是所有通知都要发邮件。

- 发起时：「正在生成报表，通常需要 1–2 分钟，完成后会通知你。」完成后通知必须呼应同一个对象名：「报表已生成，点击查看。」而不是换一种说法让用户猜是不是同一件事。
- 分级：常规后台任务完成只需要站内通知；计费失败、密钥即将过期、服务中断这类会影响账户状态或造成损失的，站内通知 + 邮件都要发。

### 引导 / 首次使用：开发者上手

代码片段旁的复制按钮，点击后的状态反馈直接替换按钮文字（「复制」→「已复制」，几秒后复位），不额外弹 toast 打断阅读代码的视线。

- 中：复制 → 已复制
- 英：Copy → Copied
- 上手清单（onboarding checklist）里已完成的项目用完成态描述，不是祈使句残留：「已连接 GitHub」而不是「连接 GitHub ✓」。

### 帮助说明：面向开发者的设置项

同一个产品里，面向终端用户的报错要去掉错误码和技术词（见「错误码 / 请求 ID」），但面向开发者本人的设置页说明文字可以用技术词，因为这里的读者就是开发者——这是软件行业的特例：受众变了，能不能用技术语言的规则也跟着变，不是「技术词一律不能出现在界面上」。

- 中（开发者设置页，合理）：超过该速率的请求会被拒绝，返回 HTTP 429。
- 中（普通用户看到的报错，仍要避免技术词）：操作过于频繁，请稍后再试。

## 6. 合规和硬约束

软件行业没有统一的行业监管机构，但计费、续费、广告用语这几类有明确法规约束；无障碍遵循 WCAG 标准。

- **广告用语**：《中华人民共和国广告法》第九条第（三）项禁止使用「国家级」「最高级」「最佳」等绝对化用语；产品内的升级引导、功能介绍文案如果带推广性质，同样不能用「最强大的 AI」「唯一一款」这类词——这不只是文风问题，是广告法硬约束。
- **自动续费提醒**：《消费者权益保护法实施条例》第九条（2024 年 7 月 1 日起施行，见第 3 节）要求以自动续费、自动展期方式提供服务的经营者，在扣费前以显著方式提醒消费者；界面上必须在扣费前的合理时间展示续费日期、金额、取消路径，不能把这条提醒做得比周围文字更小或更浅。
- **按钮解决方案（EU Consumer Rights Directive 2011/83/EU 第 8(2) 条）**：触发付费义务的按钮必须用清楚无歧义的文字标明会产生付款义务，不能写「继续」「提交」这类看不出要花钱的词；中文产品面向欧盟用户时，「立即购买」「确认支付 ¥99」这类写法符合要求，「下一步」不符合。
- **ROSCA（美国 Restore Online Shoppers' Confidence Act，15 U.S.C. §§ 8401–8405）**：面向美国用户的订阅类产品，自动续费条款要在收费前「清楚显著」地披露，并提供简单的取消路径；取消流程不能比订阅流程更复杂（取消入口藏在客服邮件、多层弹窗里属于违规风险）。
- **Dark pattern（FTC「Bringing Dark Patterns to Light」报告，2022 年 9 月发布）**：报告确认列举了虚假倒计时 / 虚假紧迫感（false urgency，如不真实的倒计时和「仅限今天」提示）、confirmshaming（用羞耻感引导用户远离对商家不利的选项）等暗黑模式类型；这里的中文示例句「不，我不想要更快的速度」是本文自拟的说明性例句，不是报告原文翻译。参见 <https://www.ftc.gov/reports/bringing-dark-patterns-light>。
- **无障碍（WCAG 2.1）**：
  - 3.3.1 Error Identification：报错要用文字指出哪里错了，不能只变红色边框；<https://www.w3.org/WAI/WCAG21/Understanding/error-identification.html>
  - 3.3.3 Error Suggestion：能给出修复建议时必须给；<https://www.w3.org/WAI/WCAG21/Understanding/error-suggestion.html>
  - 2.5.3 Label in Name：可见的按钮文字必须包含在它的无障碍名称（aria-label）里，不能图标按钮可见写「保存」、aria-label 却写别的词；<https://www.w3.org/WAI/WCAG21/Understanding/label-in-name.html>
  - 4.1.3 Status Messages：异步任务、刷新完成这类状态变化，要能被读屏器感知（`role="status"` / `aria-live`），不能只靠视觉上的 Spinner 消失；<https://www.w3.org/WAI/WCAG21/Understanding/status-messages.html>
- **必须的格式**：金额带币种和计费周期（「¥99/月」「$29/mo」），扣费前的提醒必须给出具体扣费日期；时间戳跨时区场景（部署记录、审计日志）必须带时区；错误码格式全站统一前缀（如 `ERR_` 或 HTTP 状态码 + 内部码），不要一半页面用纯数字、一半用带前缀的码。

## 7. 高风险场景

### 删除工作区 / 组织

必写：删除的对象名称、牵连范围（项目数、成员数、账单历史）、是否可恢复、确认方式。

- 中：将永久删除工作区「产品组」，包含 12 个项目和 48 名成员的访问记录。此操作无法撤销。输入工作区名称以确认。
- 英：This will permanently delete "Product Team," including 12 projects and 48 members' access. This can't be undone. Type the workspace name to confirm.

### 吊销 API 密钥 / 撤销访问令牌

必写：吊销的是哪一把（名称或后 4 位）、生效时间（立即）、依赖它的服务会怎样、能否恢复。

- 中：吊销「生产环境密钥」(sk_live_••••dp7dc) 后，使用这把密钥的请求会立刻失败，且无法恢复，需要重新生成。
- 英：Revoking "Production key" (sk_live_••••dp7dc) will immediately fail any requests using it. This can't be undone.

### 自动扣费 / 续费

必写：扣费金额、币种、扣费日期、取消路径；不能用模糊语言淡化即将发生的扣费。

- 中：Pro 套餐将于 2026 年 11 月 1 日自动续费 ¥299，可在账单设置中随时取消。
- 英：Your Pro plan renews on Nov 1, 2026 for $39. Cancel anytime in billing settings.

### 超出套餐额度

必写：当前用量、上限、超出后的具体后果（服务降级 / 停止 / 自动产生额外费用），不写恐吓性语言。

- 中：本月用量已达上限（10,000 / 10,000 次调用），超出部分将按 ¥0.01/次计费。升级到 Pro 可提升额度。
- 英：You've reached your limit (10,000 / 10,000 calls). Extra calls are billed at $0.0015 each. Upgrade to raise your limit.

### 变更成员权限

必写：被改权限的人、变更前后的差异、生效时间；不写指责性语言。

- 中：李雷的角色已从「编辑者」改为「只读」，下次登录后生效。
- 英：Li Lei's role changed from Editor to Viewer, effective next login.

### 数据同步冲突

必写：冲突双方（谁的改动、什么时间）、哪一份可能丢失、如何解决。

- 中：这份文档已被他人修改，你的更改尚未保存。保留你的版本，或先查看对方的改动再决定。
- 英：This document was changed by someone else. Your edits haven't been saved. Keep your version, or review their changes first.

### 审计日志展示范围

必写：这条记录谁能看到、记录的是什么操作（而不是只写「有变更」）、是否包含其他成员的敏感信息（IP、邮箱）。

- 中：张三于 10 月 16 日 14:29 将李雷的角色改为「只读」。此记录仅工作区管理员可见。
- 英：Zhang San changed Li Lei's role to Viewer on Oct 16, 14:29. Visible to workspace admins only.

## 8. 这个行业的 AI 腔和坏写法

| 坏写法 | 例子 | 改法 |
|---|---|---|
| 讲基础设施实现 | 「这个任务存在消息队列里，重试了 3 次」 | 删，只留用户能感知的结果：「处理失败，已自动重试 3 次」或更简单地说清当前状态 |
| toB 营销腔混进产品内 | 「全链路智能化，助力团队降本增效」出现在功能介绍或升级弹窗里 | 删，写这个功能具体能做什么：「自动生成周报，节省手动整理的时间」 |
| 内部错误类型直接抛给用户 | 「ValidationError: field 'email' invalid」「500 Internal Server Error at line 42」 | 改成用户能懂的问题 + 下一步：「邮箱格式不正确，请检查后重新输入」；堆栈只进日志 |
| 道歉过重 | 「非常抱歉给您带来不便，我们深表歉意，请您谅解」用在保存失败这类可重试错误上 | 「保存失败，请重试。」sorry 只留给真的造成损失的场景 |
| 用感叹号/emoji 软化严肃操作 | 「太棒了！工作区已删除 🎉」 | 「工作区已删除。」删除成功不该带庆祝语气 |
| 虚假稀缺的升级引导 | 「立即升级，仅剩最后 3 小时！」（其实没有时间限制） | 「升级到 Team 版，解锁无限成员和审计日志。」不造假倒计时 |
| 被动语态掩盖套餐限制 | 「该功能已被限制」，不说是因为当前套餐 | 「此功能仅限 Pro 及以上套餐，当前是 Free 套餐。」说清是谁限制的、怎么解除 |
| 错误码堆砌在正文开头 | 「ERR_8872 / Request ID: a1b2c3-xyz：保存失败」 | 先说结果和下一步，错误码放在「联系支持」的次要位置：「保存失败，请重试；多次失败请联系支持并提供错误码 ERR_8872」 |
| 电商称呼腔混进 B2B 后台 | 「亲，欢迎升级尊享版哦～」 | 「欢迎使用 Team 版。」B2B 场景不用「亲」「小主」这类零售称呼 |
| 确认框不说后果 | 「您确定吗？」 | 说清删的是什么、牵连范围、能不能撤销；按钮写动作本身，不写「确定」 |
| 状态词语义模糊 | 「处理中」同时指构建中、部署中、排队中三种状态 | 分阶段用固定词：构建中 / 部署中 / 已上线，不混用 |
| Confirmshaming | 升级弹窗的关闭按钮写「不，我不想要更快的速度」 | 「暂不升级」「以后再说」，不自我矮化用户的选择 |

## 9. 改前 → 改后

| 改前 | 改后 | 问题 |
|---|---|---|
| Error: Insufficient permissions (403) | 没有权限访问该工作区，请联系管理员开通查看权限。 | 直接暴露 HTTP 状态码当正文，没给下一步 |
| 您的套餐已达上限，请升级！ | 本月 API 调用已用完（10,000 / 10,000 次）。升级到 Pro 可提升到 100,000 次。 | 没有具体数字；升级诱导带感叹号 |
| 确定要删除这个工作区吗？ | 将永久删除工作区「产品组」，包含 12 个项目和 48 名成员的访问记录。此操作无法撤销。输入工作区名称以确认。 | 后果、牵连范围、是否可撤销全部缺失 |
| Your API key: sk_live_EXAMPLE-NOT-A-REAL-KEY-a1b2（请妥善保管） | sk_live_••••a1b2 已复制到剪贴板。离开此页面后将无法再次查看完整密钥，请立即保存。 | 明文显示密钥、没打码；「妥善保管」空洞，没说具体要做什么 |
| 处理中… | 正在生成报表，通常需要 1–2 分钟，完成后会通知你。 | 状态词笼统，没有预期时长和完成通知方式 |
| 文档已更新，但你的更改未保存（可能被覆盖） | 这份文档已被他人修改，你的更改尚未保存。保留你的版本，或先查看对方的改动再决定。 | 冒号揭晓机制，没给出可操作的两个选项 |
| Deploying / Building / Processing 在同一个部署流程里混用 | 构建中 → 部署中 → 已上线 | 同名异称，用户分不清所处阶段 |
| `$ Error occurred` | `$ Error: config file "config.yaml" not found. Run "myapp init" to create one.` | CLI 报错没说明对象和可执行的下一步命令 |
| 系统出错，错误码 ERR_8872，Request ID: a1b2c3-xyz | 保存失败，请重试；多次失败请联系支持并提供错误码 ERR_8872。 | 错误码/请求 ID 占了正文第一行，应放在联系支持时才用得上的次要位置 |
| 立即升级，只省最后 3 小时！ | 升级到 Team 版，解锁无限成员和审计日志。 | 虚假倒计时，属于 dark pattern |
| 该功能已被限制 | 此功能仅限 Pro 及以上套餐，当前是 Free 套餐。 | 被动语态掩盖是套餐限制，没说当前套餐和怎么解除 |
| 非常抱歉给您带来不便，我们深表歉意，请您谅解 | 保存失败，请重试。 | 道歉过重，Microsoft 规则里 sorry 只留给真正的损失场景 |
| Oops! Something went wrong :( （用于支付失败） | Payment failed: your card was declined. Update your payment method to keep Pro features. | 用俏皮语气处理影响账户状态的报错，没给对象和下一步 |
| 该成员权限已变更 | 李雷的角色已从「编辑者」改为「只读」，下次登录后生效。 | 没说清改了谁、改成什么、何时生效 |
| 亲，欢迎升级尊享版哦～ | 欢迎使用 Team 版。 | 电商称呼腔混进 B2B 后台 |
| 下一步（按钮，点击后立刻扣费 ¥99） | 立即支付 ¥99 | 按钮看不出会花钱，不符合「按钮解决方案」要求 |
| 输入有误，请检查后重试 | Webhook 地址必须以 https:// 开头。 | 没点名具体字段和具体要求，用户不知道哪里错 |

## 10. 审查时加查的项

- [ ] 权限报错有没有说清「谁能解决」（具体角色或人），而不是只说「没有权限」
- [ ] 计费 / 用量报错有没有给出具体数字（当前用量、上限、价格、币种、扣费日期），且和后端实际配置对得上
- [ ] 删除 / 吊销类危险操作有没有说清影响范围、能否撤销，且确认方式的重量和破坏力相称（强破坏力要求输入对象名，不是点一下「确定」）
- [ ] API 密钥 / 令牌展示有没有做到：创建后只显示一次、列表默认打码、离开页面前有复制入口
- [ ] 异步任务的进度文案有没有给出预期时长和完成后的通知方式，不是只写「处理中」
- [ ] 版本 / 部署 / 同步相关的状态词是不是全站同一套，同一阶段只用一个词，没有用「处理中」这类词兼指多个阶段
- [ ] 错误码 / 请求 ID 有没有放在「联系支持时提供」的次要位置，而不是报错正文第一行
- [ ] 升级 / 付费引导有没有虚假稀缺（倒计时、「仅剩 N 份」）、关闭按钮有没有写成自我矮化的 confirmshaming 句式
- [ ] 无障碍标签（aria-label）有没有和可见文字一致（WCAG 2.5.3），异步状态变化有没有配 `aria-live` / `role="status"`（WCAG 4.1.3）让读屏器用户能感知到
- [ ] 面向企业管理员/采购决策场景和面向普通成员场景的人称（你 / 您）有没有刻意区分、全站一致

## 11. 台港市场差异

- 台湾：
  - 网路购买享有 7 日解除权（《消費者保護法》第 19 条）。不过「非以有形媒介提供之數位內容或一經提供即為完成之線上服務」，经消费者事先同意才提供的，可以排除解除权（《通訊交易解除權合理例外情事適用準則》第 2 条第 5 款）。
  - 落到文案：付费下载、开通订阅前，要有单独的确认句，说明一经提供即无法依消保法解除契约，不能把这层同意藏在服务条款里。<https://law.moj.gov.tw/LawClass/LawSingleRela.aspx?PCODE=J0170012&FLNO=2&ty=L>
- 香港：没有通用的网购冷静期。误导性遗漏（第 13E 条）、具威嚇性的营业行为（第 13F 条）由《商品說明條例》（Cap. 362）第 2B 部「不良營商手法」规管，该部分于 2013 年 7 月 19 日生效。升级引导、续费说明不能隐瞒价格和续费条件。<https://www.elegislation.gov.hk/hk/cap362!zh-Hant-HK>
- 第 6 节引用的《广告法》第九条、《消费者权益保护法实施条例》只适用大陆，台港站要换成上面的依据。
- 个资：台湾适用《個人資料保護法》（蒐集时依第 8 条告知），香港适用《個人資料（私隱）條例》（Cap. 486），不是大陆《个人信息保护法》。

用词差异（`locale-zh-hant.md` 已有的 软件、程序、服务器、默认 等不再列）：

| 简体 | 台湾 | 香港 |
|---|---|---|
| 代码 / 源代码 | 程式碼 / 原始碼 | 程式碼 / 源代碼 |
| 插件 / 扩展 | 外掛程式 / 擴充功能 | 插件 / 擴充功能 |
| 缓存 | 快取 | 快取／緩存 |
| 字段 | 欄位 | 欄位 |
| 日志 | 記錄檔、日誌 | 日誌 |
| 运维 / 云 | 維運 / 雲端 | 運維 / 雲端 |
