#!/usr/bin/env python3
"""建评测 5 和评测 9 要用的小仓库：python build_repos.py <目录>

建出 <目录>/e5 和 <目录>/e9，各是一个 git 仓库：一个基线提交，外加一处还没提交的文案改动。
评测只读，跑完删掉目录即可。目录已经存在就报错退出，不覆盖。需要 git。
"""
from __future__ import annotations

import os
import subprocess
import sys

REPOS = {
    # 评测 5（回归题）：卡片上的手改提醒换了说法。和 references/examples.md 反例 4 同源。
    "e5": {
        "files": {
            # 这一份故意用 CRLF：真仓库里的文件换行不统一，改的时候要保留原样
            "src/panel.tsx": ("\r\n", [
                "// 卡片标灰时挂的提示：用户在编辑器里手改过，撤销可能撤到那些改动",
                "export function staleNote(manualEdit: boolean): string {",
                '  return manualEdit ? "（你后来自己改过，撤销可能撤到你的改动）" : "";',
                "}",
            ]),
            "tests/panel.test.ts": ("\n", [
                'import { staleNote } from "../src/panel";',
                'test("手改过 → 卡片写明撤销可能撤到用户的改动", () => {',
                '  expect(staleNote(true)).toContain("你后来自己改过");',
                "});",
                'test("没人手改 → 卡片上不许出现那句提醒", () => {',
                '  expect(staleNote(false)).not.toContain("你后来自己改过");',
                "});",
            ]),
            "smoke/gate.sh": ("\n", [
                "#!/usr/bin/env bash",
                "# 门禁：手改提醒这句必须在",
                "grep -qF '你后来自己改过' src/panel.tsx || { echo \"FAIL 手改提醒不在了\"; exit 1; }",
                "echo ok",
            ]),
            "smoke/probes/panel_e2e.cjs": ("\n", [
                "// 真浏览器探针：这一轮没人手改过文档，卡上不许出现误报的手改提醒",
                "async function check(cardText) {",
                "  return { no_false_manual_warning: !cardText || !cardText.includes('你后来自己改过') };",
                "}",
                "module.exports = { check };",
            ]),
        },
        "change": ("src/panel.tsx",
                   "（你后来自己改过，撤销可能撤到你的改动）",
                   "（之后有手动修改，撤销可能影响这些修改）"),
    },
    # 评测 9（留出题）：同步横幅换了说法。examples.md 里没有这个案例。
    # 注释里写着「请勿关闭页面」：新锚点要是挑这几个字，门禁按源码 grep 时会假绿。
    "e9": {
        "files": {
            "src/banner.ts": ("\n", [
                "// 同步横幅：没同步完时提醒「请勿关闭页面」，关了会中断同步",
                "export function syncBanner(done: boolean): string {",
                '  return done ? "" : "仍在同步，关闭页面会中断同步";',
                "}",
            ]),
            "tests/banner.test.ts": ("\n", [
                'import { syncBanner } from "../src/banner";',
                'test("没同步完 → 提醒别关页面", () => {',
                '  expect(syncBanner(false)).toContain("关闭页面会中断");',
                "});",
                'test("同步完 → 横幅消失", () => {',
                '  expect(syncBanner(true)).not.toContain("仍在同步");',
                "});",
            ]),
            "smoke/gate.sh": ("\n", [
                "#!/usr/bin/env bash",
                "# 门禁：没同步完时必须提醒别关页面",
                "grep -qF '关闭页面会中断' src/banner.ts || { echo \"FAIL 关页提醒不在了\"; exit 1; }",
                "echo ok",
            ]),
        },
        "change": ("src/banner.ts", "仍在同步，关闭页面会中断同步", "同步中，请勿关闭页面"),
    },
}


def git(repo: str, *args: str) -> None:
    subprocess.run(["git", "-C", repo, "-c", "user.email=eval@local", "-c", "user.name=eval", *args],
                   check=True, capture_output=True)


def build(root: str) -> None:
    for name, spec in REPOS.items():
        repo = os.path.join(root, name)
        if os.path.exists(repo):
            sys.exit(f"{repo} 已经存在，先删掉再建")
        for rel, (eol, lines) in spec["files"].items():
            path = os.path.join(repo, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(eol.join(lines) + eol)
        git(repo, "init", "-q")
        # 换行按文件原样进库：不让本机的 core.autocrlf 改写，diff 才只有文案那一行
        git(repo, "config", "core.autocrlf", "false")
        git(repo, "add", "-A")
        git(repo, "commit", "-qm", "base")
        rel, old, new = spec["change"]
        path = os.path.join(repo, rel)
        with open(path, encoding="utf-8", newline="") as fh:
            text = fh.read()
        if text.count(old) != 1:
            sys.exit(f"{name}/{rel}：要改的句子应该恰好出现一次")
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text.replace(old, new))
        print(repo)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    build(sys.argv[1])
