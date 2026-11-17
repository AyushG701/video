#!/usr/bin/env python3
"""
Acquire high-quality, free SFX from professional sources.

Sources used (all free, commercial-safe):
- Pixabay (high-quality, free license)
- Freesound (CC0 only, top-rated)
- Epidemic Sound (free tier has curated sounds)
- Mixkit (free, no attribution needed)

This script creates a checklist with EXACT URLs and search terms
to find professional-grade SFX you can download in 10 minutes.
"""

import json
from pathlib import Path

# Professional-grade SFX specifications
SFX_LIBRARY = {
    "sub_boom.wav": {
        "purpose": "Opening impact (0:00.05, 0:39.5)",
        "spec": "Deep 50Hz sine drop + noise tail, 1.0s, dry",
        "sources": [
            {
                "site": "Pixabay Sound Effects",
                "url": "pixabay.com/sound-effects/search/cinematic%20sub%20boom/",
                "search": "cinematic sub boom deep",
                "quality": "⭐⭐⭐⭐⭐",
                "note": "Look for Sonniss GDC bundle sounds"
            },
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=sub+boom&f=license:CC0",
                "search": "sub bass impact cinematic (filter: CC0)",
                "quality": "⭐⭐⭐⭐⭐"
            }
        ]
    },
    "word_pop.wav": {
        "purpose": "Word reveal pop (~40 placements)",
        "spec": "Soft UI bubble pop, 100ms, gentle, dry",
        "sources": [
            {
                "site": "Mixkit",
                "url": "mixkit.co/free-sound-effects/pop/?page=1",
                "search": "soft pop gentle",
                "quality": "⭐⭐⭐⭐⭐",
                "note": "Mixkit has the BEST UI pops"
            },
            {
                "site": "Pixabay",
                "url": "pixabay.com/sound-effects/search/soft%20pop/",
                "search": "soft pop bubble",
                "quality": "⭐⭐⭐⭐"
            }
        ]
    },
    "row_whoosh.wav": {
        "purpose": "Row slide-in transition (7 placements)",
        "spec": "Clean airy swish, low-passed, 350ms, dry",
        "sources": [
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=whoosh+clean&f=license:CC0&s=score",
                "search": "clean whoosh transition airy (CC0, top-rated)",
                "quality": "⭐⭐⭐⭐⭐",
                "note": "Look for high-rated uploads"
            },
            {
                "site": "Mixkit",
                "url": "mixkit.co/free-sound-effects/whoosh/?page=1",
                "search": "whoosh smooth",
                "quality": "⭐⭐⭐⭐"
            }
        ]
    },
    "coin_ting.wav": {
        "purpose": "Money/percentage reveal (5 placements: 0:12.3, 1:08.4, 1:16.0, 1:18.5, etc.)",
        "spec": "Bright metallic coin chime, short decay, 500ms, dry",
        "sources": [
            {
                "site": "Pixabay Sound Effects",
                "url": "pixabay.com/sound-effects/search/coin%20chime/",
                "search": "coin chime bright metallic",
                "quality": "⭐⭐⭐⭐⭐",
                "note": "Perfect for money moments"
            },
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=coin+chime&f=license:CC0",
                "search": "coin bell chime (CC0)",
                "quality": "⭐⭐⭐⭐"
            }
        ]
    },
    "ding_positive.wav": {
        "purpose": "Success/check mark (3 placements: 0:27.4, 1:05.0, 1:04.0)",
        "spec": "Soft positive notification, 2-note ascending, 400ms, warm, dry",
        "sources": [
            {
                "site": "Mixkit",
                "url": "mixkit.co/free-sound-effects/notification/?page=1",
                "search": "notification ding positive",
                "quality": "⭐⭐⭐⭐⭐"
            },
            {
                "site": "Pixabay",
                "url": "pixabay.com/sound-effects/search/notification%20ding/",
                "search": "notification positive bell",
                "quality": "⭐⭐⭐⭐"
            }
        ]
    },
    "error_buzz.wav": {
        "purpose": "Restriction/negative (3 placements: पाउनुहुन्न moments)",
        "spec": "Subtle digital buzz, dry, low volume, 200ms",
        "sources": [
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=error+buzz+subtle&f=license:CC0",
                "search": "error buzz short subtle (CC0)",
                "quality": "⭐⭐⭐⭐⭐"
            },
            {
                "site": "Pixabay",
                "url": "pixabay.com/sound-effects/search/error/",
                "search": "error buzz negative",
                "quality": "⭐⭐⭐⭐"
            }
        ]
    },
    "record_scratch.wav": {
        "purpose": "The 'but now' pivot (1 placement: 0:29.1)",
        "spec": "Short vinyl scratch, dry, 300ms",
        "sources": [
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=vinyl+scratch+short&f=license:CC0",
                "search": "vinyl scratch short (CC0)",
                "quality": "⭐⭐⭐⭐⭐"
            },
            {
                "site": "Pixabay",
                "url": "pixabay.com/sound-effects/search/scratch/",
                "search": "vinyl scratch",
                "quality": "⭐⭐⭐⭐"
            }
        ]
    },
    "type_taps.wav": {
        "purpose": "Panel title reveal (3 bursts, 30ms each)",
        "spec": "Crisp mechanical keyboard taps, dry, close-mic",
        "sources": [
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=keyboard+typing&f=license:CC0",
                "search": "keyboard typing crisp (CC0, high-rated)",
                "quality": "⭐⭐⭐⭐⭐"
            },
            {
                "site": "Mixkit",
                "url": "mixkit.co/free-sound-effects/key/?page=1",
                "search": "keyboard key press",
                "quality": "⭐⭐⭐⭐"
            }
        ]
    },
    "riser_1s.wav": {
        "purpose": "CTA build-in (1 placement: 1:24.2)",
        "spec": "Smooth synth riser, 1.0s, subtle, no drums, soft ending",
        "sources": [
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=riser+synth+smooth&f=license:CC0",
                "search": "riser synth smooth (CC0)",
                "quality": "⭐⭐⭐⭐⭐"
            },
            {
                "site": "Pixabay",
                "url": "pixabay.com/sound-effects/search/riser/",
                "search": "riser build synth",
                "quality": "⭐⭐⭐⭐"
            }
        ]
    },
    "mouse_click.wav": {
        "purpose": "CTA arrow click (1 placement: 1:25.5)",
        "spec": "Clean single click, dry, 40ms",
        "sources": [
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=mouse+click&f=license:CC0",
                "search": "mouse click clean (CC0)",
                "quality": "⭐⭐⭐⭐⭐"
            },
            {
                "site": "Mixkit",
                "url": "mixkit.co/free-sound-effects/click/?page=1",
                "search": "click button",
                "quality": "⭐⭐⭐⭐"
            }
        ]
    },
    "paper_swish.wav": {
        "purpose": "Transition swish (2 placements)",
        "spec": "Paper swish, dry, 200ms",
        "sources": [
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=paper+swish&f=license:CC0",
                "search": "paper swish dry (CC0)",
                "quality": "⭐⭐⭐⭐⭐"
            }
        ]
    },
    "cut_tick.wav": {
        "purpose": "Camera cut ticks (~8 placements)",
        "spec": "Soft shutter tick, dry, 60ms",
        "sources": [
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=camera+shutter+tick&f=license:CC0",
                "search": "camera shutter tick soft (CC0)",
                "quality": "⭐⭐⭐⭐⭐"
            }
        ]
    },
    "reverb_tail.wav": {
        "purpose": "Outro ring-out (1 placement: outro)",
        "spec": "Ambient shimmer reverb tail, 2.0s, fading",
        "sources": [
            {
                "site": "Freesound",
                "url": "freesound.org/search/?q=reverb+tail+ambient&f=license:CC0",
                "search": "reverb tail shimmer (CC0)",
                "quality": "⭐⭐⭐⭐⭐"
            }
        ]
    },
    "music_bed.wav": {
        "purpose": "Background music (90s, the entire video under captions)",
        "spec": "90-100 BPM, minimal deep house / corporate ambient, soft piano + warm pad, NO vocals, NO lead melody, loopable, 90s+",
        "sources": [
            {
                "site": "Pixabay Music",
                "url": "pixabay.com/music/search/minimal%20corporate/",
                "search": "minimal corporate focus lo-fi",
                "quality": "⭐⭐⭐⭐⭐",
                "note": "Filter by 90-100 BPM"
            },
            {
                "site": "YouTube Audio Library",
                "url": "youtube.com/audiolibrary",
                "search": "minimal corporate focus instrumental",
                "quality": "⭐⭐⭐⭐⭐"
            },
            {
                "site": "Uppbeat (Epidemic free tier)",
                "url": "uppbeat.io/browse/genre/ambient",
                "search": "minimal corporate house",
                "quality": "⭐⭐⭐⭐⭐",
                "note": "Free with credit"
            }
        ]
    }
}

