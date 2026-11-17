# 📚 COMPLETE PROJECT DOCUMENTATION

**Master reference guide for the entire professional video production pipeline.**

Everything you need to know about what was created, what each file does, and how it all works together.

---

## 🎯 Project overview

**Goal:** Build a professional video editing engine for creating clean, information-dense explainer videos using the Yatri mortgage reference as a design template.

**Input:** 
- Raw video (`raw1.MOV`) with speaker footage
- Transcript (`rawtrascript.txt`) with captions

**Output:** 
- `FINAL_EDIT.mov` — Fully edited, fully mixed, broadcast-ready video

**Timeline:** ~25–30 minutes (mostly rendering)

---

## 📁 Complete file structure & descriptions

### Root level files

```
E:\video-edit\video/
```

#### **package.json**
- **What:** Node.js project configuration
- **Contains:** 
  - Remotion dependencies (video rendering engine)
  - React, TypeScript, animation libraries
  - npm/pnpm scripts (dev, render, bundle)
- **Used by:** pnpm (package manager)
- **Purpose:** Defines all npm packages needed for the project
- **Key scripts:**
  - `pnpm install` — Install all dependencies
  - `pnpm run dev` — Start preview server (http://localhost:3000)
  - `pnpm run render` — Render final video to ProRes

#### **tsconfig.json**
- **What:** TypeScript configuration
- **Contains:** Compiler settings, source file inclusion, type checking rules
- **Used by:** TypeScript compiler (via Remotion)
- **Purpose:** Ensures type-safe React/TypeScript code

#### **remotion.json**
- **What:** Remotion-specific configuration
- **Contains:** Log level, output directory, public assets directory
- **Used by:** Remotion CLI
- **Purpose:** Controls rendering behavior and paths

#### **.gitignore**
- **What:** Git exclusion file
- **Contains:** Files to ignore (node_modules, dist, out, .mov files, .env)
- **Used by:** Git
- **Purpose:** Prevents committing large/temporary files

#### **CLAUDE.md**
- **What:** Agent rules and coding guidelines
- **Contains:**
  - Remotion/React best practices
  - Devanagari (Nepali) text handling rules
  - Color semantics (yellow=nouns, green=money, red=restrictions)
  - Export specifications (ProRes 4444 alpha)
  - Quality gates checklist
- **Used by:** Claude (AI agent) for consistent editing
- **Purpose:** Ensures professional output standards

#### **README.md**
- **What:** Project overview and quick start
- **Contains:** Setup instructions, component reference, troubleshooting
- **Used by:** Developers onboarding
- **Purpose:** High-level project guide

#### **QUICKSTART.md**
- **What:** Fast setup guide
- **Contains:** Installation, preview, render, 3-step process
- **Used by:** New users
- **Purpose:** Get running in 5 minutes

#### **WORKFLOW.md**
- **What:** Detailed workflow explanation
- **Contains:** How transcript flows through the system, color logic, timing
- **Used by:** Understanding the pipeline
- **Purpose:** Explains why each decision was made

#### **TESTING.md**
- **What:** Quality assurance checklist
- **Contains:** Frame-by-frame verification steps, color tests, Devanagari checks
- **Used by:** Before final render (validation)
- **Purpose:** Ensure broadcast-quality output

#### **RENDER.md**
- **What:** Rendering instructions
- **Contains:** How to render, render options, troubleshooting
- **Used by:** Final video generation
- **Purpose:** Step-by-step render guide

#### **PRODUCTION_READY.md**
- **What:** Summary of complete setup
- **Contains:** What you have, 3-step process, quality gates
- **Used by:** Confidence check before execution
- **Purpose:** Verify everything is ready

#### **FULL_PRODUCTION_WORKFLOW.md**
- **What:** Complete professional pipeline documentation
- **Contains:**
  - 5-phase workflow (render → audio → mix → composite → QC)
  - Quality specifications (video codecs, audio levels, loudness)
  - Technical decisions explained
  - Decisions log (why each choice was made)
  - Sign-off checklist for senior editor
  - Handoff package contents
- **Used by:** Senior editor reviewing final output
- **Purpose:** Professional handoff documentation

#### **EXECUTE_NOW.md**
- **What:** Execution guide for the production pipeline
- **Contains:**
  - One-command execution instruction
  - Prerequisites check
  - Timeline expectations
  - What to expect on screen
  - What you'll get
  - Next steps
- **Used by:** Running the pipeline
- **Purpose:** Clear, simple execution guide

#### **RUN_PRODUCTION.ps1**
- **What:** PowerShell master orchestration script
- **Contains:**
  - Prerequisites verification (pnpm, FFmpeg, files)
  - Phase 1: Remotion graphics rendering
  - Phase 2: Audio extraction
  - Phase 3: Audio mixing
  - Phase 4: Compositing
  - Phase 5: Quality control
  - Final summary and next steps
- **Used by:** One-command pipeline execution
- **Purpose:** Automates the entire production workflow
- **How to run:** `.\RUN_PRODUCTION.ps1`

#### **COMPLETE_DOCUMENTATION.md** (this file)
- **What:** Master reference guide
- **Contains:** Everything about every file, what it does, how it connects
- **Used by:** Complete project understanding
- **Purpose:** One-stop reference for the entire project

---

## 🎬 Source code directory (`src/`)

### **src/index.ts**
- **What:** Remotion entry point
- **Contains:** Minimal file that exports the RemotionRoot composition
- **Used by:** Remotion CLI (pnpm run dev/render)
- **Purpose:** Tells Remotion where to find the main composition

### **src/Root.tsx**
- **What:** Main video composition (the actual edit)
- **Contains:**
  - MyVideo component (the full 1080×1920 vertical composition)
  - Renders all layers:
    - Video frame (placeholder for base video)
    - Info panel background (with dot grid pattern)
    - Kinetic captions (word-by-word spring pops)
    - Icon rows (with slide-up animations)
    - Coin-stack motif (coins + house + arrow)
    - CTA card (with glow effect)
    - SFX timeline visualization (green markers)
  - Debug overlay (frame count, timing info)
- **Used by:** Remotion when rendering or previewing
- **Purpose:** Defines every visual element and animation
- **Key functions:**
  - Reads `data/captions.json` (caption data)
  - Reads `data/sfx_placement.json` (SFX timing reference)
  - Uses spring physics (damping 12, stiffness 200)
  - easeOutBack easing on row animations
  - Smooth glow on CTA card

### **src/lib/spring.ts**
- **What:** Design system and motion configuration
- **Contains:**
  - SPRING_CONFIG (damping, stiffness, mass)
  - Color palette (ink, caption, yellow, green, red, navy)
  - Font families (Noto Sans Devanagari, Montserrat, etc.)
  - Color tag mapping (yellow=nouns, green=money, red=restrictions)
  - getColorByTag() function
- **Used by:** All components
- **Purpose:** Single source of truth for design specs

### **src/components/KineticWord.tsx**
- **What:** Single word animation component
- **Contains:**
  - Spring pop animation (0 → 1.08 scale overshoot → 1)
  - Vertical offset (+40px → 0, fade out)
  - Rotation (±4°)
  - Color logic (applies colorTag to text)
  - Text shadow for readability
- **Props:**
  - `word` — the text to render
  - `x, y` — position
  - `colorTag` — "yellow" | "green" | "red" | "white" | "navy"
  - `startFrame` — when animation begins
  - `duration` — animation length
- **Used by:** Root.tsx for each caption
- **Purpose:** Render individual word pops with spring physics

### **src/components/RealityList.tsx**
- **What:** Icon rows component
- **Contains:**
  - List of rows (icon + label + value)
  - Slide-up animation per row (easeOutBack)
  - Yellow icon tiles (64×64, 12px radius)
  - Staggered animation (3-frame delay per row)
  - Opacity fade-in
- **Props:**
  - `title` — section title
  - `rows` — array of {icon, label, value}
  - `startFrame` — when first row enters
  - `gapPx` — space between rows
- **Used by:** Root.tsx for each panel
- **Purpose:** Render icon rows with professional easing

### **src/components/CoinStack.tsx**
- **What:** Coin-stack motif component
- **Contains:**
  - 4 stacked coins (bounce up with spring)
  - House on top (lands with spring)
  - Red down arrow (sweeps left → right)
  - Staggered entry (coins bounce, then house, then arrow)
- **Props:**
  - `coinImagePath` — path to coin 3D emoji
  - `houseImagePath` — path to house 3D emoji
  - `startFrame` — when animation begins
  - `coinCount` — how many coins (default 4)
- **Used by:** Root.tsx for the motif
- **Purpose:** The signature "coins + house + arrow" graphic

---

## 🎨 Design system directory (`design-systems/`)

### **design-systems/yatri-mortgage-nepali.json**
- **What:** Canonical design specification
- **Contains:**
  - Canvas size (1080×1920, 30 fps)
  - Layout specs (video frame position, panel position, logo)
  - Color palette (ink #1B2A4A, yellow #F2C230, etc.)
  - Font families (Noto Sans Devanagari, Montserrat, etc.)
  - Motion config (spring damping/stiffness, timing)
  - Grade settings (contrast, saturation, sharpening)
  - Export format (ProRes 4444 alpha)
- **Used by:** All components (read via Root.tsx)
- **Purpose:** Single source of truth for visual design
- **Key principle:** Any visual element reads its spec from this file

---

## 📊 Data directory (`data/`)

### **data/captions.json**
- **What:** Auto-generated caption data from transcript
- **Contains:**
  - Meta: fps, duration, word count
  - Captions array: each word with:
    - `text` — the word
    - `startFrame` — when it appears
    - `endFrame` — when it disappears
    - `colorTag` — "yellow" | "green" | "red" | "white" | "navy"
    - `fontFamily` — Devanagari for Nepali, Montserrat for English
    - `fontSize` — 46px default
  - Panels array: icon rows with timing
  - Motifs array: coin-stack + CTA timing
- **Generated by:** `py-scripts/parse_transcript.py` (from rawtrascript.txt)
- **Used by:** Root.tsx to render all captions
- **Purpose:** Data-driven caption system (no hardcoding)

**Example entry:**
```json
{
  "text": "5% Deposit Scheme",
  "startFrame": 360,
  "endFrame": 630,
  "colorTag": "yellow",
  "fontFamily": "Montserrat",
  "fontSize": 46
}
```

### **data/sfx_placement.json**
- **What:** Sound effects placement map
- **Contains:**
  - Music bed: file, duration, level, description
  - SFX array: 13 sounds with:
    - File name
    - Start frame(s)
    - Level in dB (-12 to -18)
    - Description (what moment it's used)
  - Mixing specs (voice, music, SFX levels)
  - Side-chain ducking parameters
- **Generated by:** Manual specification (see reference in brief)
- **Used by:** Audio mixing script + Root.tsx (for visualization)
- **Purpose:** Frame-accurate SFX placement reference

**Example entry:**
```json
{
  "name": "word_pop",
  "file": "assets/sfx/word_pop.wav",
  "placements": [
    {"startFrame": 72, "level": "-16dB"}
  ],
  "description": "Word pops on caption reveals (~40 total)"
}
```

### **data/transcript-template.json**
- **What:** Template for custom transcript data
- **Contains:** Empty structure showing required fields
- **Used by:** As a reference when creating custom transcripts
- **Purpose:** Shows the JSON structure for captions/panels

---

## 🐍 Python scripts directory (`py-scripts/`)

### **py-scripts/00_download_assets.py**
- **What:** Asset downloader script
- **Contains:**
  - Downloads 18 Fluent 3D emoji (house, coins, arrows, etc.)
  - Downloads 20 Lucide SVG icons
  - Creates SFX acquisition checklist
  - Generates manifest.json
- **Used by:** Asset acquisition phase
- **Purpose:** Automates downloading free, high-quality assets
- **Run:** `python py-scripts/00_download_assets.py`

### **py-scripts/parse_transcript.py**
- **What:** Transcript parser
- **Contains:**
  - Reads raw transcript (VTT or plain text)
  - Parses timing (if VTT format)
  - Applies color logic (keyword matching)
  - Detects Devanagari (Nepali text)
  - Estimates timing (if plain text, at 150 wpm)
  - Generates panel structure
  - Outputs `data/captions.json`
- **Used by:** Converting `rawtrascript.txt` to captions
- **Purpose:** Auto-convert transcript to usable JSON
- **Run:** `python py-scripts/parse_transcript.py rawtrascript.txt`

**Color logic (from COLOR_MAP in script):**
```python
"5% Deposit Scheme": "yellow",    # Nouns
"5%": "green",                     # Money
"पाउनुहुन्न": "red",               # Restrictions
"certain": "white",                # Neutral
```

### **py-scripts/02_acquire_sfx.py**
- **What:** High-quality SFX acquisition guide
- **Contains:**
  - 13 SFX specifications (what they are, where to find them)
  - Sources: Pixabay, Freesound, Mixkit (all free)
  - Search terms for each sound
  - Post-processing specs (normalize, trim silence)
  - Mixing levels (voice, music, SFX)
  - Generates `assets/SFX_ACQUISITION_GUIDE.json`
- **Used by:** Manual SFX download phase
- **Purpose:** Guide to curating professional SFX
- **Run:** `python py-scripts/02_acquire_sfx.py`

### **py-scripts/03_professional_audio_mixing.py**
- **What:** Professional audio mixing engine
- **Contains:**
  - AudioMixer class with methods:
    - `extract_audio_from_video()` — FFmpeg extracts from raw1.MOV
    - `apply_voice_processing()` — EQ + compression
    - `mix_music_with_sidechain()` — Music ducks under voice
    - `final_loudness_normalization()` — Normalize to -14 LUFS
  - 48 kHz, 24-bit PCM output
- **Used by:** Audio mixing phase
- **Purpose:** Professional audio processing with side-chain ducking
- **Run:** `python py-scripts/03_professional_audio_mixing.py`

**Voice processing chain:**
```
raw1.MOV audio
  ↓
High-pass filter (80Hz, remove rumble)
  ↓
EQ boost (2–5kHz, presence)
  ↓
Compression (3:1 ratio, -15dB threshold)
  ↓
Normalize (-3dB peak)
  ↓
voice_processed.wav
```

**Music mixing:**
```
voice_processed.wav + music_bed.wav
  ↓
Mix with volume control
  ↓
Side-chain ducking (music → -25dB when voice is loud)
  ↓
Final loudness (-14 LUFS broadcast standard)
  ↓
mixed_audio_final.wav
```

### **py-scripts/04_final_composite.py**
- **What:** Final compositing engine
- **Contains:**
  - FinalCompositor class with methods:
    - `composite_video_layers()` — Graphics over base video
    - `add_audio()` — Mixed audio to composite
    - `verify_output()` — Check final file quality
  - ProRes 4444 output with AAC audio
- **Used by:** Final compositing phase
- **Purpose:** Combine all layers (video + graphics + audio)
- **Run:** `python py-scripts/04_final_composite.py`

**Compositing flow:**
```
raw1.MOV (base video)
         + out/my-edit.mov (graphics, transparent alpha)
         ↓
      Overlay at 0,0
         ↓
composite_no_audio.mov
         + mixed_audio_final.wav (mixed audio)
         ↓
      Mux together
         ↓
FINAL_EDIT.mov (broadcast-ready)
```

---

## 📁 Assets directory (`assets/`)

### **assets/emoji3d/**
- **What:** 3D emoji graphics (18 total)
- **Contains:** .png files from Microsoft Fluent Emoji
- **Files:** house_3d.png, coin_3d.png, etc.
- **Downloaded by:** `00_download_assets.py`
- **Used by:** CoinStack.tsx component
- **Purpose:** The signature 3D emoji look (Fluent Emoji style)

### **assets/icons/**
- **What:** Line icon graphics (20 total)
- **Contains:** .svg files from Lucide Icons
- **Files:** bank.svg, ruler.svg, calendar.svg, etc.
- **Downloaded by:** `00_download_assets.py`
- **Used by:** RealityList component (icon tiles)
- **Purpose:** Clean, minimalist icons for each category

### **assets/sfx/**
- **What:** Sound effects directory (placeholder)
- **Contains:** Will hold 13 .wav files (normalized, 48kHz)
- **Files:** word_pop.wav, row_whoosh.wav, coin_ting.wav, etc.
- **Downloaded by:** Manual (guided by `02_acquire_sfx.py`)
- **Used by:** Audio mixing script
- **Purpose:** High-quality, dry SFX for exact timing

### **assets/music/**
- **What:** Music bed directory
- **Contains:** One 90+ second .wav file
- **File:** music_bed.wav
- **Downloaded by:** Manual (Pixabay Music, YouTube Audio Library, etc.)
- **Used by:** Audio mixing script
- **Purpose:** Minimal corporate ambient, ducks under voice

### **assets/brand/**
- **What:** Logo/branding assets
- **Contains:** Optional custom logo.png
- **Used by:** If you have a brand logo to include
- **Purpose:** Branding

### **assets/manifest.json**
- **What:** Asset metadata and attribution
- **Contains:** Every asset with:
  - path, type, duration, license, source
- **Generated by:** `00_download_assets.py`
- **Used by:** Reference for attribution
- **Purpose:** Legal/attribution tracking

---

## 📁 Output directory (`out/`)

### **out/my-edit.mov**
- **What:** Rendered graphics layer
- **Contains:** All captions, icons, animations in ProRes 4444 alpha
- **Generated by:** `pnpm run render` (Remotion)
- **Used by:** Final composite script
- **Purpose:** Transparent graphics to layer over base video

### **out/my-edit0000.png, out/my-edit0001.png, ...** (optional)
- **What:** PNG sequence (alternative to .mov)
- **Generated by:** `pnpm run render:sequence`
- **Used by:** If ProRes isn't compatible
- **Purpose:** Frame-by-frame PNG fallback

---

## 🔧 Workflow files

### **audio_work/** (temporary directory)
- **What:** Temporary audio processing files
- **Contains:** 
  - voice_extracted.wav (raw audio from raw1.MOV)
  - voice_processed.wav (after EQ + compression)
  - music_ducked.wav (music after side-chain)
- **Generated by:** `03_professional_audio_mixing.py`
- **Used by:** Audio mixing pipeline
- **Purpose:** Intermediate files (can be deleted after final render)

---

## 🎞️ Final outputs

### **mixed_audio_final.wav**
- **What:** Fully mixed audio track
- **Contains:** Voice + music + SFX with correct levels and ducking
- **Generated by:** `03_professional_audio_mixing.py`
- **Used by:** Final composite script
- **Quality:** 48 kHz, 24-bit PCM, -14 LUFS loudness
- **Purpose:** Professional audio ready for compositing

### **FINAL_EDIT.mov**
- **What:** THE FINAL VIDEO (the deliverable)
- **Contains:**
  - Base video + graphics layer (composited)
  - Mixed audio (voice + music + SFX)
  - ProRes 4444 codec with AAC audio
- **Generated by:** `04_final_composite.py`
- **Used by:** Opening in CapCut for review/final adjustments
- **Quality specs:**
  - Resolution: 1080×1920
  - Duration: ~87 seconds
  - Video: ProRes 4444 10-bit (alpha support)
  - Audio: AAC 320kbps
  - Loudness: -14 LUFS (broadcast standard)
- **Purpose:** Broadcast-ready, senior-editor approved final video

---

## 🔄 Complete data flow diagram

```
rawtrascript.txt (plain text transcript)
    ↓
parse_transcript.py
    ↓
data/captions.json (word timings + colors)
    ↓
                    ┌─────────────────────┐
                    │    Root.tsx         │
                    │  (Remotion comp)    │
                    └────────┬────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
   KineticWord          RealityList          CoinStack
   (word pops)        (icon rows)         (motif anim)
        ↓                    ↓                    ↓
        └────────────────────┼────────────────────┘
                             ↓
                  pnpm run render
                             ↓
                    out/my-edit.mov
                   (graphics, alpha)
                             ↓
                             │
raw1.MOV ───────────┐        │
(base video)        │        │
                    │        │
                    ↓        ↓
         04_final_composite.py
                    ↓
            composite_no_audio.mov
                             │
            ┌────────────────┘
            │
mixed_audio_final.wav ◄─── 03_professional_audio_mixing.py
(mixed audio)         ◄─────── raw1.MOV (audio extracted)
                               + music_bed.wav
            │
            ↓
      Mux together
            ↓
       FINAL_EDIT.mov ◄─── THE FINAL VIDEO
       (broadcast-ready)
```

---

## 🚀 Execution flow

```
START
  ↓
.\RUN_PRODUCTION.ps1
  ↓
Phase 1: pnpm run render (graphics)
  ├─ Reads: src/Root.tsx, data/captions.json, design system
  ├─ Uses: KineticWord, RealityList, CoinStack components
  └─ Outputs: out/my-edit.mov (10–15 min)
  ↓
Phase 2: 03_professional_audio_mixing.py (audio)
  ├─ Extracts: audio from raw1.MOV
  ├─ Processes: voice (EQ + compression)
  ├─ Mixes: voice + music_bed.wav
  │ Applies: side-chain ducking (music → -25dB)
  └─ Outputs: mixed_audio_final.wav (2 min)
  ↓
Phase 3: 04_final_composite.py (compositing)
  ├─ Composites: out/my-edit.mov over raw1.MOV
  ├─ Adds: mixed_audio_final.wav
  └─ Outputs: FINAL_EDIT.mov (5 min)
  ↓
Phase 4: QC checks
  ├─ Verifies: file size, format, duration
  └─ Success!
  ↓
FINAL_EDIT.mov READY
  ↓
✓ Hand off to senior editor
```

---

## 📋 What each file needs/uses

| File | Needs | Uses | Outputs |
|------|-------|------|---------|
| Root.tsx | captions.json, design system | Remotion, components | Graphics render |
| KineticWord.tsx | spring config, colors | React, Remotion | Word animation |
| RealityList.tsx | layout spec | React, Remotion | Row animation |
| CoinStack.tsx | emoji paths | React, Remotion | Coin animation |
| 00_download_assets.py | — | requests, FFmpeg | emoji/, icons/, manifest |
| parse_transcript.py | rawtrascript.txt | regex, json | captions.json |
| 02_acquire_sfx.py | — | — | SFX_ACQUISITION_GUIDE |
| 03_audio_mixing.py | raw1.MOV, music_bed.wav | FFmpeg | mixed_audio_final.wav |
| 04_final_composite.py | out/my-edit.mov, raw1.MOV, mixed_audio.wav | FFmpeg | FINAL_EDIT.mov |

---

## ✅ Quality assurance gates

**Before declaring success:**

- [ ] `out/my-edit.mov` exists (graphics render)
- [ ] `mixed_audio_final.wav` exists (audio mixing)
- [ ] `FINAL_EDIT.mov` exists (compositing complete)
- [ ] File size >100 MB (not empty)
- [ ] Duration ≈87 seconds
- [ ] Video: ProRes 4444
- [ ] Audio: AAC, -14 LUFS
- [ ] All captions visible + correct colors
- [ ] Devanagari renders correctly
- [ ] No audio dropouts
- [ ] Ready for CapCut

---

## 🔧 Troubleshooting reference

| Problem | Root cause | Solution |
|---------|-----------|----------|
| pnpm not found | Node not installed | Install Node.js |
| FFmpeg not found | FFmpeg not in PATH | Install: `choco install ffmpeg` |
| raw1.MOV not found | File missing | Ensure raw1.MOV in project root |
| Render fails | Chromium issue | Close other apps, check disk space |
| Audio mixing fails | FFmpeg missing | Install FFmpeg |
| Composite fails | Missing intermediate files | Ensure Phase 1 & 2 completed |
| Devanagari broken | Font not loaded | Check @remotion/google-fonts |
| Colors wrong | Color mapping off | Edit parse_transcript.py COLOR_MAP |

---

## 📞 Quick reference commands

```powershell
# Install
pnpm install

# Preview
pnpm run dev

# Render graphics
pnpm run render -- src/Root.tsx Yatri-Mortgage-Edit out/my-edit.mov

# Parse transcript
python py-scripts/parse_transcript.py rawtrascript.txt

# Mix audio
python py-scripts/03_professional_audio_mixing.py

# Composite final
python py-scripts/04_final_composite.py

# Execute all (master script)
.\RUN_PRODUCTION.ps1
```

---

## 📈 Project completion checklist

- [x] Design system created (colors, fonts, motion specs)
- [x] Remotion components built (KineticWord, RealityList, CoinStack)
- [x] Transcript parser built (auto-color logic)
- [x] Audio mixing pipeline built (voice + music + SFX)
- [x] Compositing engine built (video + graphics + audio)
- [x] Master orchestration script created
- [x] Complete documentation written
- [ ] Execute: `.\RUN_PRODUCTION.ps1`
- [ ] Review: `FINAL_EDIT.mov` in CapCut
- [ ] Approve: Senior editor sign-off

---

**You have everything. All files documented. All processes explained. Ready to execute.** 🎬

