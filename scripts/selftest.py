#!/usr/bin/env python3
"""一条命令验证三个脚本还认得出踩过的坑：python selftest.py（全过退出码 0）。

在临时目录里建一个小 git 仓库，放进这些情形，逐条断言：
  extract_ui_strings.py
    - 当连接词的「——」「 — 」要标 DASH；表格空值占位 `?? "—"`、范围「1–20」不标
    - --attrs 列得出 aria-label / placeholder；`title={条件 ? "A" : "B"}` 两句都列（可以跨行）；
      `title={变量}` 标 DYNAMIC；`data-title` 不算
  check_copy_anchors.py
    - 旧字眼只剩在注释 / docstring 里 → 仍判 BREAK（按全文查会误判成「还在」）
    - 反向断言（not.toContain、!x.includes、跨行 grep … && fail）→ VACUOUS
    - 测试自己造的夹具、没改动的文件代码里还在用的句子 → 不报
    - shell 注释里用引号引的旧句子 → 不报
  detect_industry.py
    - 依赖 + 目录 + 界面词能选出行业；依赖里写的文件名（Info.plist）按路径找
    - package.json 的 description 里出现 ai 这个词不算依赖
    - 有 zh-TW / zh-Hant / zh-HK 语言文件时列出来；只有简体时不列
    - 缩进 YAML、XML 标签、点分权限名里的依赖都认得
  2026-10-16 代码审查补的：正则 / JSX 网址里的 // 不当注释；BOM、GBK、语法错的文件不中断扫描；
    .vue 的 <!-- --> 注释；参数写错给用法；中文文件名、git mv 改名、strings.xml 资源文件都查得到
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def run(*args, cwd=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    out = subprocess.run(args, cwd=cwd, capture_output=True, env=env)
    return out.returncode, out.stdout.decode("utf-8", "replace")


def run_all(*args):
    """stdout 和 stderr 一起收：脚本崩了 Traceback 在 stderr 里。"""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    out = subprocess.run(args, capture_output=True, env=env)
    return out.returncode, (out.stdout + out.stderr).decode("utf-8", "replace")


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def git(root, *args):
    return run("git", "-C", root, "-c", "user.email=t@t", "-c", "user.name=t", *args)


def main() -> int:
    failures = []

    def check(label, ok):
        print(("PASS  " if ok else "FAIL  ") + label)
        if not ok:
            failures.append(label)

    with tempfile.TemporaryDirectory() as root:
        # ── extract_ui_strings ──────────────────────────────────────────────
        write(root, "ui/sample.tsx",
              'export const a = `销量 ${n} · 详情 ${String(r["更新日期"] ?? "—")}`;\n'
              'export const b = "没有符合筛选条件的商家 —— 放宽条件或清空筛选。";\n'
              'export const d = "第 1–20 条 / 共 99 条";\n'
              'export const e = "找不到这一段 — 插入没有执行";\n'
              'export const f = <input aria-label="搜索店铺" placeholder="搜索店铺名" />;\n')
        _, out = run(sys.executable, os.path.join(HERE, "extract_ui_strings.py"),
                     "--flags", "DASH", os.path.join(root, "ui/sample.tsx"))
        # ★行号别用 split(":") 取：Windows 路径里有盘符「C:」，切出来的是路径，
        #   两条断言会因此一条假红、一条假绿（第一版就是这么写错的）。
        flagged = {m.group(1) for line in out.splitlines() if " DASH ::" in line
                   for m in [re.search(r"sample\.tsx:(\d+)\b", line)] if m}
        check("DASH：连接词「——」「 — 」被标出", {"2", "4"} <= flagged)
        check("DASH：空值占位「—」和范围「1–20」不标", not ({"1", "3"} & flagged))
        _, out = run(sys.executable, os.path.join(HERE, "extract_ui_strings.py"),
                     "--attrs", os.path.join(root, "ui/sample.tsx"))
        check("--attrs：列出 aria-label 与 placeholder",
              "aria-label :: 搜索店铺" in out and "placeholder :: 搜索店铺名" in out)
        # 2026-09-30 评测里漏掉的两种写法：表达式里的三元、只引用变量
        write(root, "ui/attrs.tsx",
              'export const g = <th title={on ? "按数值排序" : "按文本排序"}>列</th>;\n'
              'export const h = <ToggleGroupItem title={m.hint} value="x" />;\n'
              'export const k = <button\n'
              '  aria-label={\n'
              '    open ? "收起筛选" : "展开筛选"\n'
              '  }\n'
              '/>;\n'
              'export const z = <div data-title="不是可见文字" />;\n')
        _, out = run(sys.executable, os.path.join(HERE, "extract_ui_strings.py"),
                     "--attrs", os.path.join(root, "ui/attrs.tsx"))
        check("--attrs：三元表达式里的两句都列出",
              "title :: 按数值排序" in out and "title :: 按文本排序" in out)
        check("--attrs：只引用变量的标 DYNAMIC", "title DYNAMIC :: m.hint" in out)
        check("--attrs：跨行的表达式记在属性所在那一行",
              re.search(r"attrs\.tsx:4 aria-label :: 收起筛选", out) is not None
              and re.search(r"attrs\.tsx:4 aria-label :: 展开筛选", out) is not None)
        check("--attrs：data-title 不算", "不是可见文字" not in out)

        # ── check_copy_anchors ─────────────────────────────────────────────
        repo = os.path.join(root, "repo")
        os.makedirs(repo)
        git(repo, "init", "-q")
        write(repo, "src/cell.py",
              "# 注释里写着：存回时会丢的部件\n"
              "def inspect_book():\n"
              '    """docstring 里也写着 存回时会丢"""\n'
              '    return "这份工作簿里有我们存回时会丢的东西，所以这里拒绝。"\n')
        write(repo, "src/panel.tsx",
              '// 卡片标灰时的提示\n'
              'export const stale = "（你后来自己改过，撤销可能撤到你的改动）";\n')
        write(repo, "src/untouched.ts",
              "// 注释里提到旧叫法：没法确认这一条\n"
              'export const keep = "这句不改：原文还在";\n')
        write(repo, "src/ops.ts", 'export const why = "没法确认这一条是否生效。";\n')
        write(repo, "tests/test_cell.py",
              "from src.cell import inspect_book\n"
              "def test_refuses():\n"
              '    assert "存回时会丢" in inspect_book()\n'
              "def test_fixture():\n"
              '    fixture = "测试自己造的一句夹具"\n'
              '    assert "自己造的" in fixture\n')
        write(repo, "tests/panel.test.ts",
              'expect(card).toContain("你后来自己改过");\n'
              'expect(other).not.toContain("你后来自己改过");\n'
              'const clean = !cardText.includes("你后来自己改过");\n'
              'expect(keep).toContain("原文还在");\n'
              'expect(x).toContain("没法确认这一条");\n')
        write(repo, "smoke/gate.sh",
              "# 注释里引用旧句子不是锚：\"没法确认这一条\"\n"
              "grep -qF '你后来自己改过' src/panel.tsx \\\n"
              "  && fail \"旧提示回来了\"\n")
        git(repo, "add", "-A")
        git(repo, "commit", "-qm", "base")
        # 只改字符串，注释和 docstring 原样不动
        for rel, old, new in (
            ("src/cell.py", '"这份工作簿里有我们存回时会丢的东西，所以这里拒绝。"', '"工作簿含保存时会丢失的内容，无法编辑。"'),
            ("src/panel.tsx", "（你后来自己改过，撤销可能撤到你的改动）", "（之后有手动修改，撤销可能影响这些修改）"),
            ("src/ops.ts", "没法确认这一条是否生效。", "无法确认是否生效。"),
        ):
            path = os.path.join(repo, rel)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text.replace(old, new))
        _, out = run(sys.executable, os.path.join(HERE, "check_copy_anchors.py"), "--root", repo)
        rows = [line for line in out.splitlines() if line.startswith(("BREAK", "VACUOUS"))]

        def has(kind, where, lit):
            return any(r.startswith(kind) and where in r and lit in r for r in rows)

        check("BREAK：旧字眼只剩在注释 / docstring 里仍判会断", has("BREAK", "tests/test_cell.py:3", "存回时会丢"))
        check("BREAK：正向断言锚着改掉的句子", has("BREAK", "tests/panel.test.ts:1", "你后来自己改过"))
        check("BREAK：只在没改动文件的注释里还有，也判会断", has("BREAK", "tests/panel.test.ts:5", "没法确认这一条"))
        check("VACUOUS：not.toContain", has("VACUOUS", "tests/panel.test.ts:2", "你后来自己改过"))
        check("VACUOUS：!x.includes(...)", has("VACUOUS", "tests/panel.test.ts:3", "你后来自己改过"))
        check("VACUOUS：跨行 grep … && fail", has("VACUOUS", "smoke/gate.sh:2", "你后来自己改过"))
        check("不报：测试自己造的夹具", not any("自己造的" in r for r in rows))
        check("不报：没改动的文件代码里还在用的句子", not any("原文还在" in r for r in rows))
        check("不报：shell 注释里引用的旧句子", not any("smoke/gate.sh:1" in r for r in rows))

    # ── 2026-10-16 代码审查找出的漏洞 ─────────────────────────────────────
    with tempfile.TemporaryDirectory() as root:
        ext = os.path.join(HERE, "extract_ui_strings.py")
        write(root, "ui/regex.tsx",
              'export const p = path.replace(/\\/*$/, "");\n'
              'export const a = "保存成功";\n'
              'export const j = <p>访问 https://x.com 获取帮助</p>;\n'
              'const r = x / 2; // 注释里的中文不该列出\n'
              'export const s = "标题" + " — " + detail;\n')
        _, out = run(sys.executable, ext, os.path.join(root, "ui/regex.tsx"))
        check("extract：正则字面量里的 /* 不当注释开头", "保存成功" in out)
        check("extract：JSX 文本里的 https:// 不当注释", "获取帮助" in out)
        check("extract：除号后面的 // 注释照样去掉", "注释里的中文" not in out)
        check("DASH：带空格的「 — 」当连接词要标",
              re.search(r"regex\.tsx:5 DASH ::", out) is not None)

        write(root, "enc/a_bom.py", "﻿MSG = \"带 BOM 的文件\"\n")
        with open(os.path.join(root, "enc/b_gbk.ts"), "wb") as fh:
            fh.write('export const g = "国标编码的文件";\n'.encode("gbk"))
        write(root, "enc/c_broken.py", 'MSG = """没闭合的三引号\n')
        write(root, "enc/d_after.ts", 'export const z = "后面的文件";\n')
        write(root, "enc/e_page.vue",
              "<template>\n  <!-- 模板注释不是文案 -->\n  <p>页面上的字</p>\n</template>\n")
        code, out = run_all(sys.executable, ext, os.path.join(root, "enc"))
        check("extract：BOM、GBK、语法错的文件不中断整个目录",
              code == 0 and "Traceback" not in out and "后面的文件" in out and "带 BOM 的文件" in out)
        check("extract：GBK 文件也能读出中文", "国标编码的文件" in out)
        check("extract：.vue 的 <!-- --> 注释不列", "模板注释" not in out and "页面上的字" in out)
        code, out = run_all(sys.executable, ext, "--flags", "DASH,JARGN", os.path.join(root, "enc"))
        check("extract：--flags 写错名字给用法提示，不崩", code == 2 and "Traceback" not in out)
        code, out = run_all(sys.executable, ext, "--min-cjk")
        check("extract：参数缺值给用法提示，不崩", code == 2 and "Traceback" not in out)

        repo = os.path.join(root, "repo2")
        os.makedirs(repo)
        git(repo, "init", "-q")
        write(repo, "src/文案.ts", 'export const m = "中文路径旧句子";\n')
        write(repo, "tests/文案.test.ts", 'expect(x).toContain("中文路径旧句子");\n')
        write(repo, "src/old.ts", 'export const r = "改名前的句子";\n')
        write(repo, "tests/rename.test.ts", 'expect(x).toContain("改名前的句子");\n')
        write(repo, "src/page.vue", "<template>\n  <!-- 页面旧提示 -->\n  <p>页面旧提示</p>\n</template>\n")
        write(repo, "tests/page.test.ts", 'expect(x).toContain("页面旧提示");\n')
        write(repo, "res/values/strings.xml", '<resources><string name="a">安卓旧文案</string></resources>\n')
        write(repo, "tests/strings.test.ts", 'expect(x).toContain("安卓旧文案");\n')
        write(repo, "src/broken.py", 'MSG = "坏文件旧句"\n')
        git(repo, "add", "-A")
        git(repo, "commit", "-qm", "base")
        git(repo, "mv", "src/old.ts", "src/new.ts")
        for rel, text in (
            ("src/文案.ts", 'export const m = "新的句子";\n'),
            ("src/new.ts", 'export const r = "改名后";\n'),
            ("src/page.vue", "<template>\n  <!-- 页面旧提示 -->\n  <p>新提示</p>\n</template>\n"),
            ("res/values/strings.xml", '<resources><string name="a">安卓新文案</string></resources>\n'),
            ("src/broken.py", 'MSG = """坏文件新句\n'),
        ):
            write(repo, rel, text)
        code, out = run_all(sys.executable, os.path.join(HERE, "check_copy_anchors.py"), "--root", repo)
        rows = [line for line in out.splitlines() if line.startswith(("BREAK", "VACUOUS"))]
        check("anchors：语法错的 .py 不崩", "Traceback" not in out and code in (0, 1))
        check("anchors：中文文件名的改动和测试都查得到", any("文案.test.ts:1" in r for r in rows))
        check("anchors：git mv 改名的文件按旧路径取改前内容", any("rename.test.ts:1" in r for r in rows))
        check("anchors：.vue 的 <!-- --> 注释里还有旧句子也判会断", any("page.test.ts:1" in r for r in rows))
        check("anchors：strings.xml 这类资源文件也查", any("strings.test.ts:1" in r for r in rows))

    # ── detect_industry：信号来自 references/industries/*.md 第 1 节 ──────────
    with tempfile.TemporaryDirectory() as root:
        def top(repo):
            _, out = run(sys.executable, os.path.join(HERE, "detect_industry.py"), "--json",
                         os.path.join(root, repo))
            res = json.loads(out)["industries"]
            return res[0]["industry"] if res and res[0]["score"] >= 4 else None

        write(root, "a/package.json", '{"dependencies": {"openai": "^4", "react": "18"}}\n')
        write(root, "a/src/agents/chat.ts", 'export const s = "停止生成";\n')
        write(root, "m/ios/Info.plist", "<key>NSCameraUsageDescription</key>\n")
        write(root, "m/android/AndroidManifest.xml", "<uses-permission/>\n")
        write(root, "p/package.json", '{"description": "an ai tool", "dependencies": {"react": "18"}}\n')
        write(root, "p/src/a.ts", 'export const s = "保存";\n')
        check("detect_industry：依赖 + 目录 + 界面词 → ai", top("a") == "ai")
        check("detect_industry：依赖里写的文件名按路径找（Info.plist）→ mobile", top("m") == "mobile")
        check("detect_industry：description 里的单词 ai 不算依赖，没信号就不选", top("p") is None)

        write(root, "f/pubspec.yaml", "dependencies:\n  permission_handler: ^11.0.0\n")
        write(root, "f/ios/Runner/Info.plist", "<dict>\n\t<key>NSCameraUsageDescription</key>\n</dict>\n")
        write(root, "f/android/app/src/main/AndroidManifest.xml",
              '<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>\n')
        _, out = run(sys.executable, os.path.join(HERE, "detect_industry.py"), "--json",
                     os.path.join(root, "f"))
        mob = next(r for r in json.loads(out)["industries"] if r["industry"] == "mobile")
        check("detect_industry：缩进 YAML、XML 标签、点分权限名里的依赖都认得",
              {"permission_handler", "NSCameraUsageDescription", "ACCESS_FINE_LOCATION"} <= set(mob["deps"]))

        def hant(repo):
            _, out = run(sys.executable, os.path.join(HERE, "detect_industry.py"), "--json",
                         os.path.join(root, repo))
            return json.loads(out)["zh_hant"]

        write(root, "t/web/locales/zh-TW.json", "{}\n")
        write(root, "t/android/res/values-zh-rHK/strings.xml", "<resources/>\n")
        write(root, "t/ios/zh-Hant.lproj/Localizable.strings", "\n")
        write(root, "t/web/locales/zh-CN.json", "{}\n")
        write(root, "t/docs/README.zh-Hant.md", "# 說明\n")
        found = hant("t")
        check("detect_industry：zh-TW.json、values-zh-rHK、zh-Hant.lproj 都认出是繁体",
              len(found) == 3 and not any("zh-CN" in f for f in found))
        check("detect_industry：只有简体（zh-CN）时不提示繁体", hant("a") == [] and hant("p") == [])

    print(f"--- {'全部通过' if not failures else f'{len(failures)} 条没过'}")
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    sys.exit(main())
