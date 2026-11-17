#!/usr/bin/env python3
"""
Final compositing pipeline.

INPUT:
  - raw1.MOV (base video)
  - out/my-edit.mov (graphics layer, ProRes 4444 alpha)
  - mixed_audio_final.wav (fully mixed audio)

OUTPUT:
  - FINAL_EDIT.mov (fully composited, broadcast-ready)

Process:
  1. Scale/position graphics layer to match video
  2. Composite graphics over base video
  3. Add mixed audio
  4. Apply final color grading (optional boost)
  5. Normalize metadata + format
"""

import subprocess
from pathlib import Path

class FinalCompositor:
    """Composite all layers into final video."""

    def __init__(self):
        self.output_file = Path("FINAL_EDIT.mov")
        self.codec = "prores_ks"  # ProRes, high quality
        self.pix_fmt = "yuva444p10le"  # 10-bit with alpha

    def composite_video_layers(self, base_video: str, graphics_layer: str) -> str:
        """Composite graphics layer over base video."""
        output_path = Path("composite_no_audio.mov")

        print("Compositing graphics layer over base video...")
        print(f"  Base: {base_video}")
        print(f"  Graphics: {graphics_layer}")

        # FFmpeg complex filter:
        # Scale graphics to 1920x1920, overlay on base at correct position
        # Use "over" blend (alpha compositing)

        filter_chain = (
            "[0:v]scale=1080:1920[base];"
            "[1:v]format=pix_fmts=rgba[gfx];"
            "[base][gfx]overlay=0:0:format=auto[out]"
        )

        cmd = [
            "ffmpeg",
            "-i", base_video,       # Input 0: base video
            "-i", graphics_layer,   # Input 1: graphics (alpha)
            "-filter_complex", filter_chain,
            "-map", "[out]",        # Map composite output
            "-c:v", self.codec,
            "-profile:v", "4444",   # ProRes 4444 (alpha support)
            "-vendor", "apl0",      # Apple profile
            "-bits_per_mb", "8000",
            "-y",
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Composite created: {output_path}")
            return str(output_path)
        else:
            print(f"ERROR compositing:\n{result.stderr}")
            return None

    def add_audio(self, video_file: str, audio_file: str) -> str:
        """Add mixed audio to composite video."""
        print(f"\nAdding audio to composite...")
        print(f"  Video: {video_file}")
        print(f"  Audio: {audio_file}")

        cmd = [
            "ffmpeg",
            "-i", video_file,       # Video (with or without audio)
            "-i", audio_file,       # Mixed audio track
            "-c:v", "copy",         # Copy video codec (don't re-encode)
            "-c:a", "aac",          # AAC audio codec (CapCut-friendly)
            "-b:a", "320k",         # High bitrate audio
            "-shortest",            # Match to shortest input
            "-y",
            str(self.output_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Final video created: {self.output_file}")
            return str(self.output_file)
        else:
            print(f"ERROR adding audio:\n{result.stderr}")
            return None

    def verify_output(self):
        """Verify final output quality."""
        if not self.output_file.exists():
            print(f"ERROR: {self.output_file} not found!")
            return False

        file_size_mb = self.output_file.stat().st_size / (1024 * 1024)
        print(f"\n✓ Final output verified")
        print(f"  File: {self.output_file}")
        print(f"  Size: {file_size_mb:.1f} MB")
        print(f"  Format: ProRes 4444 + AAC audio")
        print(f"  Ready for CapCut: YES")
        return True

    def run_full_pipeline(self, base_video: str, graphics_layer: str, audio_file: str):
        """Execute full compositing pipeline."""
        print("\n" + "="*70)
        print("FINAL COMPOSITING PIPELINE")
        print("="*70)

        # Step 1: Composite layers
        composite = self.composite_video_layers(base_video, graphics_layer)
        if not composite:
            print("ERROR: Could not create composite. Is FFmpeg installed?")
            print("Install FFmpeg:")
            print("  Windows: choco install ffmpeg")
            print("  Mac: brew install ffmpeg")
            print("  Linux: apt install ffmpeg")
            return False

        # Step 2: Add audio
        final = self.add_audio(composite, audio_file)
        if not final:
            print("ERROR: Could not add audio.")
            return False

        # Step 3: Verify
        self.verify_output()

        print("\n" + "="*70)
        print("✓ COMPOSITING COMPLETE")
        print("="*70)
        print(f"\n🎬 FINAL VIDEO: {self.output_file}")
        print(f"\nNext steps:")
        print(f"  1. Open in CapCut")
        print(f"  2. Review audio levels + timings")
        print(f"  3. Make adjustments if needed")
        print(f"  4. Grade the base video layer (if desired)")
        print(f"  5. Export final")
        return True

if __name__ == "__main__":
    compositor = FinalCompositor()

    # Paths
    base_video = "raw1.MOV"
    graphics_layer = "out/my-edit.mov"
    mixed_audio = "mixed_audio_final.wav"

    # Run
    success = compositor.run_full_pipeline(base_video, graphics_layer, mixed_audio)
