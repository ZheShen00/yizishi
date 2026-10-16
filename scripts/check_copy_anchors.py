#!/usr/bin/env python3
"""改完界面文案之后，查测试 / 门禁 / 探针里锚在旧句子上的字面量。

用法（改动已经落到工作树；--base 是改之前的那个提交，默认 HEAD）：
  python check_copy_anchors.py [--root 仓库根] [--base HEAD] [--test-glob 模式 ...]

报两类问题：
  BREAK    测试里的字面量：改前产品代码里有、改后产品代码里哪儿都没有 → 这条锚会断
  VACUOUS  反向断言（not.toContain / not.toMatch / queryBy…toBeNull / `not in` / assertNotIn /
           `! grep`）的字面量：改前有、改后没有 → 它从此永远通过，什么都没测。
           这一类不会红，只会悄悄失效 —— 必须换成新句子里对应的片段。

比「grep 一下旧句子」多做的三件事（都是踩出来的）：
  1. 产品代码先去掉注释和 docstring 再比 —— 旧字眼只剩在注释里时，按全文查会误判成「还在」；
  2. 反向断言单独报；
  3. 测试文件一律按工作树里的版本看（同一批里改过的测试按改后的算）。

它查不到的（还得靠真跑测试和门禁）：
  - 按函数源码查的门禁（inspect.getsource(某函数)）—— 旧字眼可能还在同一文件的别处；
  - 运行时拼出来的句子、从别的服务返回的句子；
  - 锚点形状在多处出现导致的假绿（写完判据先 grep -c 数一下，命中不是 1 就再收紧）。
"""
from __future__ import annotations

import ast
import fnmatch
import io
import os
import re
import subprocess
import sys
import tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from extract_ui_strings import HTML_EXT, read_source, strip_html_comments, strip_ts_comments  # noqa: E402

CJK = re.compile(r"[一-鿿]")
SCRIPT_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte"}
#: 界面文案常住的地方：代码、配置，以及 Android / iOS / gettext / Flutter / Java 的资源文件
PRODUCT_EXT = SCRIPT_EXT | {".py", ".json", ".yaml", ".yml", ".html", ".htm", ".xml", ".strings",
                            ".po", ".arb", ".properties", ".resx", ".wxml"}
DEFAULT_TEST_GLOBS = [
    "*/tests/*", "tests/*", "*/__tests__/*", "*.test.*", "*.spec.*", "*/test_*.py", "test_*.py",
    "*_test.py", "smoke/*", "e2e/*", "*/e2e/*", ".context/*.cjs",
]
LITERALS = [
    re.compile(r'"([^"\\\n]{2,160})"'),
    re.compile(r"'([^'\\\n]{2,160})'"),
    re.compile(r"`([^`\\]{2,160})`"),
    re.compile(r"/([^/\n*]{2,160})/[gimsuy]*[,)\s.;]"),
]
NEGATIVE = re.compile(
    r"not\.toContain|not\.toMatch|not\.toHaveTextContent|queryBy\w*\(.*\)\)?\.toBeNull|"
    r"\bnot\s+in\b|assertNotIn|!\s*grep\b|\.not\.|"
    r"!\s*[\w.$()\[\]'\"]+\.(includes|contains|startsWith|endsWith)\(|"   # !text.includes('…')
    r"grep\s+-q\w*\s.*&&\s*fail"                                           # grep -q '…' && fail
)
SHELL_EXT = {".sh", ".bash", ""}


def strip_test_comments(path: str, src: str) -> str:
    """测试 / 门禁文件也先去掉注释（保留行号）：注释里用引号引用旧句子不是锚点。"""
    ext = os.path.splitext(path)[1]
    if ext in SHELL_EXT:
        return "\n".join("" if ln.lstrip().startswith("#") else ln for ln in src.split("\n"))
    if ext in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}:
        return strip_ts_comments(src)
    if ext == ".py":
        lines = src.split("\n")
        try:
            for tok in tokenize.generate_tokens(io.StringIO(src).readline):
                if tok.type == tokenize.COMMENT:
                    row, col = tok.start
                    lines[row - 1] = lines[row - 1][:col]
            tree = ast.parse(src)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    body = getattr(node, "body", [])
                    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                            and isinstance(body[0].value.value, str):
                        for r in range(body[0].lineno - 1, body[0].end_lineno):
                            lines[r] = ""
        except (SyntaxError, tokenize.TokenError):
            pass
        return "\n".join(lines)
    return src


def git(root, *args, check=True):
    # core.quotePath=false：中文路径原样输出，不然会变成带引号的 "\346\226\207…" 被当成别的扩展名
    out = subprocess.run(["git", "-C", root, "-c", "core.quotePath=false", *args], capture_output=True)
    if check and out.returncode != 0:
        raise SystemExit(out.stderr.decode("utf-8", "replace"))
    return out.stdout.decode("utf-8", "replace")


def is_test(path, globs):
    p = path.replace("\\", "/")
    return any(fnmatch.fnmatch(p, g) for g in globs)


def py_strings(src: str) -> str:
    """Python：只留非 docstring 的字符串常量（注释本来就不在 AST 里）。"""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        # 解析不了（改到一半的文件）就退一步：去掉注释 token，整份留着；连 token 都切不开就只去整行注释
        out = []
        try:
            for tok in tokenize.generate_tokens(io.StringIO(src).readline):
                if tok.type != tokenize.COMMENT:
                    out.append(tok.string)
        except (tokenize.TokenError, SyntaxError):
            return "\n".join(ln for ln in src.split("\n") if not ln.lstrip().startswith("#"))
        return " ".join(out)
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                docs.add(id(body[0].value))
    parts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            parts.append("".join(str(v.value) if isinstance(v, ast.Constant) else "{}" for v in node.values))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docs:
            parts.append(node.value)
    return "\n".join(parts)


