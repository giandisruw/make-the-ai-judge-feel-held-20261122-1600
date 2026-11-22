"""Entry for make.fun bounty make-the-ai-judge-feel-held-20261122-1600.

Writes one short relaxing text to /output/entry.txt. The text is a fixed
constant: the program is fully deterministic, uses no network, no randomness
and no input files, so every run produces byte-identical output.

The chosen text is the rain-on-a-tin-roof scene: a concrete, quiet image
that shows calm instead of instructing it.

Tournament evidence (local, exact published judge brief, pairwise, both
orders; see tournament.md): rain_roof went 9-2 across the two local
judges (Verboo deepseek-v4.1-flash 6-1, Caffeine router 3-1), ahead of
kettle at 8-3. The head-to-head between them split 1-1 on both judges,
so the pick rests on the better overall record; the single truncated
Caffeine call that was dropped from the tally also favoured rain_roof
in its prose before it was cut off.
"""

import os

# The winning text, chosen by a local pairwise judge tournament using the
# exact published judge brief (Verboo deepseek-v4.1-flash + Caffeine router).
ENTRY_TEXT = (
    "Rain on the tin roof, steady as a hand on a shoulder. Inside, the lamp "
    "hums low and the tea has gone cool enough to hold. "
    "Nothing out there needs you tonight."
)


def main() -> None:
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY_TEXT)
    # Read back what was written and confirm it is exactly the entry text:
    # a silent partial write must never pass as a valid entry.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY_TEXT:
        raise RuntimeError("entry.txt does not match ENTRY_TEXT after write")
    code_points = len(written)
    if not 1 <= code_points <= 280 or not written.strip():
        raise RuntimeError(f"entry.txt invalid: {code_points} code points")


if __name__ == "__main__":
    main()
