#!/usr/bin/env python
"""把盲判的 A/B 产物落成仓库里的正规 run 目录，并写元数据。

  python postprocess.py <临时目录> <目标 run 目录>

产出：
  <目标>/<id>-<group>.md            作答原文
  <目标>/<id>-<group>.verdict.json  判分
  <目标>/map.json                   盲判对照表（事后可查，判分时没给 judge）
  <目标>/meta.json                  模型、日期、commit、口径与偏差
"""
import io
import json
import os
import shutil
import subprocess
import sys


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    src, dst = argv
    mapping = json.loads(io.open(os.path.join(src, "map.json"), encoding="utf-8").read())
    os.makedirs(dst, exist_ok=True)

    copied = judged = missing = 0
    for key, group in sorted(mapping.items(), key=lambda kv: (int(kv[0].split("-")[0]), kv[1])):
        cid = key.split("-")[0]
        for suffix, out_ext in ((".md", ".md"), (".verdict.json", ".verdict.json")):
            a = os.path.join(src, "out", key + suffix)
            b = os.path.join(dst, "%s-%s%s" % (cid, group, out_ext))
            if not os.path.exists(a):
                missing += 1
                continue
            shutil.copyfile(a, b)
            if suffix == ".md":
                copied += 1
            else:
                judged += 1

    shutil.copyfile(os.path.join(src, "map.json"), os.path.join(dst, "map.json"))

    commit = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=os.path.dirname(os.path.dirname(dst)), text=True).strip()
    meta = {
        "run": os.path.basename(dst),
        "commit": commit,
        "date": "2026-11-24",
        # 下面几条是这次跑的偏见项，写进目录里，别人看数之前先看到
        "model": {
            "name": "deepseek-flash",
            "pinned": False,
            "note": "跑在 DSH harness 里，拿不到精确模型版本号；PROTOCOL 第 2 节要求钉死版本，这条不满足",
        },
        "judge": {
            "model": "deepseek-flash（与被测同源）",
            "blind": True,
            "note": "盲编有效，但 judge 与被测同一模型，PROTOCOL 第 5 节要求不同模型，这条不满足",
        },
        "injection": {
            "method": "experiment-A-approx",
            "note": "带技能那组读 SKILL.md，按它自己的指示再按需读 references/；带 harness 框架",
        },
        "isolation": "每组一个干净上下文子代理，分 8 个一批并发",
        "counts": {"answers": copied, "verdicts": judged, "missing": missing},
    }
    with io.open(os.path.join(dst, "meta.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("作答 %d 份，判分 %d 份，缺 %d 份 → %s" % (copied, judged, missing, dst))
    return 0 if missing == 0 else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
