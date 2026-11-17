#!/usr/bin/env python3
"""
Fallback word-timing generator: distributes the real transcript words across
the audio's ACTUAL speech segments (bounded by real detected silences),
weighted by word length within each segment.

This is used when ML-based forced alignment (stable-ts/whisper) is unavailable
or produces bad results, as a network-independent, audio-grounded alternative
to flat word-per-minute estimation. It respects real pauses; it does NOT
know exact per-word boundaries inside a continuous speech run.

INPUT:  rawtrascript.txt, tools/silence.txt (ffmpeg silencedetect output)
OUTPUT: data/words.json
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

FPS = 30
ROOT = Path(__file__).resolve().parents[1]
AUDIO_DURATION = 87.1  # raw1.MOV duration (ffprobe-confirmed)

def load_words(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    text_lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or re.match(r"^\d+:\d+:\d+", line):
            continue
        text_lines.append(line)
    text = " ".join(text_lines)
    return text.split()

def load_speech_segments(path: Path, total_duration: float) -> list[tuple[float, float]]:
    """Parse ffmpeg silencedetect output into the complementary speech segments."""
    silences = []
    cur_start = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m_start = re.search(r"silence_start:\s*([\d.]+)", line)
        m_end = re.search(r"silence_end:\s*([\d.]+)", line)
        if m_start:
            cur_start = float(m_start.group(1))
        elif m_end and cur_start is not None:
            silences.append((cur_start, float(m_end.group(1))))
            cur_start = None

    segments = []
    cursor = 0.0
    for s_start, s_end in silences:
        if s_start > cursor:
            segments.append((cursor, s_start))
        cursor = s_end
    if cursor < total_duration:
        segments.append((cursor, total_duration))
    return [seg for seg in segments if seg[1] - seg[0] > 0.05]

def distribute_words(words: list[str], segments: list[tuple[float, float]]) -> list[dict]:
    total_chars = sum(len(w) + 1 for w in words)  # +1 models inter-word gap cost
    total_speech_duration = sum(e - s for s, e in segments)

    # Allocate word counts to segments proportional to segment duration,
    # then lay words out within each segment weighted by (len(word)+1).
    out = []
    word_idx = 0
    chars_used_global = 0
    for seg_i, (seg_start, seg_end) in enumerate(segments):
        seg_duration = seg_end - seg_start
        # target: this segment should consume seg_duration/total_speech_duration
        # of total_chars worth of words.
        target_chars = total_chars * (seg_duration / total_speech_duration)
        chars_in_segment = 0
        seg_word_start_idx = word_idx
        while word_idx < len(words):
            w = words[word_idx]
            w_cost = len(w) + 1
            # stop if adding this word would overshoot target (unless segment is empty so far)
            if chars_in_segment > 0 and chars_in_segment + w_cost > target_chars and seg_i < len(segments) - 1:
                break
            chars_in_segment += w_cost
            word_idx += 1
        # last segment takes all remaining words
        if seg_i == len(segments) - 1:
            while word_idx < len(words):
                chars_in_segment += len(words[word_idx]) + 1
                word_idx += 1

        seg_words = words[seg_word_start_idx:word_idx]
        if not seg_words:
            continue
        seg_total_cost = sum(len(w) + 1 for w in seg_words)
        cursor = seg_start
        for w in seg_words:
            w_cost = len(w) + 1
            w_dur = seg_duration * (w_cost / seg_total_cost)
            start = cursor
            end = cursor + w_dur
            out.append({
                "text": w,
                "start": round(start, 3),
                "end": round(end, 3),
                "startFrame": int(round(start * FPS)),
                "endFrame": int(round(end * FPS)),
            })
            cursor = end
    return out

def main():
    words = load_words(ROOT / "rawtrascript.txt")
    # Fine-grained silencedetect (-24dB / 0.08s) catches micro-pauses BETWEEN
    # words, not just phrase-level breaks — this gets close to per-word
    # segmentation (218 gaps for 253 words) instead of the original 23
    # phrase-level gaps, so length-weighting now only has to interpolate
    # within a word or two at a time, not across a whole clause.
    segments = load_speech_segments(ROOT / "tools" / "silence_fine.txt", AUDIO_DURATION)
    print(f"{len(words)} words, {len(segments)} speech segments, "
          f"{sum(e - s for s, e in segments):.1f}s speech / {AUDIO_DURATION}s total")

    out_words = distribute_words(words, segments)

    out = {
        "meta": {
            "fps": FPS,
            "source": "rawtrascript.txt + ffmpeg silencedetect (pause-anchored fallback, no ML alignment)",
            "method": "word-length-weighted distribution within real detected speech segments",
            "wordCount": len(out_words),
            "lastWordEndFrame": out_words[-1]["endFrame"] if out_words else 0,
        },
        "words": out_words,
    }
    out_path = ROOT / "data" / "words.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Wrote {len(out_words)} words to {out_path}")
    print(f"  Last word end frame: {out['meta']['lastWordEndFrame']} (~{out['meta']['lastWordEndFrame']/FPS:.1f}s)")

if __name__ == "__main__":
    main()
