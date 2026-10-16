#!/usr/bin/env python3
"""抽出界面文案：列出源码里含中文的字符串（先去掉注释 / docstring），并标出可疑写法。

用法：
  python extract_ui_strings.py [--min-cjk N] [--only-flagged] [--flags 名字,名字] <文件或目录>...
  python extract_ui_strings.py --attrs <文件或目录>...   # 只列 aria-label / title / placeholder / alt
    （`title={条件 ? "A" : "B"}` 两句都列；`title={变量}` 标 DYNAMIC，要去定义处看）

- .ts / .tsx / .js / .jsx / .mjs / .cjs / .vue：按词法去掉注释，逐行打印含中文的代码行
  （字符串字面量和 JSX 文本都在里面）；
- .py：用 AST 列出字符串字面量（f-string 的插值位写成 {…}），跳过 docstring，
  并标出所在函数或常量名 —— 方便区分「显示给用户的句子」和「写给模型的提示词」；
- 目录递归展开（跳过 node_modules / .next / dist / build / __pycache__ / .git）。

默认标出的写法（--flags 只看其中几类，例如 --flags DASH,STAR）：
  DASH    破折号「——」当连接词（短文案一律不用）
  STAR    markdown 强调「**」（纯文本渲染的面上会连星号一起显示）
  MEIFA   「没法」（界面统一用「无法」）
  ROUND   「这一轮 / 这一条 / 这一批」（卡片上下文里多半多余）
  QUERY   「确认不了 / 改没改 / 看一眼」这类口语套话
  JARGON  开发者用词：产物、改盘、版本链、快照、锚点、线程、盘上、落上、回落、注册名、
          沙箱、引擎、留痕、白名单、端点、字节
"""
from __future__ import annotations

import ast
import os
import re
import sys

CJK = re.compile(r"[一-鿿]")
FLAGS = {
    # 破折号当连接词。单独一个「—」当空值占位（`?? "—"`、表格里的缺省值）不算，见 _dash_text()
    "DASH": re.compile(r"——|—"),
    "STAR": re.compile(r"\*\*"),
    "MEIFA": re.compile(r"没法"),
    "ROUND": re.compile(r"这一轮|这一条|这一批"),
    "QUERY": re.compile(r"确认不了|改没改|看一眼"),
    "JARGON": re.compile(r"产物|改盘|版本链|快照|锚点|线程|盘上|落上|回落|注册名|沙箱|引擎|留痕|白名单|端点|字节"),
}
TS_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue"}

#: 单独成串的「—」：空值占位，不是连接词（`?? "—"`、`'—'`、Python 里整串就是「—」）。
_LONE_DASH = re.compile(r"""(["'`])\s*[—–-]\s*\1""")


def _dash_text(text: str) -> str:
    """判 DASH 之前先去掉空值占位的「—」，别把表格缺省值当成破折号连接词。"""
    if text.strip() in {"—", "–", "-"}:
        return ""
    return _LONE_DASH.sub("", text)
SKIP_DIRS = {"node_modules", ".next", "dist", "build", "__pycache__", ".git", ".venv", "venv"}


def strip_ts_comments(src: str) -> str:
    """按词法去掉 // 与 /* */ 注释，字符串（含模板字符串）原样保留，换行保留。"""
    out, i, n, state, quote = [], 0, len(src), "code", ""
    while i < n:
        c = src[i]
        d = src[i + 1] if i + 1 < n else ""
        if state == "code":
            if c == "/" and d == "/":
                state = "line"
                i += 2
                continue
            if c == "/" and d == "*":
                state = "block"
                i += 2
                continue
            if c in ("'", '"', "`"):
                state, quote = "str", c
            out.append(c)
        elif state == "str":
            out.append(c)
            if c == "\\":
                out.append(d)
                i += 2
                continue
            if c == quote or (c == "\n" and quote != "`"):
                state = "code"
        elif state == "line":
            if c == "\n":
                out.append(c)
                state = "code"
        else:  # block
            if c == "*" and d == "/":
                state = "code"
                i += 2
                continue
            if c == "\n":
                out.append(c)
        i += 1
    return "".join(out)


def ts_rows(path: str):
    src = open(path, encoding="utf-8").read().replace("\r", "")
    for no, line in enumerate(strip_ts_comments(src).split("\n"), 1):
        yield no, "", line.strip()


#: JSX 里这几个属性的文字用户看得见（或读屏器读得出），但混在代码行里不好对照。
#: 前面不许是字母或连字符：`data-title=`、`subtitle=` 不算。
_ATTR_START = re.compile(r"(?<![\w-])(aria-label|title|placeholder|alt)=")
#: 表达式里的字符串字面量："…" / '…' / `…`（模板字符串原样保留 ${…}，看得出插的是哪个变量）
_STR_LIT = re.compile(r'"((?:[^"\\\n]|\\.)*)"' r"|'((?:[^'\\\n]|\\.)*)'" r"|`((?:[^`\\]|\\.)*)`")


