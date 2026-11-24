#!/usr/bin/env python
"""把判分结果汇总成 PROTOCOL.md 第 6 节要的三个数。

  python evals/tally.py evals/runs/<stamp>
  python evals/tally.py <目录> --map map.json     # 目录里用 A/B 命名时，给一张对照表
  python evals/tally.py <目录> --evals evals/evals.json   # 再加一段按 scope 分组的数

判分文件命名：<id>-<group>.verdict.json，group 是 with / without。
用 A/B 盲判时，给一张 {"13-A": "with", "13-B": "without"} 的对照表。

三个数：
  逐项通过率   = 1 的数量 ÷ (1 + 0 的数量)，NA 不进分母
  区分度       = with 的通过率 − without 的通过率
  整条全对率   = 没有 0 的 case 数 ÷ 总 case 数

给 --evals 时按 scope 再分一组：只有 scope=project-convention 且 kind=held-out 的题
才算「区分候选」，只有这组数字能拿来外推技能的价值。
"""
import argparse
import glob
import io
import json
import os
import re
import sys


def load_verdicts(path):
    text = io.open(path, encoding="utf-8").read()
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("%s 里没有 JSON" % path)
    return json.loads(m.group(0))["verdicts"]


def norm(v):
    """1 / 0 / 'NA' 归一。多余的写法直接报错，不猜。"""
    if v in (1, "1"):
        return 1
    if v in (0, "0"):
        return 0
    if isinstance(v, str) and v.strip().upper() == "NA":
        return "NA"
    raise ValueError("不认识的判定值：%r" % (v,))


def tally(rows):
    """rows: [(case_id, group, verdict)] → 三个数"""
    agg = {}
    for cid, group, verdict in rows:
        a = agg.setdefault(group, {"pass": 0, "fail": 0, "na": 0, "cases": {}})
        c = a["cases"].setdefault(cid, {"pass": 0, "fail": 0, "na": 0})
        for bucket, key in ((1, "pass"), (0, "fail"), ("NA", "na")):
            if verdict == bucket:
                a[key] += 1
                c[key] += 1
                break

    def rate(d):
        denom = d["pass"] + d["fail"]
        return (d["pass"] / denom) if denom else None

    out = {}
    for group, a in agg.items():
        # 有 NA 的题不算「整条全对」：没判完就是没判完，不能算满分。
        # 同理也不进整条全对率的分母。
        settled = {k: v for k, v in a["cases"].items() if v["na"] == 0}
        allpass = sum(1 for c in settled.values() if c["fail"] == 0 and c["pass"] > 0)
        out[group] = {
            "pass": a["pass"], "fail": a["fail"], "na": a["na"],
            "rate": rate(a),
            "cases": a["cases"],
            "cases_allpass": allpass,
            "cases_counted": len(settled),
            "cases_unsettled": sorted(int(k) for k, v in a["cases"].items()
                                      if v["na"] > 0),
        }
    return out


