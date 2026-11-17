# Testing Your Video Edit

Before final render, test everything works perfectly. This guide covers QA steps.

## 1️⃣ Browser Preview (npm run dev)

```powershell
npm run dev
# → Opens http://localhost:3000
```

**What to look for:**

### Visuals
- ✅ Captions pop in with spring bounce (not linear fade)
- ✅ All text colors are correct (yellow = scheme names, green = money, red = restrictions)
- ✅ Icon rows slide up smoothly (no jank)
- ✅ Coin-stack animates (coins bounce, house lands, arrow sweeps)
- ✅ CTA card slides up with glow effect
- ✅ No text clipping or overflow
- ✅ Devanagari renders correctly (conjuncts intact: "पाउनुहुन्न", "त्यो")

### Timing
- ✅ Green markers on timeline (bottom) show SFX placement
- ✅ Magenta flash when each SFX should trigger
- ✅ Timing matches the master spec (see `data/sfx_placement.json`)

### Performance
- ✅ No stuttering or frame drops
- ✅ Smooth 30fps playback
- ✅ Hot-reload works (edit and save → instant update)

---

## 2️⃣ Scrub through timeline (manual test)

Drag the timeline slider in the preview to test specific moments:

| Time | What to check | Expected |
|------|---|---|
| 0:00 | Opening | Sub-boom hits, word pops start |
| 0:08 | First panel row | Slide-in smooth, "bank" icon appears |
| 0:12 | Coin ting SFX marker | Green marker flashes, 5% money token |
| 0:29 | Record scratch moment | "but now..." pivot, dramatic marker |
| 0:39 | పाউనుhnुन्न + error buzz | Red text, error buzz marker |
| 0:54 | Panel 2 starts | "How to Protect Yourself" title |
| 1:08 | 6 months money token | Coin ting, green color |
| 1:24 | CTA build (riser SFX) | Card slides up, yellow glow pulsing |
| 1:25 | Mouse click | Click marker flashes, arrow animates |

---

## 3️⃣ Frame-by-frame verification

**Use the preview's frame controls:**

```
<< < > >>   Play  Duration display
```

Frame-step through critical moments:

### 0:00–0:08 (Hook)
- [ ] All captions have correct text + colors
- [ ] Spring pops are smooth (not snappy, not slow)
- [ ] No gibberish Devanagari

### 0:08–0:29 (Reality panel)
- [ ] 3 icon rows all present
- [ ] Slide-ups don't jitter
- [ ] Record scratch SFX marker at 0:29.1

### 0:29–0:54 (New rule + coin-stack)
- [ ] "Housing Australia Government" text correct
- [ ] Coin-stack animates smoothly
- [ ] Red down-arrow sweeps cleanly
- [ ] Error buzz markers at restriction moments

### 0:54–1:20 (Exceptions)
- [ ] 3 exception rows appear
- [ ] 6-month timing correct
- [ ] Green check marks pop

### 1:20–1:27 (CTA)
- [ ] Riser SFX marker at 1:24.2
- [ ] CTA card glows and slides
- [ ] Mouse click marker at 1:25.5
- [ ] Reverb tail marker at end

---

## 4️⃣ Color verification (critical)

**Match each caption against design spec:**

| Word type | Color | Frame in preview | Is correct? |
|---|---|---|---|
| "5% Deposit Scheme" | 🟨 Yellow | ~360 | ☐ |
| "5%" | 🟩 Green | ~369 | ☐ |
| "पाउनुहुन्न" | 🔴 Red | ~1185 | ☐ |
| "Housing Australia" | 🟨 Yellow | ~873 | ☐ |
| "Living Expenses" | 🟨 Yellow | ~1248 | ☐ |
| "certainly" / neutral | ⚪ White | most frames | ☐ |

If any colors are wrong, it's in the parse script. Edit:

