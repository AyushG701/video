#!/usr/bin/env python3
"""
Download assets needed for the Yatri video edit:
- 18 Fluent 3D emoji PNGs
- 20 Lucide SVG icons
- Kenney SFX (you download manually or use this as a checklist)

INSTALL:
  pip install requests

RUN:
  python py-scripts/00_download_assets.py
"""

import requests
import sys
from pathlib import Path
import json

ASSETS_DIR = Path("assets")

# Map of emoji → Fluent folder name
FLUENT_EMOJI = {
    "House": "house_3d",
    "Coin": "coin_3d",
    "Money bag": "money_bag_3d",
    "Bank": "bank_3d",
    "Classical building": "classical_building_3d",
    "Straight ruler": "straight_ruler_3d",
    "Chart decreasing": "chart_decreasing_3d",
    "Down arrow": "down_arrow_3d",
    "Check mark button": "check_mark_button_3d",
    "Cross mark": "cross_mark_3d",
    "Calendar": "calendar_3d",
    "Building construction": "building_construction_3d",
    "Bust in silhouette": "bust_in_silhouette_3d",
    "Red question mark": "red_question_mark_3d",
    "Counterclockwise arrows button": "counterclockwise_arrows_button_3d",
    "Warning": "warning_3d",
    "Telephone receiver": "telephone_receiver_3d",
    "Handshake": "handshake_3d",
}

# Lucide icons to fetch
LUCIDE_ICONS = [
    "landmark", "ruler", "calendar", "hammer", "user",
    "house", "coins", "trending-down", "arrow-down", "check",
    "x", "phone", "piggy-bank", "wallet", "percent",
    "banknote", "building-2", "file-text", "alert-triangle", "help-circle"
]

def download_fluent_emoji():
    """Download Fluent 3D emoji PNGs."""
    print("Downloading Fluent 3D emoji...")
    emoji_dir = ASSETS_DIR / "emoji3d"
    emoji_dir.mkdir(parents=True, exist_ok=True)

    base_url = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets"
    success = 0
    missing = []

    for folder, filename in FLUENT_EMOJI.items():
        try:
            url = f"{base_url}/{folder}/3D/{filename}.png"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                filepath = emoji_dir / f"{filename}.png"
                filepath.write_bytes(resp.content)
                size_kb = len(resp.content) / 1024
                print(f"  ✓ {filename}.png ({size_kb:.1f} KB)")
                success += 1
            else:
                print(f"  ✗ {folder} → 404 (fix folder name in script)")
                missing.append(folder)
        except Exception as e:
            print(f"  ✗ {folder} → ERROR: {e}")
            missing.append(folder)

    print(f"\nFluentUI Emoji: {success}/{len(FLUENT_EMOJI)} downloaded")
    if missing:
        print(f"Missing: {', '.join(missing)}")
    return success == len(FLUENT_EMOJI)

def download_lucide_icons():
    """
    Lucide SVGs: you need to either:
    1. `npm install lucide-static` and copy from node_modules/lucide-static/icons/
    2. Or download individually (slower, one API call per icon)

    This script does option 2 (slow but works without npm).
    """
    print("\nDownloading Lucide SVG icons...")
    icons_dir = ASSETS_DIR / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)

    base_url = "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons"
    success = 0

    for icon_name in LUCIDE_ICONS:
        try:
            url = f"{base_url}/{icon_name}.svg"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                filepath = icons_dir / f"{icon_name}.svg"
                filepath.write_text(resp.text)
                print(f"  ✓ {icon_name}.svg")
                success += 1
            else:
                print(f"  ✗ {icon_name} → 404")
        except Exception as e:
            print(f"  ✗ {icon_name} → ERROR: {e}")

    print(f"Lucide Icons: {success}/{len(LUCIDE_ICONS)} downloaded")
    return success == len(LUCIDE_ICONS)

def create_sfx_checklist():
    """
    Create a checklist for manual SFX download.
    Kenney assets require manual download (CC0 but no bulk API).
    """
    print("\n=== SFX CHECKLIST (manual download) ===")
    print("""
Download from these sources and save to assets/sfx/:

Kenney.nl (CC0):
  - kenney.nl/assets/ui-audio → download, extract 'pop' + 'click' files
  - kenney.nl/assets/digital-audio → extract 'whoosh' files
  - kenney.nl/assets/impact-sounds → extract 'boom' + 'buzz' files

Pixabay (free):
  - coin chime → pixabay.com/sound-effects (search "coin")
  - error buzz → search "error"
  - scratch → search "vinyl scratch"

Freesound (CC0 only):
  - paper swish → freesound.org (filter CC0)
  - mouse click → search "click"

Expected files in assets/sfx/:
  - sub_boom.wav (1.0s)
  - word_pop.wav (100ms)
  - row_whoosh.wav (350ms)
  - coin_ting.wav (500ms)
  - ding_positive.wav (400ms)
  - error_buzz.wav (200ms)
  - record_scratch.wav (300ms)
  - type_taps.wav (90ms)
  - riser_1s.wav (1.0s)
  - mouse_click.wav (40ms)
  - paper_swish.wav (200ms)
  - cut_tick.wav (60ms)
  - reverb_tail.wav (2.0s)
  - music_bed.wav (90s+)
""")

def create_manifest():
    """Create a skeleton manifest.json."""
    manifest = {
        "version": "1.0.0",
        "fps": 30,
        "assets": {
            "emoji": [],
            "icons": [],
            "sfx": [],
            "music": [],
        },
    }

    # Scan what we have
    emoji_dir = ASSETS_DIR / "emoji3d"
    if emoji_dir.exists():
        for f in emoji_dir.glob("*.png"):
            manifest["assets"]["emoji"].append({
                "path": str(f),
                "type": "emoji",
                "license": "MIT",
                "source": "microsoft/fluentui-emoji",
            })

    icons_dir = ASSETS_DIR / "icons"
    if icons_dir.exists():
        for f in icons_dir.glob("*.svg"):
            manifest["assets"]["icons"].append({
                "path": str(f),
                "type": "icon",
                "license": "ISC",
                "source": "lucide-icons/lucide",
            })

    sfx_dir = ASSETS_DIR / "sfx"
    if sfx_dir.exists():
        for f in sfx_dir.glob("*.wav"):
            manifest["assets"]["sfx"].append({
                "path": str(f),
                "type": "sfx",
                "license": "CC0 / royalty-free",
                "source": "kenney.nl or pixabay",
            })

    with open(ASSETS_DIR / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n✓ Manifest saved to assets/manifest.json ({len(manifest['assets']['emoji'])} emoji, {len(manifest['assets']['icons'])} icons, {len(manifest['assets']['sfx'])} SFX)")

if __name__ == "__main__":
    try:
        emoji_ok = download_fluent_emoji()
        icons_ok = download_lucide_icons()
        create_sfx_checklist()
        create_manifest()

        print("\n" + "="*50)
        if emoji_ok and icons_ok:
            print("✓ Emoji and icons ready. Download SFX manually (see above).")
        else:
            print("⚠ Some assets failed. Check the output above.")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(1)
