#!/usr/bin/env python
"""跑评测：同一条题，带技能 / 不带技能各跑一次，落盘等人判。

  python evals/run.py --only 13 --dry-run     # 不调模型，只把两组 prompt 落盘
  python evals/run.py --only 13               # 调模型，真跑一条
  python evals/run.py                         # 跑全部 12 条 × 2 组

规矩在 evals/PROTOCOL.md，这份脚本只执行规矩，不改规矩。
只用标准库，和 scripts/ 下的脚本保持一致。
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)

# 不带技能那组的 system prompt。刻意保持中性：不给任何文案领域提示，
# 否则基线被抬高，区分度就假了。改动这里等于改结论，要同步写进 REPORT.md。
NEUTRAL_SYSTEM = "你是一个编程助手。"


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def git_commit():
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=SKILL_DIR, text=True)
        return out.strip()
    except Exception:
        return "nogit"


def build_runs(case, groups):
    """一条题 → 两组 (group, system, user)。两组只有 system 不同。"""
    user = case["prompt"]
    if case.get("setup"):
        user += "\n\n（环境说明：%s）" % case["setup"]
    out = []
    if "with" in groups:
        out.append(("with", read_text(os.path.join(SKILL_DIR, "SKILL.md")), user))
    if "without" in groups:
        out.append(("without", NEUTRAL_SYSTEM, user))
    return out


def markdown(case, group, system, user, model, commit, started):
    head = [
        "---",
        "case: %s" % case["id"],
        "kind: %s" % case["kind"],
        "group: %s" % group,
        "model: %s" % model,
        "commit: %s" % commit,
        "started: %s" % started.isoformat(timespec="seconds"),
        "---",
        "",
    ]
    body = [
        "## system prompt",
        "",
        "````text",
        system,
        "````",
        "",
        "## user prompt",
        "",
        "````text",
        user,
        "````",
        "",
        "## output",
        "",
    ]
    return "\n".join(head + body)


def call_anthropic(model, system, user, max_tokens):
    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "temperature": 0,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "content-type": "application/json",
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode())
    return "".join(b.get("text", "") for b in data.get("content", []))


def call_openai(model, system, user, max_tokens, base_url):
    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }).encode()
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=body,
        headers={
            "content-type": "application/json",
            "authorization": "Bearer " + os.environ["OPENAI_API_KEY"],
        },
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode())
    return data["choices"][0]["message"]["content"]


def main(argv):
    ap = argparse.ArgumentParser(description="跑 yizishi 评测")
    ap.add_argument("--only", type=int, action="append",
                    help="只跑这些 id，可重复：--only 13 --only 5")
    ap.add_argument("--group", choices=["with", "without", "both"], default="both")
    ap.add_argument("--dry-run", action="store_true",
                    help="不调模型，只把两组 prompt 落盘，用来检查注入是否正确")
    ap.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic")
    ap.add_argument("--model", default=os.environ.get("EVAL_MODEL", ""))
    ap.add_argument("--base-url", default="https://api.openai.com/v1")
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--outdir", default=os.path.join(HERE, "runs"))
    args = ap.parse_args(argv)

    groups = ["with", "without"] if args.group == "both" else [args.group]
    cases = json.loads(read_text(os.path.join(HERE, "evals.json")))["evals"]
    if args.only:
        wanted = set(args.only)
        cases = [c for c in cases if c["id"] in wanted]
        missing = wanted - {c["id"] for c in cases}
        if missing:
            sys.stderr.write("没有这些 id：%s\n" % sorted(missing))
            return 2

    commit = git_commit()
    today = datetime.date.today().isoformat()
    # dry-run 单独放，免得空跑产物被当成真结果提交进报告
    stamp = "%s-%s" % (commit, today)
    outdir = os.path.join(args.outdir, "_dryrun", stamp if args.dry_run else "")
    if not args.dry_run:
        outdir = os.path.join(args.outdir, stamp)
    os.makedirs(outdir, exist_ok=True)
    model = args.model or "UNSET"

    if not args.dry_run and not args.model:
        sys.stderr.write("缺 --model（或用 EVAL_MODEL 环境变量）\n")
        return 2

    for case in cases:
        if case.get("setup"):
            sys.stderr.write("注意：题 %s 需要夹具，先跑 %s\n"
                             % (case["id"], case["setup"].split("，")[0]))
        for group, system, user in build_runs(case, groups):
            started = datetime.datetime.now()
            path = os.path.join(outdir, "%s-%s.md" % (case["id"], group))
            text = markdown(case, group, system, user, model, commit, started)

            if args.dry_run:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(text + "\n（dry-run：没有调模型）\n")
                print("dry-run  %s  (%d 字 system / %d 字 user)"
                      % (os.path.basename(path), len(system), len(user)))
                continue

            try:
                if args.provider == "anthropic":
                    output = call_anthropic(model, system, user, args.max_tokens)
                else:
                    output = call_openai(model, system, user,
                                         args.max_tokens, args.base_url)
            except urllib.error.HTTPError as e:
                sys.stderr.write("题 %s %s 组失败：HTTP %s %s\n"
                                 % (case["id"], group, e.code,
                                    e.read().decode("utf-8", "replace")[:400]))
                return 1
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text + output.strip() + "\n")
            print("done  %s  (%d 字输出)" % (os.path.basename(path), len(output)))

    print("\n落盘目录 %s" % outdir)
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