def main(argv):
    ap = argparse.ArgumentParser(description="汇总评测结果")
    ap.add_argument("dir")
    ap.add_argument("--map", help='盲判对照表 JSON：{"13-A": "with"}')
    ap.add_argument("--evals", help="evals.json 的路径，给了就按 scope 再分组")
    ap.add_argument("--json", action="store_true", help="额外输出机器可读的 JSON")
    args = ap.parse_args(argv)

    mapping = {}
    if args.map:
        mapping = json.loads(io.open(args.map, encoding="utf-8").read())

    files = sorted(glob.glob(os.path.join(args.dir, "*.verdict.json")))
    if not files:
        sys.stderr.write("%s 里没有 *.verdict.json\n" % args.dir)
        return 2

    rows = []
    case_ids = set()
    for path in files:
        base = os.path.basename(path)[: -len(".verdict.json")]
        group = mapping.get(base)
        if not group:
            group = base.rsplit("-", 1)[-1]
        if group not in ("with", "without"):
            sys.stderr.write("%s：认不出对照组 %r\n" % (base, group))
            return 2
        case_id = base.rsplit("-", 1)[0]
        case_ids.add(case_id)
        for i, v in enumerate(load_verdicts(path), 1):
            try:
                rows.append((case_id, group, norm(v.get("verdict"))))
            except ValueError as e:
                sys.stderr.write("%s 第 %d 条：%s\n" % (base, i, e))
                return 2

    result = tally(rows)
    w, wo = result.get("with", {}), result.get("without", {})

    print("case  " + "  ".join("%-14s" % c for c in ("with 通过/失败/NA",
                                                     "without 通过/失败/NA")))
    for cid in sorted(case_ids, key=int):
        cells = []
        for g in ("with", "without"):
            c = result.get(g, {}).get("cases", {}).get(cid)
            cells.append("%d/%d/%d" % (c["pass"], c["fail"], c["na"]) if c else "-")
        print("%-5s %-16s %s" % (cid, cells[0], cells[1]))

    print()
    for g in ("with", "without"):
        d = result.get(g)
        if not d:
            continue
        r = "—" if d["rate"] is None else "%.1f%%" % (d["rate"] * 100)
        print("%-8s 逐项通过率 %s  (1=%d  0=%d  NA=%d)"
              % (g, r, d["pass"], d["fail"], d["na"]))
        if d["cases_counted"]:
            print("%-8s 整条全对率 %.1f%%  (%d/%d 条判完)"
                  % ("", d["cases_allpass"] / d["cases_counted"] * 100,
                     d["cases_allpass"], d["cases_counted"]))
        if d["cases_unsettled"]:
            print("%-8s 有 NA 没判完的题：%s（不进上面的分母）"
                  % ("", d["cases_unsettled"]))

    if w.get("rate") is not None and wo.get("rate") is not None:
        print("\n区分度 %.1f 个百分点（with %.1f%% − without %.1f%%）"
              % ((w["rate"] - wo["rate"]) * 100, w["rate"] * 100, wo["rate"] * 100))
    else:
        print("\n区分度算不出来：有一组没有可判的项")

    if args.evals:
        meta = {str(e["id"]): e
                for e in json.loads(io.open(args.evals, encoding="utf-8").read())["evals"]}
        buckets = {}
        for cid, group, verdict in rows:
            e = meta.get(cid, {})
            usable = (e.get("kind") == "held-out"
                      and e.get("scope") == "project-convention")
            key = (e.get("scope", "?"), "区分候选" if usable else "不作外推")
            g = buckets.setdefault(key, {}).setdefault(
                group, {"pass": 0, "fail": 0, "na": 0})
            for val, name in ((1, "pass"), (0, "fail"), ("NA", "na")):
                if verdict == val:
                    g[name] += 1
                    break

        print("\n按 scope 分组（只有「区分候选」那行能拿来外推技能的价值）：")
        for key in sorted(buckets):
            g = buckets[key]
            dw, dwo = g.get("with", {}), g.get("without", {})
            nw = dw.get("pass", 0) + dw.get("fail", 0)
            nwo = dwo.get("pass", 0) + dwo.get("fail", 0)
            cell_w = "%.1f%%" % (dw["pass"] / nw * 100) if nw else "—"
            cell_wo = "%.1f%%" % (dwo["pass"] / nwo * 100) if nwo else "—"
            gap = ""
            if nw and nwo:
                gap = "  区分度 %+.1fpp" % ((dw["pass"] / nw - dwo["pass"] / nwo) * 100)
            print("  %-20s %-10s with %-7s without %-7s%s"
                  % (key[0], key[1], cell_w, cell_wo, gap))

    na = w.get("na", 0) + wo.get("na", 0)
    if na:
        print("NA 共 %d 条，没进分母，缺的行为证据要另外补" % na)

    if args.json:
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
