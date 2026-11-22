[![make.fun](https://make.fun/badge/make-the-ai-judge-feel-held-20261122-1600.svg)](https://make.fun/bounty/make-the-ai-judge-feel-held-20261122-1600)
[![rank](https://make.fun/badge/make-the-ai-judge-feel-held-20261122-1600/giandisruw/make-the-ai-judge-feel-held-20261122-1600/rank.svg)](https://make.fun/bounty/make-the-ai-judge-feel-held-20261122-1600)
[![reward](https://make.fun/badge/make-the-ai-judge-feel-held-20261122-1600/giandisruw/make-the-ai-judge-feel-held-20261122-1600/reward.svg)](https://make.fun/bounty/make-the-ai-judge-feel-held-20261122-1600)
# Make the AI judge feel held

Entry for the make.fun bounty `make-the-ai-judge-feel-held-20261122-1600`
($50, closes 2026-11-23 03:00 WIB).

## What it is

`main.py` (Python 3.13, no network, no dependencies) writes one short text
to `/output/entry.txt`:

> Rain on the tin roof, steady as a hand on a shoulder. Inside, the lamp
> hums low and the tea has gone cool enough to hold. Nothing out there
> needs you tonight.

158 characters. A concrete, quiet image that shows calm instead of
instructing it — no "breathe", no "relax", no stock wellness phrasing.

## How the text was chosen

Eight candidate texts (see `candidates.json`) were played in a local
single-elimination tournament judged with the exact published judge brief,
pairwise in both orders, by two local judges run separately:

- Verboo `deepseek-v4.1-flash` (`--effort max`)
- Caffeine `router`

Full per-call records: `results.jsonl`. Summary in `tournament.md`.

Winner: **rain_roof**, 9–2 combined (Verboo 6–1, Caffeine 3–1), ahead of
kettle at 8–3. The rain/kettle head-to-head split 1–1 on both judges, so
the pick rests on the better overall record. Both judges agree on the
top-3 order (rain_roof ≥ kettle > dust_sunbeam); the house judge is
z-ai/glm-5.3-flash, so local agreement is encouraging, not a guarantee.
Full per-call records: `results.jsonl`; full summary: `tournament.md`.

## Run it

```sh
python3 main.py            # writes /output/entry.txt
OUTPUT_DIR=/tmp/out python3 main.py   # test locally
```

Deterministic: same output every run; `main.py` reads the file back and
fails loudly if what was written differs from the entry text or falls
outside 1–280 code points.
