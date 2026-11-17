#!/usr/bin/env python3
"""
Build data/sfx_placement.json (+ a CSV sheet) from the REAL captions.json
timings and the REAL files actually present in assets/sfx / assets/music.

Previous version of this file referenced files that were never downloaded
(sub_boom.wav, word_pop.wav, coin_ting.wav, ...) and frame numbers from the
old flat 150wpm estimate. This rebuilds it from what actually exists.
"""
import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
FPS = 30

def main():
    captions = json.loads((ROOT / "data" / "captions.json").read_text(encoding="utf-8"))
    words = captions["captions"]
    panels = captions["panels"]
    motifs = captions["motifs"]
    duration_frames = captions["meta"]["durationFrames"]

    sfx = []

    # Word pops — a soft click on every colored (emphasized) word, not every
    # single word, matching the design's "pop on emphasis" rule rather than
    # pop-spamming all 253 words.
    pop_placements = [
        {"startFrame": w["startFrame"], "level": "-16dB", "note": w["text"]}
        for w in words if w["colorTag"] != "white"
    ]
    sfx.append({
        "name": "word_pop",
        "file": "assets/sfx/click_002.wav",
        "placements": pop_placements,
        "description": "Soft pop on every emphasized (colored) word",
    })

    # Coin ting — green (money/%) words specifically.
    coin_placements = [
        {"startFrame": w["startFrame"], "level": "-14dB", "note": w["text"]}
        for w in words if w["colorTag"] == "green"
    ]
    sfx.append({
        "name": "coin_ting",
        "file": "assets/sfx/coin_chime_01.mp3",
        "placements": coin_placements,
        "description": "Bright chime on money/percentage/allowed-exception words",
    })

    # Error buzz — red (restriction/negative) words.
    error_placements = [
        {"startFrame": w["startFrame"], "level": "-14dB", "note": w["text"]}
        for w in words if w["colorTag"] == "red"
    ]
    sfx.append({
        "name": "error_buzz",
        "file": "assets/sfx/error_003.wav",
        "placements": error_placements,
        "description": "Buzz on restriction/negative words",
    })

    # Row whoosh — every icon-tile row reveal across both panels.
    row_placements = []
    for panel in panels:
        for row in panel["rows"]:
            row_placements.append({"startFrame": row["startFrame"], "level": "-14dB",
                                     "note": f"{panel['title']} / {row['label']}"})
    sfx.append({
        "name": "row_whoosh",
        "file": "assets/sfx/whoosh_01.mp3",
        "placements": row_placements,
        "description": "Whoosh on each icon-tile row sliding up",
    })

    # Panel title type-on tick.
    title_placements = [{"startFrame": p["startFrame"], "level": "-14dB", "note": p["title"]} for p in panels]
    sfx.append({
        "name": "panel_title_tick",
        "file": "assets/sfx/toggle_002.wav",
        "placements": title_placements,
        "description": "Soft tick as each panel title appears",
    })

    # Coin-stack motif: impact boom + scratch pivot just before it, confirmation
    # ding when the house lands.
    for m in motifs:
        if m["type"] == "coin-stack":
            sfx.append({
                "name": "pivot_scratch", "file": "assets/sfx/scratch_002.wav",
                "startFrame": max(m["startFrame"] - 10, 0), "level": "-14dB",
                "description": "Record-scratch pivot just before the restriction motif",
            })
            sfx.append({
                "name": "motif_impact", "file": "assets/sfx/impact_boom_01.mp3",
                "startFrame": m["startFrame"], "level": "-12dB",
                "description": "Impact as the coin-stack / restriction motif lands",
            })
            sfx.append({
                "name": "motif_confirm", "file": "assets/sfx/confirmation_002.wav",
                "startFrame": m["startFrame"] + 8, "level": "-14dB",
                "description": "Confirmation ding as the house settles on the stack",
            })
        if m["type"] == "cta-card":
            sfx.append({
                "name": "cta_riser", "file": "assets/sfx/riser_01.mp3",
                "startFrame": max(m["startFrame"] - 30, 0), "level": "-16dB",
                "description": "1s riser building into the CTA card",
            })
            sfx.append({
                "name": "cta_click", "file": "assets/sfx/click_004.wav",
                "startFrame": m["startFrame"] + 10, "level": "-16dB",
                "description": "Click as the CTA card settles",
            })

    # Opening hook impact.
    sfx.insert(0, {
        "name": "opening_boom", "file": "assets/sfx/impact_boom_02.mp3",
        "startFrame": 0, "level": "-12dB",
        "description": "Opening attention-grab impact",
    })

    out = {
        "meta": {
            "fps": FPS,
            "durationFrames": duration_frames,
            "durationSeconds": duration_frames / FPS,
            "note": "All startFrame values are real frame numbers against data/captions.json timing.",
        },
        "music": {
            "file": "assets/music/music_bed.mp3",
            "startFrame": 0,
            "durationFrames": duration_frames,
            "level": "-25dB (ducks to -30dB under speech, swells to -22dB at CTA)",
            "description": "Instrumental, no-vocal bed — verified via spectrogram inspection",
        },
        "sfx": sfx,
        "mixing": {
            "vocal": {"target": "-6 to -3 dB LUFS-ish", "chain": "highpass 80Hz -> de-ess 5-7kHz -> compress 3:1 @ -15dB threshold"},
            "music_bed": {"level": "-25dB", "sidechain_keyed_to": "vocal", "threshold": "-18dB", "ratio": "4:1", "attack_ms": 10, "release_ms": 250},
            "sfx": {"level": "-14 to -16dB"},
        },
    }

    out_path = ROOT / "data" / "sfx_placement.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    # CSV sheet — one row per concrete placement, flattened.
    csv_path = ROOT / "data" / "sfx_placement_sheet.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sfx_name", "file", "start_frame", "start_seconds", "level", "note"])
        for entry in sfx:
            if "placements" in entry:
                for p in entry["placements"]:
                    writer.writerow([entry["name"], entry["file"], p["startFrame"],
                                      round(p["startFrame"] / FPS, 3), p["level"], p.get("note", "")])
            else:
                writer.writerow([entry["name"], entry["file"], entry["startFrame"],
                                  round(entry["startFrame"] / FPS, 3), entry["level"], entry.get("description", "")])

    total_placements = sum(len(e["placements"]) if "placements" in e else 1 for e in sfx)
    print(f"✓ Wrote {len(sfx)} SFX categories, {total_placements} total placements")
    print(f"  JSON: {out_path}")
    print(f"  CSV:  {csv_path}")

if __name__ == "__main__":
    main()
