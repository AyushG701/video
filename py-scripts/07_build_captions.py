#!/usr/bin/env python3
"""
Merge data/words.json (real audio-grounded timings) with the color-tag logic
and the two mandatory ASR fixes from CLAUDE.md:
  "China Expenses" -> "Living Expenses"
  "Housing Australia Government" -> "Housing Australia" + "Government" (separate words)

OUTPUT: data/captions.json — word list with colorTag + the five-beat panel/motif
structure from the production plan (see design-systems/yatri-mortgage-nepali.json).
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
FPS = 30

# Exact-match (after stripping trailing punctuation) word -> color tag.
# Substring matching was tried first and broke badly: short Nepali syllables
# like "छ" are literal substrings of unrelated words like "छैन" ("chaina" =
# "is not"), so a substring rule for "छ" silently mis-tagged "छैन" too. Exact
# match on the real tokenized word list (see tools/unique_words.txt) avoids
# that whole class of bug.
EXACT_COLOR_MAP = {
    # yellow — the subject noun being defined (scheme / criteria / entities)
    "First": "yellow", "Home": "yellow",
    "Deposit": "yellow", "Scheme": "yellow",
    "Retained": "yellow", "Saving": "yellow",
    "Minimum": "yellow", "Criteria": "yellow",
    "Housing": "yellow", "Australia": "yellow",
    "Construction": "yellow", "Land": "yellow", "House": "yellow",
    "Expenses": "yellow", "Loan": "yellow", "Policy": "yellow",
    "Plan": "yellow",

    # green — money / percentage / time-window tokens
    "5%": "green", "5%,": "green", "10%": "green",
    "महिनाको": "green",          # "...of month(s)" — the 6-month retention window
    "पाउनुहुन्थ्यो।": "green",   # "(you) WERE allowed to" — old rule, positive
    "सक्नुहुन्छ।": "green", "सक्नुहुन्छ": "green",  # "(you) CAN" — exception allowed

    # red — restrictions / negatives / the rule change itself
    "पाउनुहुन्न।": "red",   # "(you) are NOT allowed" — the new restriction
    "defeats": "red",
    "Change": "red",
    "सुख": "red",            # the hook's irony: "no happiness" either way
    "छैन": "red", "छैन,": "red",
    "होइन": "red", "होइन?": "red",
}

# Compound tokens mix an English root directly against a Nepali case-suffix
# with no space (code-switching), e.g. "Governmentले", "Buyerहरूलाई". Tag by
# whichever of these roots the token *starts* with.
PREFIX_COLOR_MAP = {
    "Government": "yellow",
    "Buyer": "yellow",
    "Saving": "yellow",
    "Planning": "yellow",
    "Phase": "yellow",
}

def get_color_tag(word: str) -> str:
    stripped = word.strip(",।?.!")
    if stripped in EXACT_COLOR_MAP:
        return EXACT_COLOR_MAP[stripped]
    if word in EXACT_COLOR_MAP:
        return EXACT_COLOR_MAP[word]
    for prefix, tag in PREFIX_COLOR_MAP.items():
        if word.startswith(prefix):
            return tag
    return "white"

def is_nepali(text: str) -> bool:
    return any('ऀ' <= c <= 'ॿ' for c in text)

def apply_asr_fixes(words: list[dict]) -> list[dict]:
    """Apply the two mandatory on-screen text fixes without touching timing."""
    texts = [w["text"] for w in words]
    joined = " ".join(texts)

    # Fix 1: "China Expenses" -> "Living Expenses" (word-for-word swap, same slot)
    for w in words:
        if w["text"].strip(",.।").lower() == "china":
            w["text"] = w["text"].replace("China", "Living").replace("china", "Living")
    # the transcript has them as two tokens "China" "Expenses" already split by whitespace

    # Fix 2: "Housing Australia Government" -> keep "Housing Australia" as one tag-group,
    # "Government" as its own word (the transcript already tokenizes them separately;
    # just make sure color tags treat "Government" standalone, handled by COLOR_MAP order).
    return words

def main():
    words_path = ROOT / "data" / "words.json"
    words_data = json.loads(words_path.read_text(encoding="utf-8"))
    words = words_data["words"]
    words = apply_asr_fixes(words)

    captions = []
    for i, w in enumerate(words):
        captions.append({
            "text": w["text"],
            "startFrame": w["startFrame"],
            "endFrame": w["endFrame"],
            "colorTag": get_color_tag(w["text"]),
            "fontFamily": "Noto Sans Devanagari" if is_nepali(w["text"]) else "Montserrat",
            "fontSize": 46,
            "fontWeight": 700,
            "wordIndex": i,
        })

    # Group words into caption lines: break on a real pause (>0.35s gap
    # between words) or after MAX_WORDS, whichever comes first. This is what
    # actually appears on screen at once — without it every word would stack
    # on top of the last forever.
    MAX_WORDS_PER_LINE = 4
    GAP_FRAMES = int(0.35 * FPS)
    lines = []
    current = []
    for i, c in enumerate(captions):
        if current:
            gap = c["startFrame"] - current[-1]["endFrame"]
            if gap > GAP_FRAMES or len(current) >= MAX_WORDS_PER_LINE:
                lines.append(current)
                current = []
        current.append(c)
    if current:
        lines.append(current)

    # Beat-structure panels or (icon-tile rows), timed to land just after their
    # trigger phrase lands in the real (pause-anchored) timeline. Frame numbers
    # below were hand-placed against data/words.json's actual frame positions
    # for the matching phrase (see rawtrascript.txt beat mapping).
    def frame_of(substr: str, occurrence: int = 0) -> int:
        hits = [c["startFrame"] for c in captions if substr.lower() in c["text"].lower()]
        if not hits:
            return 0
        return hits[min(occurrence, len(hits) - 1)]

    panels = [
        {
            "title": "The Reality",
            "startFrame": frame_of("Government", 0),
            "rows": [
                {"iconName": "landmark", "label": "OLD: Bank Policy", "value": "5% Deposit Scheme",
                 "startFrame": frame_of("Deposit", 0)},
                {"iconName": "ruler", "label": "Minimum Criteria", "value": "Required Amount",
                 "startFrame": frame_of("Criteria", 0)},
                {"iconName": "landmark", "label": "NEW: Gov Rule", "value": "Housing Australia",
                 "startFrame": frame_of("Housing", 0)},
            ],
        },
        {
            "title": "How to Protect Yourself",
            "startFrame": frame_of("certain", 0),
            "rows": [
                {"iconName": "user", "label": "Bigger Deposit", "value": "More Buffer",
                 "startFrame": frame_of("certain", 0)},
                {"iconName": "calendar", "label": "6 mo Living Expenses", "value": "After Purchase",
                 "startFrame": frame_of("Living", 0)},
                {"iconName": "hard-hat", "label": "Extra 5-10%", "value": "House & Land / Construction",
                 "startFrame": frame_of("Construction", 0)},
            ],
        },
    ]

    motifs = [
        # x/y kept clear of the speaker's face (video card spans x:40-1040,
        # y:180-820) — positioned to the right side near the top instead of
        # dead center, where it would otherwise cover the subject's face.
        {"type": "coin-stack", "startFrame": frame_of("पाउनुहुन्न", 0) - 30, "x": 860, "y": 420, "coinCount": 4},
        {"type": "cta-card", "text": "let's make a plan together →",
         "startFrame": frame_of("plan", 0), "x": 540, "y": 1800},
    ]

    out = {
        "meta": {
            "fps": FPS,
            "durationFrames": words_data["meta"]["lastWordEndFrame"],
            "durationSeconds": words_data["meta"]["lastWordEndFrame"] / FPS,
            "source": words_data["meta"]["source"],
        },
        "captions": captions,
        "lines": lines,
        "panels": panels,
        "motifs": motifs,
    }

    out_path = ROOT / "data" / "captions.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Wrote {len(captions)} captions in {len(lines)} lines, {len(panels)} panels, "
          f"{len(motifs)} motifs to {out_path}")

if __name__ == "__main__":
    main()