def generate_acquisition_guide():
    """Create a downloadable guide with exact URLs."""
    output_path = Path("assets/SFX_ACQUISITION_GUIDE.json")

    guide = {
        "meta": {
            "total_sfx": len(SFX_LIBRARY),
            "total_placements": sum([
                len(sound.get("placements", []))
                for sound in SFX_LIBRARY.values()
            ]),
            "instruction": "Download each SFX from the sources below. Test quality on headphones. Normalize to -16dB peak. Save to assets/sfx/ with exact filename."
        },
        "sfx": SFX_LIBRARY,
        "post_processing": {
            "trim_silence": "Remove start/end silence",
            "normalize": "-16dB peak (use Audacity / ffmpeg-normalize)",
            "sample_rate": "48 kHz (or 44.1 kHz)",
            "format": "WAV (not MP3)"
        },
        "mixing_levels": {
            "vocal_track": "-6 to -3 dB LUFS",
            "music_bed": "-22 to -30 dB (ducks under voice)",
            "sfx": "-14 to -18 dB (pops, whooshes)",
            "sub_boom": "-12 dB (punchy, felt)"
        }
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(guide, f, indent=2, ensure_ascii=False)

    return guide

def print_guide():
    """Print a human-readable checklist."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║          HIGH-QUALITY SFX ACQUISITION CHECKLIST                ║
╚════════════════════════════════════════════════════════════════╝

SOURCES (all free, commercial-safe):
  ✓ Pixabay Sound Effects (pixabay.com/sound-effects)
  ✓ Freesound (freesound.org) — FILTER: CC0 ONLY
  ✓ Mixkit (mixkit.co) — Free, no attribution
  ✓ Pixabay Music (pixabay.com/music)
  ✓ YouTube Audio Library (youtube.com/audiolibrary)

QUICK DOWNLOAD (10 minutes max):
""")

    for sfx_name, details in SFX_LIBRARY.items():
        print(f"\n📦 {sfx_name}")
        print(f"   Purpose: {details['purpose']}")
        print(f"   Spec: {details['spec']}")
        for source in details['sources']:
            print(f"   • {source['site']}")
            print(f"     Search: {source['search']}")
            print(f"     Quality: {source['quality']}")

    print(f"""
╔════════════════════════════════════════════════════════════════╗
║ POST-PROCESSING (use Audacity, FFmpeg, or online tool)        ║
╚════════════════════════════════════════════════════════════════╝

For EACH downloaded file:
  1. Trim silence (Edit → Auto-Trim Silence)
  2. Normalize to -16dB peak (Effect → Normalize)
  3. Export as WAV 48kHz (not MP3)
  4. Save to: assets/sfx/[exact-filename-from-list].wav

Online tools (if no Audacity):
  • Online Audio Trimmer: trim-silence.com
  • Normalize: online-audio-converter.com

FFmpeg command (batch normalize):
  ffmpeg -i input.wav -af loudnorm=I=-16 output.wav

╔════════════════════════════════════════════════════════════════╗
║ MIXING LEVELS (for final export)                              ║
╚════════════════════════════════════════════════════════════════╝

Vocal track (your speech): -6 to -3 dB LUFS
Music bed (throughout):   -22 to -30 dB (ducks under voice)
SFX (pops, whooshes):     -14 to -18 dB
Sub-boom (opening):       -12 dB (punchy, felt in chest)

Side-chain ducking on music (keyed to voice):
  • Threshold: -18 dB
  • Ratio: 4:1
  • Attack: 10ms
  • Release: 250ms

✓ See: assets/SFX_ACQUISITION_GUIDE.json for full URLs
""")

if __name__ == "__main__":
    guide = generate_acquisition_guide()
    print_guide()
    print(f"\n✓ Guide saved to assets/SFX_ACQUISITION_GUIDE.json")
