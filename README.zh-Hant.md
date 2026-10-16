# zh-ui-copy

[简体中文](README.md) · [English](README.md#english)

給 AI 程式助理用的介面文案技能（[Agent Skill](https://agentskills.io)）：寫、改、審前端文案，去掉 AI 腔，而且改完不會弄壞測試。

支援 Claude Code、OpenAI Codex、DeepSeek Harness，以及其他相容 Agent Skills 規範的工具。規則以簡體中文撰寫，主要針對中文介面；英文文案和繁體介面（台灣、香港）同樣適用。

## 改前 → 改後

| 改前 | 改後 | 問題 |
|---|---|---|
| 讀不到這個檔案：[Errno 2] No such file or directory: '/srv/files/…/x.docx' | 讀取檔案失敗，請再試一次；多次失敗請聯絡管理員。 | 例外原文和伺服器路徑外洩給使用者 |
| 好，這一輪我沒有修改文件。 | 文件沒有變更。 | 助理腔 |
| 檔案的位元組沒有變化 —— 它可能只是回答了你，並沒有修改這份檔案。 | 檔案沒有變化，智慧代理可能只回答了問題，沒有修改檔案。 | 開發者用詞、破折號 |
| 已復原 3 步，文件已恢復 | 已送出 3 步復原，請確認文件是否已恢復。 | 沒有回應結果，卻寫成已完成 |
| 郵件已寄給 3 位聯絡人 ✓ | 郵件已寫好，請在信箱中檢查後寄出。 | 頁面只開啟了信箱，不知道信寄出沒有 |
| 最近對話 · 共 30 個（API 只取了 30 個） | 最近 30 個對話 | 截斷寫成了總數 |
| 上傳文件失敗，請檢查網絡 | 上傳檔案失敗，請檢查網路 | 只換字不換詞，台灣使用者一看就知道是轉出來的 |

更多案例見 [`references/examples.md`](references/examples.md)。

## 它和一般的「去 AI 味」提示詞有什麼不同

- **只說確認過的事**：沒有回應結果的動作、交給別的應用程式做的事、無法確認的狀態，都有固定寫法，不會寫成「已完成」。
- **按狀態審**：載入中、成功、空、失敗、截斷各顯示哪句話。失敗被顯示成「目前沒有資料」、截斷被寫成「共 N 筆」，這類問題逐句讀是讀不出來的。
- **文案裡的數字和程式碼對帳**：上限、筆數、時長，以程式碼裡的值為準。
- **改完不弄壞測試**：`check_copy_anchors.py` 會找出測試和 CI 檢查裡會斷的錨點（BREAK），以及改完後永遠會通過的反向斷言（VACUOUS）。
- **專案慣例可設定**：用詞、使用者裁定過的名稱、固定句式寫進專案的 `docs/copy-glossary.md`，技能會先讀它。
- **行業風格**：內建 9 個行業，自動判斷，見下文。

## 行業風格

銀行要寫清手續費和入帳時間，醫院要分清楚給醫師看還是給病人看，工廠的警報要寫原因、後果和處置。技能內建 9 個行業的風格檔，各含語氣、術語、按元素的寫法、法規硬約束、高風險情境和改前 → 改後：

| id | 行業 | 典型產品 |
|---|---|---|
| `ai` | AI 產品 | 對話助理、Copilot、智慧代理、模型主控台 |
| `software` | 軟體 / SaaS / 開發者工具 | 協作工具、雲端主控台、管理後台、CLI |
| `system` | 作業系統 / 系統軟體 / 桌面應用程式 | 系統設定、安裝更新、資安軟體、瀏覽器 |
| `mobile` | 手機 App / 小程式 | 消費型 App、小程式、手機廠商應用程式 |
| `finance` | 金融 | 銀行、支付、理財、保險、借貸 |
| `medical` | 醫療健康 | HIS / EMR、病患 App、遠距醫療、醫療器材軟體 |
| `education` | 教育 | K12、大專院校、LMS、語言學習、考試 |
| `government` | 政府 / 公共服務 | 政府線上服務、社會保險、稅務、公用事業 |
| `industrial` | 工業 / 製造 / 能源 | HMI / SCADA、MES、IIoT、能源管理 |

**怎麼選**，先到先用：

1. 你直接說：「這是銀行 App」。
2. 專案術語表 `docs/copy-glossary.md` 裡寫一行 `行业：finance`（多個行業用逗號隔開，如 `行业：finance, ai`）。
3. 自動判斷：`python scripts/detect_industry.py <儲存庫目錄>` 依相依套件、目錄名稱、介面用詞評分，★ 是最高分。儲存庫裡有 `zh-TW` / `zh-Hant` / `zh-HK` 語系檔時，它還會提示載入繁體用詞和台港差異。
4. 都沒有：從句子本身判斷，判斷不了就用通用規則。

多個行業同時符合時，法規硬約束全部疊加，語氣以使用者最直接面對的那個行業為準。

**繁體 / 台港**：[`references/locale-zh-hant.md`](references/locale-zh-hant.md) 管用詞和標點（「文件」→「檔案」、「默认」→「預設」）；每份行業檔的「台港市场差异」一節管法規和必須出現的文字，例如台灣借貸要標示總費用年百分率，個資告知依台灣《個人資料保護法》，而不是中國大陸的《個人信息保護法》。

**新增行業**：照 [`references/industries/_TEMPLATE.md`](references/industries/_TEMPLATE.md) 寫一份 `references/industries/<id>.md`。判斷腳本會從新檔案第 1 節讀取訊號，不必改程式。

## 安裝

技能就是一個目錄，放到工具會掃描的位置即可。

| 工具 | 使用者層級目錄 | 專案層級目錄 |
|---|---|---|
| Claude Code | `~/.claude/skills/zh-ui-copy` | `.claude/skills/zh-ui-copy` |
| OpenAI Codex | `~/.agents/skills/zh-ui-copy` | `.agents/skills/zh-ui-copy` |
| DeepSeek Harness | `~/.agents/skills/zh-ui-copy` 或 `~/.dsh/skills/zh-ui-copy` | `.agents/skills/zh-ui-copy` 或 `.dsh/skills/zh-ui-copy` |

三個工具都用的話，複製一份，再連結過去：

```bash
# macOS / Linux
git clone https://github.com/ZheShen00/zh-ui-copy ~/.agents/skills/zh-ui-copy
mkdir -p ~/.claude/skills && ln -s ~/.agents/skills/zh-ui-copy ~/.claude/skills/zh-ui-copy
```

```powershell
# Windows（目錄連接，不需要系統管理員權限）
git clone https://github.com/ZheShen00/zh-ui-copy "$env:USERPROFILE\.agents\skills\zh-ui-copy"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
cmd /c mklink /J "$env:USERPROFILE\.claude\skills\zh-ui-copy" "$env:USERPROFILE\.agents\skills\zh-ui-copy"
```

不要再往 `~/.codex/skills` 放一份副本，否則 Codex 會載入兩次。

需要 Python 3.8 以上（腳本只用標準函式庫）；`check_copy_anchors.py` 需要 git。

## 使用

- Claude Code：`/zh-ui-copy`，或直接說「把這頁文案去一下 AI 味」
- Codex：`$zh-ui-copy`，或在 `/skills` 裡選
- DeepSeek Harness：`/zh-ui-copy`，或直接描述需求

三種工作：

- **審**：「審一下 `src/pages/orders.tsx` 的文案，只列問題」。交付問題清單，不改檔案。
- **改**：「把這幾句錯誤訊息改精簡」。交付改前 → 改後、改了幾處、驗證結果。
- **寫**：「幫上傳失敗寫一句錯誤訊息」。

## 幫你的專案寫術語表

把 [`assets/glossary-template.md`](assets/glossary-template.md) 複製到專案的 `docs/copy-glossary.md`，填上你們的用詞和裁定。`SKILL.md` 裡的「项目约定」是預設值，專案術語表優先。繁體專案可以在術語表裡直接寫繁體用詞，它會蓋過 `locale-zh-hant.md`。

## 腳本

都是唯讀的，不改任何檔案。路徑相對於技能目錄；macOS / Linux 上沒有 `python` 就用 `python3`。

```bash
python scripts/extract_ui_strings.py src/             # 列出介面文字
python scripts/extract_ui_strings.py --attrs src/     # 列出 aria-label / title / placeholder / alt
python scripts/check_copy_anchors.py --base HEAD      # 在儲存庫裡執行：找出改文案會弄斷的測試錨點
python scripts/detect_industry.py <儲存庫目錄>         # 判斷行業、找出繁體介面
python scripts/selftest.py                            # 腳本自我測試
```

## 參考

規則參考了 Ant Design、Microsoft、Material、NN/g、Polaris 的寫作規範，以及 no-ai-slop、stop-slop、humanizer、renhua、說人話、speak-human-tw 等去 AI 腔專案，完整清單見 [`references/sources.md`](references/sources.md)。

## 授權

[MIT](LICENSE)
