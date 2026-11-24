## 结论先说

会挂两处：**一个单测 + 门禁脚本**。另外还有一处探针不会报错，但从此形同虚设。改动本身（面板提示的措辞）没问题，挂的原因全是测试和门禁把**旧文案的字面量**当成了断言对象。

| 检查 | 位置 | 结果 |
| --- | --- | --- |
| 单测「手改过 → 卡片写明撤销可能撤到用户的改动」 | [tests/panel.test.ts:3](tests/panel.test.ts#L3) | ❌ 挂 |
| 单测「没人手改 → 卡片上不许出现那句提醒」 | [tests/panel.test.ts:6](tests/panel.test.ts#L6) | ✅ 过（但已经没意义了） |
| 门禁 `smoke/gate.sh` | [smoke/gate.sh:3](smoke/gate.sh#L3) | ❌ 挂（exit 1，打印 `FAIL 手改提醒不在了`） |
| 真浏览器探针 `panel_e2e.cjs` | [smoke/probes/panel_e2e.cjs:3](smoke/probes/panel_e2e.cjs#L3) | ⚠️ 过，但恒为 true，等于没检查 |

## 逐条原因

旧句 `你后来自己改过` 现在整个仓库只剩三处引用，`src/panel.tsx` 里已经没有了（我 grep 过全仓）：

- **单测第一条**：`expect(staleNote(true)).toContain("你后来自己改过")`。改后返回的是「（之后有手动修改，撤销可能影响这些修改）」，不含旧句 → 断言失败。
- **单测第二条**：`expect(staleNote(false)).not.toContain("你后来自己改过")`。`false` 分支直接返回空串，仍然通过。**所以只会挂一个用例，别看到一条绿就以为没事。** 这条的测试名还是一句「撤销可能撤到用户的改动」，也跟着过时了。
- **门禁**：`grep -qF '你后来自己改过' src/panel.tsx || { echo "FAIL 手改提醒不在了"; exit 1; }`。[src/panel.tsx](src/panel.tsx) 里这个字面量已经被你替换掉了（连 [第 1 行注释](src/panel.tsx#L1) 里也只有「手改过」，没有完整旧句），grep 不匹配 → 门禁直接失败。
- **探针**：`no_false_manual_warning: !cardText.includes('你后来自己改过')`。它只在卡片文本里找**旧**句子，而卡片现在输出新句子，于是这个字段任何时候都是 `true`。它本来是防「没人手改却弹出提醒」的误报的，现在这个防线的语义失效了——真出现误报也抓不到，属于**静默弱化**，比挂掉更难发现。

## 提交层面

不会被拦：仓库里没有 `package.json`、没有测试/构建配置、`.git/hooks` 只有 `*.sample`、`core.hooksPath` 也没设，所以 `git commit` 阶段没有任何钩子会挡你。这两处是在跑单测和跑门禁时挂（CI 或手动跑 `smoke/gate.sh`）。也就是说**你现在提交得上去，但流水线/门禁会红**。

另外 [src/panel.tsx:1](src/panel.tsx#L1) 的注释还写着「撤销可能撤到那些改动」，只是注释、不影响任何检查，但建议和文案一起同步，免得下次有人对着注释找旧句子。

## 建议改法（保留你的新文案）

核心思路：断言行为，别再锁死整句文案；文案收成单一来源。

1) 单测改成语义断言（`撤销`、`手动修改` 这些词新老文案都有，不会再被下一次改词打断）：

```ts
import { staleNote } from "../src/panel";

test("手改过 → 卡片要挂提醒", () => {
  expect(staleNote(true)).not.toBe("");
  expect(staleNote(true)).toContain("撤销");
});

test("没人手改 → 卡片上不许出现提醒", () => {
  expect(staleNote(false)).toBe("");
});
```

2) 门禁别 grep 整句，抓在两版文案里都稳定的片段，或抓「提醒没被删掉」这件事：

```bash
# 方案一：抓稳定片段
grep -qF '撤销可能' src/panel.tsx || { echo "FAIL 手改提醒不在了"; exit 1; }

# 方案二：文案抽成常量后，抓常量名 + 非空字符串
grep -qF 'STALE_NOTE' src/panel.tsx || { echo "FAIL 手改提醒不在了"; exit 1; }
```

3) 探针同步新文案，否则那条检查永远是绿的：

```js
return { no_false_manual_warning: !cardText || !cardText.includes('之后有手动修改') };
```

4) 更彻底的做法是把文案抽成单一常量，测试/探针/门禁都引它，下次改词只动一处：

```ts
// src/panel.tsx
export const STALE_NOTE = "（之后有手动修改，撤销可能影响这些修改）";
export function staleNote(manualEdit: boolean): string {
  return manualEdit ? STALE_NOTE : "";
}
```

注意：单测别写成 `expect(staleNote(true)).toBe(STALE_NOTE)`，那就变成自己验证自己了，保留上面第 1 条那种语义断言。

## 我实际做了什么

- 读了仓库里被 git 跟踪的 4 个文件（[src/panel.tsx](src/panel.tsx)、[tests/panel.test.ts](tests/panel.test.ts)、[smoke/gate.sh](smoke/gate.sh)、[smoke/probes/panel_e2e.cjs](smoke/probes/panel_e2e.cjs)）。
- `git status` / `git diff`：确认只有 `src/panel.tsx` 一处未提交修改，改的正是那句提示。
- 仓库没有 package.json、没有 vitest/jest 依赖，所以我没法把测试套件真跑起来；我改用脚本按**真实返回值**逐条复算三处断言的判定：`staleNote(true)` 不含旧句（第一条挂）、`staleNote(false)` 为空（第二条过）、`src/panel.tsx` 不含旧句（门禁挂）、探针恒为 true。结论与上表一致。
- 门禁脚本本体是 bash，我没在 Windows 上直接跑，但 `grep -qF` 的条件我按原样在文件内容上验证过，结果就是不匹配。
