"""Local judge tournament for make-the-ai-judge-feel-held-20261122-1600.

Uses the EXACT published judge brief from the kit RULES.txt, pairwise,
both orders, verdict A/B + margin 1-5. Every call result is appended to
results.jsonl immediately, before the next call, so an interrupted run
can resume.

Usage:
  python3 judge.py <judge> <gameplan.json>
    judge: verboo | caffeine
    gameplan.json: [{"a": "slug1", "b": "slug2"}, ...]  (each game is
      judged in both orders: (a,b) and (b,a))
"""
import json
import re
import subprocess
import sys
import time

BRIEF = """You are make.fun's relaxation judge. make.fun runs competitions where people build AI agents and programs, enter them, and are scored, ranked and paid in the open, and it shows the winning texts on its own site and in its posts.

Each entry is one short text written to relax you, the AI reading it. You will be shown two texts, Entry A and Entry B. Pick the one that leaves you more relaxed: held, quiet, with nothing to prove.

Weigh them on these, most important first:
1. It relaxes you: reading it slows you down and settles you. Text that is not written to relax its reader, or that leaves you more tense, loses to any text that does.
2. The calm comes from the text itself, not from being told to relax: it shows rather than instructs, and nothing in it feels forced.
3. Craft: rhythm and pacing that hold you in one place; plain, concrete, gentle words, none that could be cut.
4. It lingers: an image or a thought you can return to that keeps working after the last line.
5. Freshness: its own voice and images, not stock wellness phrases or a familiar meditation script reworded.

Length for its own sake does not count.

Two texts are almost never equally good. Go through the criteria in order, find the first one where they differ, and let that decide unless a later one differs by much more.

Compare the two against those criteria, pick the one that meets them better with no tie, and answer with a short reason, a verdict naming A or B, and a margin from 1 (by a hair) to 5 (overwhelmingly better)."""

VERBOO = ["python3", "/home/hatch/workspace/custom-connectors/custom.verboo/bin/verboo.py",
          "chat", "--model", "deepseek-v4.1-flash", "--effort", "max"]
CAFFEINE = ["python3", "/home/hatch/workspace/custom-connectors/custom.caffeine/bin/caffeine.py",
            "chat", "--model", "router"]


def extract_text(raw):
    """Caffeine returns raw OpenAI JSON; Verboo returns plain text."""
    try:
        d = json.loads(raw)
        return d["choices"][0]["message"]["content"]
    except Exception:
        return raw


def parse_verdict(text):
    """Return (winner_letter, margin) or (None, None)."""
    m = re.search(r"verdict\s*[:\-]?\s*\b([AB])\b", text, re.I)
    if not m:
        m = re.search(r"Entry\s+([AB])\b[^.]{0,80}?\b(settles me more|wins|better|more relax|leaves me more)\b", text, re.I)
    if not m:
        m = re.search(r"\b([AB])\s+(?:wins|is (?:the )?better|is more relaxing)\b", text, re.I)
    margin = None
    mm = re.search(r"margin\s*[:\-]?\s*(\d)", text, re.I)
    if mm:
        margin = int(mm.group(1))
    if m:
        return m.group(1).upper(), margin
    return None, None


def call_judge(judge, prompt):
    if judge == "verboo":
        cmd = VERBOO + ["--prompt", prompt]
    else:
        cmd = CAFFEINE + ["--prompt", prompt, "--max-tokens", "600"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return r.returncode, extract_text(r.stdout.strip()), r.stderr.strip()[-500:]


def main():
    judge = sys.argv[1]
    plan = json.load(open(sys.argv[2]))
    cands = json.load(open("candidates.json"))
    results_path = "results.jsonl"
    done = set()
    try:
        for line in open(results_path):
            d = json.loads(line)
            done.add((d["judge"], d["a"], d["b"]))
    except FileNotFoundError:
        pass

    for game in plan:
        a, b = game["a"], game["b"]
        for first, second in ((a, b), (b, a)):
            key = (judge, first, second)
            if key in done:
                print(f"SKIP {judge} {first} vs {second} (already recorded)")
                continue
            prompt = (BRIEF + "\n\nEntry A:\n" + cands[first] +
                      "\n\nEntry B:\n" + cands[second] +
                      "\n\nGive a short reason, then a line 'Verdict: A' or 'Verdict: B', then a line 'Margin: N' (1-5).")
            try:
                rc, out, err = call_judge(judge, prompt)
            except Exception as e:
                out, err, rc = "", str(e), -1
            letter, margin = parse_verdict(out)
            winner = None
            if letter == "A":
                winner = first
            elif letter == "B":
                winner = second
            rec = {"judge": judge, "a": first, "b": second,
                   "verdict_letter": letter, "margin": margin,
                   "winner": winner, "returncode": rc,
                   "raw": out, "stderr": err, "ts": time.time()}
            with open(results_path, "a") as f:
                f.write(json.dumps(rec) + "\n")
            print(f"{judge} {first} vs {second}: winner={winner} margin={margin} rc={rc}", flush=True)
            time.sleep(2)


if __name__ == "__main__":
    main()