def _skip_string(src: str, i: int) -> int:
    """src[i] 是引号：返回这个字符串结束之后的位置。"""
    quote, n = src[i], len(src)
    i += 1
    while i < n:
        c = src[i]
        if c == "\\":
            i += 2
            continue
        if c == quote or (c == "\n" and quote != "`"):
            return i + 1
        i += 1
    return n


def _brace_end(src: str, i: int) -> int:
    """src[i] 是「{」：返回配对的「}」之后的位置，字符串里的括号不算。"""
    depth, n = 0, len(src)
    while i < n:
        c = src[i]
        if c in "\"'`":
            i = _skip_string(src, i)
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


def attr_rows(path: str, minimum: int = 1):
    """`--attrs`：列 aria-label / title / placeholder / alt 的文字，方便和可见文字对照。

    - `attr="…"`：原样列出；
    - `attr={…}`：列出表达式里所有含中文的字面量。三元 `条件 ? "A" : "B"` 两句都列，
      表达式跨行也行，行号记属性所在的那一行；
    - 表达式里一个中文字面量都没有（`title={m.hint}`、`title={t("key")}`）：标 DYNAMIC。
      文字在别处定义，要去定义处看，别当成「这个控件没有文字」。
    """
    src = strip_ts_comments(open(path, encoding="utf-8").read().replace("\r", ""))
    for m in _ATTR_START.finditer(src):
        no = src.count("\n", 0, m.start()) + 1
        attr, i = m.group(1), m.end()
        if i >= len(src):
            continue
        if src[i] in "\"'":
            value = src[i + 1:_skip_string(src, i) - 1]
            if len(CJK.findall(value)) >= minimum:
                yield no, attr, "", value
        elif src[i] == "{":
            expr = src[i + 1:_brace_end(src, i) - 1]
            found = [next(g for g in lit.groups() if g is not None) for lit in _STR_LIT.finditer(expr)]
            found = [t for t in found if len(CJK.findall(t)) >= minimum]
            if not found:
                yield no, attr, "DYNAMIC", " ".join(expr.split())
            for text in found:
                yield no, attr, "", text


def py_rows(path: str):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                docs.add(id(body[0].value))
    owner: dict[int, str] = {}

    def tag(node, name):
        for child in ast.walk(node):
            owner.setdefault(id(child), name)

    for top in tree.body:
        if isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for inner in ast.walk(top):
                if isinstance(inner, (ast.FunctionDef, ast.AsyncFunctionDef)) and inner is not top:
                    tag(inner, f"{top.name}.{inner.name}")
            tag(top, top.name)
        elif isinstance(top, (ast.Assign, ast.AnnAssign)):
            targets = top.targets if isinstance(top, ast.Assign) else [top.target]
            names = [t.id for t in targets if isinstance(t, ast.Name)]
            tag(top, "=" + (names[0] if names else "?"))
    joined_parts = set()
    rows = []
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            text = ""
            for v in node.values:
                joined_parts.add(id(v))
                text += str(v.value) if isinstance(v, ast.Constant) else "{…}"
            rows.append((node.lineno, owner.get(id(node), ""), text))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if id(node) in docs or id(node) in joined_parts:
                continue
            rows.append((node.lineno, owner.get(id(node), ""), node.value))
    for no, who, text in sorted(rows):
        yield no, who, text.replace("\n", "⏎")


def expand(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for f in sorted(files):
                    if os.path.splitext(f)[1] in TS_EXT | {".py"}:
                        yield os.path.join(root, f)
        else:
            yield p


def main(argv):
    minimum, only_flagged, wanted, attrs = 1, False, set(FLAGS), False
    files = []
    it = iter(argv)
    for a in it:
        if a == "--min-cjk":
            minimum = int(next(it))
        elif a == "--only-flagged":
            only_flagged = True
        elif a == "--flags":
            wanted = {x.strip().upper() for x in next(it).split(",") if x.strip()}
        elif a == "--attrs":
            attrs = True
        else:
            files.append(a)
    if not files:
        print(__doc__)
        return 2
    if attrs:
        for path in expand(files):
            if os.path.splitext(path)[1] not in TS_EXT:
                continue
            for no, attr, mark, value in attr_rows(path, minimum):
                tag = f" {mark}" if mark else ""
                print(f"{path.replace(os.sep, '/')}:{no} {attr}{tag} :: {value[:160]}")
        return 0
    for path in expand(files):
        ext = os.path.splitext(path)[1]
        rows = py_rows(path) if ext == ".py" else ts_rows(path) if ext in TS_EXT else []
        for no, who, text in rows:
            if len(CJK.findall(text)) < minimum:
                continue
            hits = [name for name in sorted(wanted)
                    if FLAGS[name].search(_dash_text(text) if name == "DASH" else text)]
            if only_flagged and not hits:
                continue
            where = f" [{who}]" if who else ""
            print(f"{path.replace(os.sep, '/')}:{no}{where} {','.join(hits) or '-'} :: {text[:200]}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    sys.exit(main(sys.argv[1:]))
