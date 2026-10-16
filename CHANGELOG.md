# Changelog

## 1.0.1 (2026-10-16)

改名为 yizishi（一字师）。修了代码审查找出的脚本漏洞，自测从 21 条加到 36 条。

- `check_copy_anchors.py`：中文文件名不再被跳过；`git mv` 改名的文件按旧路径取改前内容；也查 `.strings`、`.xml`、`.po`、`.arb`、`.properties`、`.svelte`、`.html` 等资源文件；`.vue` 的 `<!-- -->` 注释先去掉；改到一半、语法错的 `.py` 不再让脚本崩溃
- `extract_ui_strings.py`：正则字面量里的 `/*`、JSX 文本里网址的 `//` 不再被当成注释；带 BOM 或 GBK 编码的文件能读，语法错的 `.py` 跳过而不中断整个目录；`" — "` 这种拼句子的破折号会标 DASH；`--flags` 写错名字、参数缺值时给用法提示
- `detect_industry.py`：缩进的 YAML、XML 标签里、点分的 Android 权限名里的依赖都能认出
- 行业文件复核：改正了几处错误的法条和日期（醫療法第 85 條、衛福部函日期、互联网诊疗监管细则条号、港府网站无障碍要求），删掉查不到出处的厂商条目，EU AI Act 第 50 条按 Regulation (EU) 2026/1744 更新；金融审查项压到 10 条
- 评测 12、13 跑了第一轮，结果记在 `evals/evals.json` 的说明里

## 1.0.0 (2026-10-16)

首次公开发布。

- 审、改、写三种活的流程和交付格式
- 默认项目约定（叫法、固定句式、中文细则），可用项目的 `docs/copy-glossary.md` 覆盖
- 9 个行业风格（AI、软件、系统、手机、金融、医疗、教育、政府、工业），`detect_industry.py` 按仓库信号自动选择
- 繁体界面（zh-TW / zh-HK）用词和标点；每个行业有「台港市场差异」一节（台港法规、必须出现的话、用词差异）；`detect_industry.py` 发现 zh-TW / zh-Hant / zh-HK 语言文件时提示
- 繁体中文 README
- 去 AI 腔规则，含新一代口头禅、讲义腔冒号、被动空主语、对话面板套话、工具残留、可移植套话、无源背书；按作用判断而不按词表命中
- `extract_ui_strings.py`、`check_copy_anchors.py`、`detect_industry.py` 和 21 条自测
- 12 个评测场景（含 2 道繁体题）
- 适配 Claude Code、OpenAI Codex、DeepSeek Harness
