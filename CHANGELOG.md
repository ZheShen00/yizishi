# Changelog

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
