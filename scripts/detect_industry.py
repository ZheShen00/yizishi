#!/usr/bin/env python3
"""猜一个仓库属于哪个行业，决定加载 references/industries/ 下的哪份风格文件。

信号不写在这里：每份行业文件「## 1. 什么时候用这份」一节里的
  - 代码 / 依赖：`包名` …        → 在依赖清单里找（权重 3）
  - 目录 / 文件名：`目录名` …     → 在路径里找（权重 2）
  - 界面里的词：词、词、词        → 在源码文字里找（权重 1）
加一个行业只要加一份 md，不用改这个脚本。

用法：
  python detect_industry.py [仓库目录]         默认当前目录
  python detect_industry.py --json [仓库目录]

输出按分数从高到低列出行业和命中的证据；发现 zh-TW / zh-Hant / zh-HK 语言文件时
多打一行，提醒读繁体用词和台港差异。只读，不改任何文件。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IND_DIR = os.path.join(HERE, "..", "references", "industries")

MANIFESTS = {
    "package.json", "requirements.txt", "pyproject.toml", "Pipfile", "setup.py", "setup.cfg",
    "go.mod", "Cargo.toml", "pom.xml", "build.gradle", "build.gradle.kts", "Podfile",
    "Package.swift", "pubspec.yaml", "composer.json", "Gemfile", "AndroidManifest.xml",
    "Info.plist", "app.json", "project.config.json", "manifest.json", "CMakeLists.txt",
    "vcpkg.json", "conanfile.txt", "packages.config", "Directory.Packages.props",
}
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", "out", "target", "vendor",
             "__pycache__", ".venv", "venv", "coverage", ".idea", ".vscode", "Pods"}
TEXT_EXT = {".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte", ".py", ".java", ".kt", ".swift",
            ".dart", ".go", ".rs", ".cs", ".xml", ".strings", ".json", ".yaml", ".yml",
            ".md", ".html", ".wxml", ".properties", ".arb", ".po", ".resx"}
MAX_FILES = 3000
MAX_BYTES = 200_000
# 繁体语言文件：locales/zh-TW.json、values-zh-rTW/、zh-Hant.lproj、b+zh+Hant/、zh_HK.po …
ZH_HANT = re.compile(r"(?:^|[^a-z])zh[-_+](?:hant|r?tw|r?hk|r?mo)(?:[^a-z]|$)")
DOC_EXT = (".md", ".mdx", ".txt", ".rst", ".html", ".pdf")


def parse_signals(path):
    """从行业文件第 1 节读出三类信号。"""
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^## 1\..*?$(.*?)^## 2\.", text, re.M | re.S)
    if not m:
        return None
    sec = m.group(1)
    deps, dirs, words = set(), set(), set()
    cat = None
    for line in sec.splitlines():
        if not line.strip().startswith("-"):
            continue
        s = line.strip().replace("**", "")
        if not line.startswith((" ", "\t")):
            # 顶层条目决定类别；缩进的子条目沿用上一个顶层条目的类别
            head = s[:16]
            cat = ("deps" if ("代码" in head or "依赖" in head) else
                   "dirs" if ("目录" in head or "文件名" in head) else
                   "words" if "界面" in head else None)
        ticks = re.findall(r"`([^`]+)`", s)
        if cat == "deps":
            deps.update(t.strip() for t in ticks)
        elif cat == "dirs":
            dirs.update(t.strip().strip("/") for t in ticks)
        elif cat == "words" and not line.startswith((" ", "\t")):
            body = s.split("：", 1)[-1] if "：" in s else s.split(":", 1)[-1]
            body = re.sub(r"[（(][^）)]*[）)]", "", body)
            for w in re.split(r"[、，,；;/`「」]|\s{2,}", body):
                w = w.strip(" .。<>")
                if 2 <= len(w) <= 12:
                    words.add(w)
    deps.discard("")
    dirs.discard("")
    return {"deps": deps, "dirs": dirs, "words": words}


def load_industries():
    out = {}
    for fn in sorted(os.listdir(IND_DIR)):
        if fn.endswith(".md") and not fn.startswith("_"):
            sig = parse_signals(os.path.join(IND_DIR, fn))
            if sig:
                out[fn[:-3]] = sig
    return out


def walk(root):
    n = 0
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in fns:
            yield os.path.join(dp, fn)
            n += 1
            if n >= MAX_FILES:
                return


def read(path):
    try:
        if os.path.getsize(path) > MAX_BYTES:
            return ""
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def dep_pattern(dep):
    """依赖名只在清单里「像依赖名」的位置算命中：
    前面是行首（可缩进：requirements.txt、pubspec.yaml、go.mod 的 require 块）、引号、
    XML 标签的「>」（Info.plist 的 <key>、pom.xml 的 <artifactId>）或「.」（android.permission.X）；
    后面跟引号、版本号运算符、「<」或行尾。`@scope/*` 这种结尾的通配按前缀算。
    句中前面是空格的不算：package.json 的 description 里写的 "an ai tool" 不是依赖 ai。"""
    d = dep.lower().strip()
    if d.endswith("/*"):
        body = re.escape(d[:-1]) + r"[\w.-]+"
    else:
        body = re.escape(d)
    return re.compile(r"(?:^[ \t]*|[\"'>.])" + body + r"(?=[\"'\s=<>~^!:;,\[\]]|$)", re.M)


def detect(root, industries):
    manifest_text, path_parts, src_text, hant = [], set(), [], []
    for p in walk(root):
        rel = os.path.relpath(p, root).replace("\\", "/")
        # 繁体文档（README.zh-Hant.md）不代表界面是繁体，只认目录名和语言资源文件
        d, b = os.path.split(rel.lower())
        if ZH_HANT.search(d) or (ZH_HANT.search(b) and not b.endswith(DOC_EXT)):
            hant.append(rel)
        for part in rel.lower().split("/"):
            path_parts.add(part)
            path_parts.add(os.path.splitext(part)[0])
        base = os.path.basename(p)
        if base in MANIFESTS or base.endswith((".csproj", ".plist")):
            manifest_text.append(read(p).lower())
        if os.path.splitext(base)[1].lower() in TEXT_EXT:
            src_text.append(read(p))
    manifest = "\n".join(manifest_text)
    source = "\n".join(src_text)

    results = []
    for ind, sig in industries.items():
        # 依赖里也会写文件名（Info.plist、tauri.conf.json），按路径再找一次
        hit_deps = sorted(d for d in sig["deps"]
                          if dep_pattern(d).search(manifest) or d.lower() in path_parts)
        hit_dirs = sorted(d for d in sig["dirs"] if d.lower().split("/")[-1] in path_parts)
        hit_words = sorted(w for w in sig["words"] if w in source)
        score = 3 * len(hit_deps) + 2 * len(hit_dirs) + len(hit_words)
        results.append({"industry": ind, "score": score, "deps": hit_deps,
                        "dirs": hit_dirs, "words": hit_words[:12]})
    results.sort(key=lambda r: -r["score"])
    return results, hant


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    root = args[0] if args else "."
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    industries = load_industries()
    if not industries:
        print("没有找到行业文件：" + os.path.normpath(IND_DIR))
        return 1
    results, hant = detect(root, industries)
    if as_json:
        print(json.dumps({"industries": results, "zh_hant": hant[:20]},
                         ensure_ascii=False, indent=2))
        return 0
    top = results[0]["score"] if results else 0
    for r in results:
        if r["score"] == 0:
            continue
        mark = "★" if r["score"] == top else ("+" if r["score"] >= max(4, top // 2) else " ")
        print(f"{mark} {r['industry']:<12} {r['score']:>3}  依赖{r['deps']} 目录{r['dirs']} 词{r['words']}")
    if top < 4:
        print("没有明显的行业信号：只用通用规则，或问用户是什么行业。")
    if hant:
        more = f" 等 {len(hant)} 个" if len(hant) > 3 else ""
        print(f"有繁体界面（{', '.join(hant[:3])}{more}）：再读 references/locale-zh-hant.md "
              "和行业文件的「台港市场差异」一节。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
