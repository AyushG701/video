#!/usr/bin/env python3
"""
Parse a plain-text transcript and convert to caption JSON.

INPUT: A plain text transcript (can be VTT format or just lines)
OUTPUT: data/captions.json (ready to feed into Remotion components)

USAGE:
  python py-scripts/parse_transcript.py rawtrascript.txt

The script will:
1. Extract words + timings (if VTT) or estimate timings (if plain text)
2. Apply color logic (yellow/green/red/white/navy based on keywords)
3. Generate panels (icon rows)
4. Output captions.json
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

FPS = 30

# Color logic: keyword → tag
COLOR_MAP = {
    # Yellow (subject nouns / scheme names)
    "5% Deposit Scheme": "yellow",
    "Deposit Scheme": "yellow",
    "Retained Saving": "yellow",
    "Retained Savings": "yellow",
    "Minimum Criteria": "yellow",
    "Housing Australia": "yellow",
    "Government": "yellow",
    "First Home Buyer": "yellow",
    "Bank Policy": "yellow",
    "Gov Rule": "yellow",
    "House and Land": "yellow",
    "Construction": "yellow",
    "Living Expenses": "yellow",

    # Green (money / percentages / positive)
    "5%": "green",
    "10%": "green",
    "6 महिना": "green",
    "छ महिनाको": "green",
    "राख्न पाउनुहुन्थ्यो": "green",
    "पाउनुहुन्छ": "green",
    "राख्न सक्नुहुन्छ": "green",
    "certain": "green",

    # Red (restrictions / negatives / warnings)
    "पाउनुहुन्न": "red",
    "defeats the purpose": "red",
    "defeats": "red",
    "Change": "red",
    "नि": "red",
    "होइन": "red",
    "नि त": "red",
    "सुख छैन": "red",

    # Navy (static labels for panels)
    "OLD": "navy",
    "NEW": "navy",
}

def extract_vtt_timings(text: str) -> List[tuple]:
    """Extract timings from VTT format: HH:MM:SS,mmm --> HH:MM:SS,mmm"""
    timings = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        match = re.match(r'(\d+):(\d+):(\d+),(\d+)\s+-->\s+(\d+):(\d+):(\d+),(\d+)', line)
        if match:
            start_h, start_m, start_s, start_ms, end_h, end_m, end_s, end_ms = map(int, match.groups())
            start_time = start_h * 3600 + start_m * 60 + start_s + start_ms / 1000
            end_time = end_h * 3600 + end_m * 60 + end_s + end_ms / 1000
            # Next line is the caption text
            if i + 1 < len(lines):
                text_line = lines[i + 1].strip()
                timings.append((start_time, end_time, text_line))
    return timings

def get_color_tag(word: str) -> str:
    """Determine color tag based on keyword matching."""
    for keyword, tag in COLOR_MAP.items():
        if keyword.lower() in word.lower():
            return tag
    return "white"  # default

def is_nepali(text: str) -> bool:
    """Check if text contains Devanagari (Nepali)."""
    return any('ऀ' <= c <= 'ॿ' for c in text)

def parse_transcript(filepath: str) -> Dict[str, Any]:
    """Parse transcript and generate caption JSON."""
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: {filepath} not found")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try to detect VTT format
    if '-->' in content:
        print(f"Detected VTT format in {filepath}")
        vtt_timings = extract_vtt_timings(content)

        captions = []
        for start_s, end_s, text in vtt_timings:
            # Clean up text (remove speaker tags, etc.)
            text = re.sub(r'\[speaker_\d+\]', '', text).strip()
            if not text:
                continue

            # Split into words
            words = text.split()
            word_duration_s = (end_s - start_s) / len(words) if words else 0.5

            current_time = start_s
            for word in words:
                word_end = current_time + word_duration_s
                start_frame = int(current_time * FPS)
                end_frame = int(word_end * FPS)

                captions.append({
                    "text": word,
                    "startFrame": start_frame,
                    "endFrame": end_frame,
                    "colorTag": get_color_tag(word),
                    "fontFamily": "Noto Sans Devanagari" if is_nepali(word) else "Montserrat",
                    "fontSize": 46,
                    "fontWeight": 700,
                })

                current_time = word_end
    else:
        # Plain text: estimate timings at 150 wpm
        print(f"Plain text format. Estimating timings at 150 wpm...")
        words_text = content.strip().split()
        wpm = 150
        wps = wpm / 60  # words per second

        captions = []
        current_time = 0
        for word in words_text:
            word_duration = 1.0 / wps
            start_frame = int(current_time * FPS)
            end_frame = int((current_time + word_duration) * FPS)

            captions.append({
                "text": word,
                "startFrame": start_frame,
                "endFrame": end_frame,
                "colorTag": get_color_tag(word),
                "fontFamily": "Noto Sans Devanagari" if is_nepali(word) else "Montserrat",
                "fontSize": 46,
                "fontWeight": 700,
            })

            current_time += word_duration

    # Generate panels (icon rows) from key sections
    panels = [
        {
            "title": "The Reality",
            "startFrame": 240,
            "rows": [
                {
                    "iconName": "bank",
                    "label": "OLD: Bank Policy",
                    "value": "5% Deposit Scheme",
                    "startFrame": 360,
                },
                {
                    "iconName": "ruler",
                    "label": "Minimum Criteria",
                    "value": "Required amount",
                    "startFrame": 630,
                },
                {
                    "iconName": "building-2",
                    "label": "NEW: Gov Rule",
                    "value": "Housing Australia",
                    "startFrame": 900,
                },
            ],
        },
        {
            "title": "How to Protect Yourself",
            "startFrame": 1620,
            "rows": [
                {
                    "iconName": "user",
                    "label": "Bigger Deposit",
                    "value": "More Buffer",
                    "startFrame": 1620,
                },
                {
                    "iconName": "calendar",
                    "label": "6 mo Living Expenses",
                    "value": "After purchase",
                    "startFrame": 1920,
                },
                {
                    "iconName": "building-2",
                    "label": "Extra 5–10%",
                    "value": "House & Land / Construction",
                    "startFrame": 2220,
                },
            ],
        },
    ]

    # Motifs (animations)
    motifs = [
        {
            "type": "coin-stack",
            "startFrame": 1050,
            "x": 540,
            "y": 600,
            "coinCount": 4,
        },
        {
            "type": "cta-card",
            "text": "let's make a plan together →",
            "startFrame": 2340,
            "x": 540,
            "y": 1800,
        },
    ]

    # Output JSON
    output = {
        "meta": {
            "fps": FPS,
            "durationSeconds": max([c["endFrame"] for c in captions]) / FPS if captions else 87,
            "durationFrames": int(max([c["endFrame"] for c in captions])) if captions else 2610,
            "language": "Nepali-English",
            "source": str(filepath),
        },
        "captions": captions,
        "panels": panels,
        "motifs": motifs,
    }

    return output

def main():
    if len(sys.argv) < 2:
        print("USAGE: python py-scripts/parse_transcript.py <transcript.txt>")
        print("\nEXAMPLE:")
        print("  python py-scripts/parse_transcript.py rawtrascript.txt")
        sys.exit(1)

    transcript_file = sys.argv[1]
    output_data = parse_transcript(transcript_file)

    output_path = Path("data/captions.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Parsed {len(output_data['captions'])} captions")
    print(f"  Duration: {output_data['meta']['durationSeconds']}s")
    print(f"  Panels: {len(output_data['panels'])}")
    print(f"  Output: {output_path}")
    print(f"\nNow edit src/Root.tsx to wire in captions from {output_path}")

if __name__ == "__main__":
    main()
