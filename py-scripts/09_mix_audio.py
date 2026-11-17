#!/usr/bin/env python3
"""
Build the final mixed audio track: cleaned-up voice + ducked music bed +
every SFX placement from data/sfx_placement.json, sample-accurate.

OUTPUT: mixed_audio_final.wav
"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
FFMPEG_BIN = ROOT / "tools" / "ffmpeg-master-latest-win64-gpl" / "bin" / "ffmpeg.exe"
FFPROBE_BIN = ROOT / "tools" / "ffmpeg-master-latest-win64-gpl" / "bin" / "ffprobe.exe"
os.environ["PATH"] = str(FFMPEG_BIN.parent) + os.pathsep + os.environ.get("PATH", "")

from pydub import AudioSegment
AudioSegment.converter = str(FFMPEG_BIN)
AudioSegment.ffprobe = str(FFPROBE_BIN)

FPS = 30

def frame_to_ms(frame: int) -> int:
    return int(frame * 1000 / FPS)

def db_to_gain(db_str: str) -> float:
    """Parse a '-14dB' style string to a float dB value (first number found)."""
    import re
    m = re.search(r"-?\d+\.?\d*", db_str)
    return float(m.group()) if m else 0.0

def clean_voice(raw_wav: Path, out_wav: Path):
    """Voice cleanup chain: high-pass rumble, de-ess sibilance, compress for
    even loudness. Pure ffmpeg filter chain, no external plugins needed."""
    filt = (
        "highpass=f=80,"
        "equalizer=f=3000:t=q:w=1.5:g=2,"      # gentle presence boost (clarity)
        "deesser=i=0.3,"
        "acompressor=threshold=-15dB:ratio=3:attack=10:release=200:makeup=2"
    )
    subprocess.run([
        str(FFMPEG_BIN), "-y", "-i", str(raw_wav),
        "-af", filt,
        str(out_wav),
    ], check=True, capture_output=True)

def build_sfx_track(placement: dict, total_ms: int) -> AudioSegment:
    silent = AudioSegment.silent(duration=total_ms, frame_rate=48000)
    count = 0
    for entry in placement["sfx"]:
        file_path = ROOT / entry["file"]
        if not file_path.exists():
            print(f"  ! missing SFX file, skipping: {entry['file']}")
            continue
        clip = AudioSegment.from_file(file_path)
        gain_db = db_to_gain(entry.get("level", "-16dB"))
        clip = clip.apply_gain(gain_db - clip.max_dBFS if clip.max_dBFS != float("-inf") else 0)
        clip = clip + gain_db  # normalize-ish then apply target level

        placements = entry.get("placements")
        if placements is None:
            placements = [{"startFrame": entry["startFrame"]}]
        for p in placements:
            pos_ms = frame_to_ms(p["startFrame"])
            if pos_ms < 0 or pos_ms > total_ms:
                continue
            silent = silent.overlay(clip, position=pos_ms)
            count += 1
    print(f"  placed {count} SFX instances")
    return silent

def main():
    placement = json.loads((ROOT / "data" / "sfx_placement.json").read_text(encoding="utf-8"))
    total_ms = frame_to_ms(placement["meta"]["durationFrames"])

    print("1. Cleaning up voice track...")
    raw_voice = ROOT / "data" / "audio" / "voice_raw.wav"
    clean_voice_path = ROOT / "tools" / "voice_clean.wav"
    clean_voice(raw_voice, clean_voice_path)
    voice = AudioSegment.from_file(clean_voice_path)
    if len(voice) < total_ms:
        voice = voice + AudioSegment.silent(duration=total_ms - len(voice))
    voice = voice[:total_ms]

    print("2. Building SFX track...")
    sfx_track = build_sfx_track(placement, total_ms)

    print("3. Loading + looping/trimming music bed...")
    music_path = ROOT / placement["music"]["file"]
    music = AudioSegment.from_file(music_path)
    while len(music) < total_ms:
        music = music + music
    music = music[:total_ms]

    print("4. Writing foreground (voice+SFX) and music bed as separate stems...")
    voice = voice.set_frame_rate(48000).set_channels(2)
    sfx_track = sfx_track.set_frame_rate(48000).set_channels(2)
    music = music.set_frame_rate(48000).set_channels(2) - 10  # base bed level before ducking

    foreground = voice.overlay(sfx_track)
    foreground_path = ROOT / "tools" / "foreground_voice_sfx.wav"
    music_path_out = ROOT / "tools" / "music_bed_trimmed.wav"
    foreground.export(foreground_path, format="wav")
    music.export(music_path_out, format="wav")
    print(f"  foreground: {foreground_path}  ({len(foreground)/1000:.1f}s)")
    print(f"  music bed:  {music_path_out}  ({len(music)/1000:.1f}s)")

    print("5. Sidechain-ducking music under the foreground (real compressor, keyed to voice+sfx)...")
    final_path = ROOT / "mixed_audio_final.wav"
    # sidechaincompress: music is the main input, foreground is the sidechain
    # key — music ducks automatically whenever voice/SFX is present.
    filter_complex = (
        "[1:a][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=10:release=300[ducked];"
        "[0:a][ducked]amix=inputs=2:weights=1 1:normalize=0[out]"
    )
    subprocess.run([
        str(FFMPEG_BIN), "-y",
        "-i", str(foreground_path),
        "-i", str(music_path_out),
        "-filter_complex", filter_complex,
        "-map", "[out]",
        str(final_path),
    ], check=True, capture_output=True)
    print(f"✓ Wrote final mixed audio to {final_path}")

if __name__ == "__main__":
    main()