```python
# py-scripts/parse_transcript.py
COLOR_MAP = {
    "my keyword": "yellow",
    "5%": "green",
    "restriction": "red",
}
```

Then re-parse:

```powershell
python py-scripts/parse_transcript.py rawtrascript.txt
```

The JSON updates, preview hot-reloads.

---

## 5️⃣ Devanagari rendering test

**Critical for Nepali text.**

Frame-step to these moments and verify conjuncts are intact (not broken):

| Nepali | Expected | Frame | ✓ |
|---|---|---|---|
| पाउनुहुन्न | ण्न (न्न conjunct) stays together | ~1185 | ☐ |
| त्यो | त्य (त consonant + य conjunct) | depends | ☐ |
| छ महिनाको | ष्ठ or similar | ~1248 | ☐ |
| धेरै | धे + रै | varies | ☐ |

If broken (looks like separate letters instead of conjuncts):
- **Font issue:** Check `Noto Sans Devanagari` is loading in `src/lib/spring.ts`
- **Render issue:** Chromium (Remotion) handles it correctly. If still wrong, it's a font loading delay.

**To test:** Pause at that frame, take a screenshot, compare with the original `rawtrascript.txt`.

---

## 6️⃣ Audio reference (after SFX acquisition)

Once you download the SFX, do a **dry run** of the mix:

### Quick check
1. Import `music_bed.wav` into Audacity/REAPER
2. Import 1-2 key SFX (sub_boom, word_pop, coin_ting)
3. Place them at the timings in `data/sfx_placement.json`
4. Set levels: music -25dB, SFX -16dB, voice -6dB
5. Listen for:
   - ✅ Music doesn't overpower voice
   - ✅ SFX are crisp and dry (no reverb)
   - ✅ Sub-boom is felt, not just heard
   - ✅ Pops are playful, not annoying

If anything sounds off, adjust in the audio file (trim, normalize, EQ) BEFORE importing into final mix.

---

## 7️⃣ Final checklist before render

- [ ] All captions visible and correct color
- [ ] All Devanagari renders (no broken text)
- [ ] All rows slide smoothly (no stutters)
- [ ] Coin-stack animates cleanly
- [ ] CTA card appears with glow
- [ ] SFX timeline (green dots) all visible
- [ ] Duration matches 86.9s (or close)
- [ ] No console errors (browser dev tools)
- [ ] Performance: solid 30fps (no drops)

---

## 8️⃣ If something looks wrong

| Problem | Diagnosis | Fix |
|---------|---|---|
| Caption text is gibberish | Encoding issue in parse script | Check `rawtrascript.txt` encoding (UTF-8) |
| Colors wrong (all white) | Color tag not applied | Re-run `parse_transcript.py` with updated COLOR_MAP |
| Animation jittery | Easing function conflict | Check `src/lib/spring.ts` SPRING_CONFIG |
| Text overflowing | Font size too large | Edit `KineticWord.tsx` fontSize prop |
| Devanagari broken | Font not loaded | Check @remotion/google-fonts in package.json |
| SFX markers not visible | sfx_placement.json not loading | Check import in Root.tsx |
| Timeline slider doesn't work | Browser issue | Reload page, clear cache |

---

## 🎬 Ready to render?

Once all tests pass, you're ready:

```powershell
npm run render -- src/Root.tsx Yatri-Mortgage-Edit out/my-edit.mov
```

The `.mov` file will have:
- ✅ Smooth, professional captions
- ✅ Polished animations (springs, easing)
- ✅ Correct timing + colors
- ✅ True alpha transparency
- ✅ Ready for CapCut

**Then:**
1. Stack `out/my-edit.mov` on top of `raw1.MOV` in CapCut
2. Import the SFX (use timings from `data/sfx_placement.json`)
3. Import music (use timings from `data/sfx_placement.json`)
4. Adjust blend modes (if needed)
5. Grade base video only
6. Export

---

**You're in control. Test thoroughly, then render with confidence.** ✨
