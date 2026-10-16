# zh-ui-copy

[繁體中文](README.zh-Hant.md) · [English](#english)

一个给 AI 编程助手用的界面文案技能（[Agent Skill](https://agentskills.io)）：写、改、审前端文案，去掉 AI 腔，并且改完不弄坏测试。

支持 Claude Code、OpenAI Codex、DeepSeek Harness，以及其他兼容 Agent Skills 规范的工具。主要面向中文界面，英文文案同样适用。

## 改前 → 改后

| 改前 | 改后 | 问题 |
|---|---|---|
| 读不到这个文件：[Errno 2] No such file or directory: '/srv/files/…/x.docx' | 读取文件失败，请重试；多次失败请联系管理员。 | 异常原文和服务器路径漏给用户 |
| 好，这一轮我没有改动文档。 | 文档没有改动。 | 助手腔 |
| 文件的字节没有变化 —— 它可能只是回答了你，并没有改动这份文件。 | 文件没有变化，智能体可能只回答了问题，没有修改文件。 | 开发者用词、破折号 |
| 已撤销 3 步，文档已恢复 | 已发出 3 步撤销，请确认文档是否已恢复。 | 没有回执，却说成已完成 |
| 邮件已发送给 3 位联系人 ✓ | 邮件已写好，请在邮箱中检查后发送。 | 页面只打开了邮箱，不知道信发没发 |
| 最近对话 · 共 30 个（接口只取了 30 个） | 最近 30 个对话 | 截断写成了总数 |

更多案例见 [`references/examples.md`](references/examples.md)。

## 它和普通的「去 AI 味」提示词有什么不同

- **只说确认了的事**：没有回执的动作、交给别的应用做的事、无法确认的状态，都有固定写法，不会写成「已完成」。
- **按状态审**：加载中、成功、空、失败、截断各显示哪句话。失败被显示成「暂无数据」、截断被写成「共 N 条」，这类问题逐句读是读不出来的。
- **文案里的数字和代码对账**：上限、条数、时长，以代码里的值为准。
- **改完不弄坏测试**：`check_copy_anchors.py` 会找出测试和门禁里会断的锚点（BREAK），以及改完后会永远通过的反向断言（VACUOUS）。
- **项目约定可配置**：叫法、用户裁决过的名字、固定句式写进项目的 `docs/copy-glossary.md`，技能会先读它。

## 安装

技能就是一个目录，放到工具会扫描的位置即可。

| 工具 | 用户级目录 | 项目级目录 |
|---|---|---|
| Claude Code | `~/.claude/skills/zh-ui-copy` | `.claude/skills/zh-ui-copy` |
| OpenAI Codex | `~/.agents/skills/zh-ui-copy` | `.agents/skills/zh-ui-copy` |
| DeepSeek Harness | `~/.agents/skills/zh-ui-copy` 或 `~/.dsh/skills/zh-ui-copy` | `.agents/skills/zh-ui-copy` 或 `.dsh/skills/zh-ui-copy` |

三个工具都用的话，克隆一份，再链接过去：

```bash
# macOS / Linux
git clone https://github.com/ZheShen00/zh-ui-copy ~/.agents/skills/zh-ui-copy
mkdir -p ~/.claude/skills && ln -s ~/.agents/skills/zh-ui-copy ~/.claude/skills/zh-ui-copy
```

```powershell
# Windows（目录联接，不需要管理员权限）
git clone https://github.com/ZheShen00/zh-ui-copy "$env:USERPROFILE\.agents\skills\zh-ui-copy"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
cmd /c mklink /J "$env:USERPROFILE\.claude\skills\zh-ui-copy" "$env:USERPROFILE\.agents\skills\zh-ui-copy"
```

不要再往 `~/.codex/skills` 放一份副本，否则 Codex 会加载两次。

需要 Python 3.8 以上（脚本只用标准库）；`check_copy_anchors.py` 需要 git。

## 使用

- Claude Code：`/zh-ui-copy`，或者直接说「把这页文案去下 AI 味」
- Codex：`$zh-ui-copy`，或在 `/skills` 里选
- DeepSeek Harness：`/zh-ui-copy`，或直接描述需求

三种活：

- **审**：「审一下 `src/pages/orders.tsx` 的文案，只列问题」。交付问题清单，不改文件。
- **改**：「把这几句报错改干练」。交付改前 → 改后、改了多少处、验证结果。
- **写**：「给上传失败写一句报错」。

## 行业风格

银行要写清手续费和到账时间，医院要分清给医生看还是给病人看，工厂的报警要写原因、后果和处置。技能内置 9 个行业的风格文件，各含语气、术语、按元素的写法、合规硬约束、高风险场景和改前 → 改后：

| id | 行业 | 典型产品 |
|---|---|---|
| `ai` | AI 产品 | 对话助手、Copilot、智能体、模型控制台 |
| `software` | 软件 / SaaS / 开发者工具 | 协作工具、云控制台、管理后台、CLI |
| `system` | 操作系统 / 系统软件 / 桌面应用 | 系统设置、安装更新、安全软件、浏览器 |
| `mobile` | 手机 App / 小程序 | 消费类 App、小程序、厂商应用 |
| `finance` | 金融 | 银行、支付、理财、保险、借贷 |
| `medical` | 医疗健康 | HIS / EMR、患者 App、互联网医院、医疗器械软件 |
| `education` | 教育 | K12、高校、LMS、语言学习、考试 |
| `government` | 政府 / 公共服务 | 政务服务、社保税务、公共事业 |
| `industrial` | 工业 / 制造 / 能源 | HMI / SCADA、MES、IIoT、能源管理 |

**怎么选**，先到先得：

1. 你直接说：「这是银行 App」。
2. 项目术语表 `docs/copy-glossary.md` 里写一行 `行业：finance`（几个行业就写几个，如 `行业：finance, ai`）。
3. 自动识别：`python scripts/detect_industry.py <仓库目录>` 按依赖、目录名、界面用词打分，★ 是最高分。仓库里有 `zh-TW` / `zh-Hant` / `zh-HK` 语言文件时，它还会提示加载繁体用词和台港差异。
4. 都没有：从句子本身判断，判断不了就用通用规则。

几个行业同时命中时，合规硬约束全部叠加，语气按用户最直接面对的那个行业。

**繁体 / 台港**：[`references/locale-zh-hant.md`](references/locale-zh-hant.md) 管用词和标点（「文件」→「檔案」、「默认」→「預設」）；每份行业文件的「台港市场差异」一节管法规和必须出现的话，例如台湾借贷要标示總費用年百分率、个资告知按台湾《個人資料保護法》而不是大陆《个人信息保护法》。

**加一个行业**：照 [`references/industries/_TEMPLATE.md`](references/industries/_TEMPLATE.md) 写一份 `references/industries/<id>.md`。识别脚本从新文件第 1 节读信号，不用改代码。

## 给你的项目写术语表

把 [`assets/glossary-template.md`](assets/glossary-template.md) 复制到项目的 `docs/copy-glossary.md`，填上你们的叫法和裁决。`SKILL.md` 里的「项目约定」是默认值，项目术语表优先。

## 脚本

都是只读的，不改任何文件。路径相对技能目录；macOS / Linux 上没有 `python` 就用 `python3`。

```bash
python scripts/extract_ui_strings.py src/             # 列出界面文字
python scripts/extract_ui_strings.py --attrs src/     # 列出 aria-label / title / placeholder / alt
python scripts/check_copy_anchors.py --base HEAD      # 在仓库里跑：查改文案会弄断的测试锚点
python scripts/detect_industry.py <仓库目录>          # 猜行业、发现繁体界面
python scripts/selftest.py                            # 脚本自测
```

## 目录

```
SKILL.md                      技能入口
checklist.md                  改完自查
references/principles.md      通用写法、按元素写、去 AI 腔
references/examples.md        真实的改前 → 改后和反例
references/sources.md         出处
references/industries/        9 个行业风格 + 模板
references/locale-zh-hant.md  繁体（台湾 / 香港）用词和标点
assets/glossary-template.md   项目术语表模板
scripts/                      提取文案、查测试锚点、自测
evals/                        评测场景（改技能后复测用）
agents/openai.yaml            Codex 的显示信息
```

## 参考

规则参考了 Ant Design、Microsoft、Material、NN/g、Polaris 的写作规范，以及 no-ai-slop、stop-slop、humanizer、renhua、说人话等去 AI 腔项目，完整列表见 [`references/sources.md`](references/sources.md)。

## 许可

[MIT](LICENSE)

---

## English

**zh-ui-copy** is an [Agent Skill](https://agentskills.io) for writing, rewriting, and reviewing user-facing UI copy (buttons, placeholders, empty states, errors, toasts, confirmations, status labels, tooltips, aria-labels, chat-panel replies) and removing AI tone, without breaking your tests.

It works with Claude Code, OpenAI Codex, DeepSeek Harness, and other tools that support the Agent Skills format. The rules are written in Chinese and tuned for Chinese interfaces, but they apply to English copy as well.

What it adds beyond a generic "humanize this" prompt:

- **Honesty rules**: actions with no receipt, hand-offs to other apps, and unconfirmed states have fixed phrasings and are never reported as done.
- **State-by-state review**: loading, success, empty, failure, and truncated results each get checked, so a failed request never shows up as "no data" and a truncated list never reads as a total.
- **Numbers checked against code**: limits, counts, and durations in the copy must match the values in code.
- **Test-safe edits**: `scripts/check_copy_anchors.py` finds test and CI anchors that a copy change will break (BREAK), and negative assertions that will silently always pass (VACUOUS).
- **Per-project conventions**: put your terms, ruled names, and fixed phrasings in `docs/copy-glossary.md`; the skill reads it first.
- **Industry styles**: nine built-in style files (AI, SaaS / developer tools, OS / desktop, mobile apps, finance, healthcare, education, government, industrial) cover tone, terminology, per-element rules, compliance constraints, and high-risk scenarios. The skill picks one in this order: what you tell it, an `行业：<id>` line in your glossary, then `scripts/detect_industry.py`, which scores the repo by dependencies, directory names, and UI vocabulary. To add an industry, copy `references/industries/_TEMPLATE.md`; the detector reads the new file's signals with no code change.
- **Traditional Chinese**: `references/locale-zh-hant.md` covers Taiwan and Hong Kong vocabulary and punctuation, and each industry file has a Taiwan / Hong Kong section on local regulations (for example, Taiwan's Personal Data Protection Act instead of mainland China's PIPL). The detector flags `zh-TW` / `zh-Hant` / `zh-HK` locale files.

**Install**: put this directory in `~/.claude/skills/zh-ui-copy` (Claude Code) or `~/.agents/skills/zh-ui-copy` (Codex, DeepSeek Harness). To share one copy, clone it once and symlink it (on Windows, use a `mklink /J` junction). Python 3.8+ is required for the scripts.

**Use**: `/zh-ui-copy` in Claude Code, `$zh-ui-copy` in Codex, or just ask to review or tighten the copy in a file.

License: [MIT](LICENSE)
