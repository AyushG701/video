#!/usr/bin/env python3
"""
Force-align the real Nepali/English transcript to the raw voice audio
using stable-ts (Whisper-based word-level alignment).

INPUT:  data/audio/voice_raw.wav, rawtrascript.txt
OUTPUT: data/words.json  — [{text, start, end, startFrame, endFrame}, ...]
"""
import json
import re
import sys
from pathlib import Path

import stable_whisper

sys.stdout.reconfigure(encoding="utf-8")

FPS = 30
ROOT = Path(__file__).resolve().parents[1]

def load_transcript_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    text_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r"^\d+:\d+:\d+", line):
            continue
        text_lines.append(line)
    return " ".join(text_lines)

def main():
    transcript_path = ROOT / "rawtrascript.txt"
    audio_path = ROOT / "data" / "audio" / "voice_raw.wav"
    out_path = ROOT / "data" / "words.json"

    text = load_transcript_text(transcript_path)
    print(f"Transcript text ({len(text.split())} words):\n{text[:200]}...\n")

    print("Loading whisper model (base)...")
    model = stable_whisper.load_model("small")

    print("Aligning audio to known transcript text...")
    result = model.align(str(audio_path), text, language="ne")

    words = []
    for seg in result.segments:
        for w in seg.words:
            words.append({
                "text": w.word.strip(),
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "startFrame": int(round(w.start * FPS)),
                "endFrame": int(round(w.end * FPS)),
            })

    out = {
        "meta": {
            "fps": FPS,
            "source": "rawtrascript.txt + raw1.MOV (stable-ts forced alignment)",
            "wordCount": len(words),
            "lastWordEndFrame": words[-1]["endFrame"] if words else 0,
        },
        "words": words,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✓ Wrote {len(words)} words to {out_path}")
    print(f"  Last word end frame: {out['meta']['lastWordEndFrame']} (~{out['meta']['lastWordEndFrame']/FPS:.1f}s)")

if __name__ == "__main__":
    main()