def product_text(path: str, src: str) -> str:
    ext = os.path.splitext(path)[1]
    src = src.replace("\r\n", "\n")
    if ext == ".py":
        return py_strings(src)
    if ext in HTML_EXT:
        src = strip_html_comments(src)
    if ext in SCRIPT_EXT or ext in {".html", ".htm", ".strings"}:
        return strip_ts_comments(src)
    if ext in {".po", ".properties"}:
        return "\n".join(ln for ln in src.split("\n") if not ln.lstrip().startswith(("#", "!")))
    return src


def read(root, path):
    full = os.path.join(root, path)
    if not os.path.isfile(full):
        return None
    return read_source(full)


def main(argv):
    root, base, globs = ".", "HEAD", list(DEFAULT_TEST_GLOBS)
    it = iter(argv)
    for a in it:
        if a in ("--root", "--base", "--test-glob"):
            value = next(it, None)
            if value is None:
                print(f"{a} 后面要跟一个值\n\n{__doc__}", file=sys.stderr)
                return 2
            if a == "--root":
                root = value
            elif a == "--base":
                base = value
            else:
                globs.append(value)
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
    root = git(root, "rev-parse", "--show-toplevel").strip()

    # 改名（git mv）的文件，改前的内容要按旧路径取
    old_path: dict[str, str] = {}
    changed = []
    for line in git(root, "diff", "--name-status", "-M", base).splitlines():
        parts = line.split("\t")
        if len(parts) == 3 and parts[0].startswith(("R", "C")):
            old_path[parts[2]] = parts[1]
            changed.append(parts[2])
        elif len(parts) == 2:
            changed.append(parts[1])
    changed += [p for p in git(root, "ls-files", "--others", "--exclude-standard").splitlines() if p]
    product_changed = [p for p in changed if not is_test(p, globs) and os.path.splitext(p)[1] in PRODUCT_EXT]
    if not product_changed:
        print(f"没有相对 {base} 改动过的产品代码文件，没什么可查。")
        return 0

    pre, post = [], []
    for p in product_changed:
        old = git(root, "show", f"{base}:{old_path.get(p, p)}", check=False)
        new = read(root, p) or ""
        pre.append(product_text(p, old))
        post.append(product_text(p, new))
    pre_text, post_text = "\n".join(pre), "\n".join(post)
    changed_set = set(product_changed)

    tests = [p for p in git(root, "ls-files").splitlines() if is_test(p, globs)]
    tests += [p for p in changed if is_test(p, globs) and p not in tests]
    seen_lit: dict[str, bool] = {}
    breaks, vacuous = [], []
    for t in tests:
        src = read(root, t)
        if src is None:
            continue
        stripped = strip_test_comments(t, src.replace("\r\n", "\n")).split("\n")
        for no, line in enumerate(stripped, 1):
            # 反向写法常常跨行（`grep -qF '…' f \` 换行 `&& fail`）：只在本行用 `\` 续行时连下一行一起认
            continued = line.rstrip().endswith("\\") and no < len(stripped)
            context = line + (" " + stripped[no] if continued else "")
            for pat in LITERALS:
                for lit in pat.findall(line):
                    if len(CJK.findall(lit)) < 2:
                        continue
                    if lit not in seen_lit:
                        gone = lit in pre_text and lit not in post_text
                        if gone:
                            # 还可能活在没改动的产品文件里（去掉注释之后再认）
                            hits = git(root, "grep", "-l", "-F", "-e", lit, "--", ".", check=False).splitlines()
                            for h in hits:
                                if h in changed_set or is_test(h, globs) or os.path.splitext(h)[1] not in PRODUCT_EXT:
                                    continue
                                if lit in product_text(h, read(root, h) or ""):
                                    gone = False
                                    break
                        seen_lit[lit] = gone
                    if seen_lit[lit]:
                        (vacuous if NEGATIVE.search(context) else breaks).append(f"{t}:{no}  「{lit[:70]}」")
    for label, rows in (("BREAK", breaks), ("VACUOUS", vacuous)):
        for r in sorted(set(rows)):
            print(f"{label}  {r}")
    print(f"--- {len(set(breaks))} 条锚会断，{len(set(vacuous))} 条反向断言会失效"
          f"（对比 {base}，查了 {len(product_changed)} 个产品文件、{len(tests)} 个测试文件）")
    if breaks:
        print("    BREAK 也看一眼：测试夹具里碰巧和旧句子重合的字面量（自己造的输入，不是去找产品里的句子）是误报。"
              "门禁按源码 grep 的，新锚点最好限定在字符串字面量里（grep -qE '\"[^\"]*片段[^\"]*\"'），"
              "至少别挑注释里也有的片段，否则句子删了门禁照样绿。")
    if vacuous:
        print("    VACUOUS 要逐条人工判断：如果它守的是「这句错的写法不许回来」（故意删掉的旧写法），"
              "失效是对的、保留；如果它守的是「这时不许出现那句提示」而那句提示只是换了说法，"
              "优先改成断言精确值（toBe(\"\")、元素不存在），做不到精确时才换成新说法里对应的片段。")
    return 1 if (breaks or vacuous) else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    sys.exit(main(sys.argv[1:]))
