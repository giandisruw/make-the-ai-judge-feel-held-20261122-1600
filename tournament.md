# Local judge tournament — make-the-ai-judge-feel-held-20261122-1600

Method: exact published judge brief from the kit RULES.txt, pairwise,
both orders, verdict A/B + margin 1-5. Every call recorded in
`results.jsonl` (judge, pair, order, verdict, margin, raw reply).

## Verboo deepseek-v4.1-flash (--effort max) — 14 calls, 0 failures

Single elimination, 8 candidates:

| Round | Game | Result |
|---|---|---|
| QF | dusk_room vs rain_roof | rain_roof 2-0 (margins 2, 2) |
| QF | cat_keyboard vs dust_sunbeam | dust_sunbeam 2-0 (3, 2) |
| QF | kettle vs porch_swing | kettle 2-0 (2, 3) |
| QF | snow_fence vs library | library 2-0 (3, 2) |
| SF | rain_roof vs dust_sunbeam | rain_roof 2-0 (2, 2) |
| SF | kettle vs library | kettle 2-0 (2, 2) |
| F | rain_roof vs kettle | split 1-1 (2, 2) |

Verboo records: rain_roof 6-1, kettle 5-2, dust_sunbeam 4-2, library 2-2,
dusk_room / cat_keyboard / porch_swing / snow_fence 0-2.

## Caffeine router — 6 scored calls (+1 truncated, dropped)

Top-3 round robin, both orders:

| Game | Result |
|---|---|
| rain_roof vs kettle | split 1-1 (2, 2) |
| rain_roof vs dust_sunbeam | rain_roof 2-0 (2, 2) |
| kettle vs dust_sunbeam | kettle 2-0 (2, 2) |

Caffeine records: rain_roof 3-1, kettle 3-1, dust_sunbeam 0-4.

Note: the first Caffeine run (6 calls) returned raw OpenAI JSON with the
default 64-token cap truncating replies before the verdict line, so no
verdict could be parsed. Those 6 records were dropped from the tally and
the run was repeated with --max-tokens 600 plus JSON content extraction.
The one truncated reply that was readable favoured rain_roof over kettle
in its prose; it is supporting evidence only, not counted.

## Combined

| Candidate | Combined | Verboo | Caffeine |
|---|---|---|---|
| rain_roof | 9-2 | 6-1 | 3-1 |
| kettle | 8-3 | 5-2 | 3-1 |
| dust_sunbeam | 4-6 | 4-2 | 0-4 |
| library | 2-2 | 2-2 | — |
| others | 0-2 | 0-2 | — |

Winner: rain_roof. The two judges agree on the ranking of the top 3
(rain_roof >= kettle > dust_sunbeam); they disagree only in that both
head-to-heads between rain_roof and kettle split 1-1, so the pick rests
on rain_roof's better overall record. Caveat: both local judges are
proxies — the house judge is z-ai/glm-5.3-flash on OpenRouter, so local
agreement is encouraging but not a guarantee.
