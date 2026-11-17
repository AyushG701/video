# The Complete Workflow

## 🔄 How it works (you to me)

### Step 1: You give me transcript (plain text)

```
rawtrascript.txt
─────────────────────
पैसा थोरै हुँदा त सुख छैन,
अब धेरै हुँदा पनि सुख छैन...
5% Deposit Scheme...
Retained Saving...
Housing Australia Government...
```

**Format:** Any of these:
- VTT format (00:00:00,000 --> 00:00:05,000 + text)
- Plain text (I estimate timings at 150 wpm)
- With speaker tags or without

### Step 2: I convert to JSON automatically

```bash
python py-scripts/parse_transcript.py rawtrascript.txt
```

Generates: `data/captions.json` with:
- **Word-by-word captions** (timing + color logic applied)
- **Panel rows** (icon tiles + labels)
- **Motifs** (coin-stack, arrows, CTA timing)

### Step 3: I wire into Remotion component

```tsx
// src/Root.tsx
import captionsData from "../data/captions.json";

<KineticWord word={caption.text} colorTag={caption.colorTag} startFrame={caption.startFrame} />
<RealityList rows={panel.rows} startFrame={panel.startFrame} />
<CoinStack startFrame={motif.startFrame} />
```

### Step 4: You render

```bash
npm run render -- src/Root.tsx Yatri-Mortgage-Edit out/my-edit.mov
```

Output: **ProRes 4444 alpha layers** (transparent, ready for CapCut)

---

## 📋 What the parser does automatically

### 1. Color logic (keywords → tags)

| Keyword | Color | Meaning |
|---------|-------|---------|
| "5% Deposit Scheme" | 🟨 Yellow | Subject noun |
| "5%" | 🟩 Green | Money / percentage |
| "पाउनुहुन्न" / "defeats" | 🔴 Red | Restriction / negative |
| Other words | ⚪ White | Neutral |
| Panel labels | 🟦 Navy | Static text |

### 2. Font detection

- Devanagari script (पा, त, etc.) → `Noto Sans Devanagari`
- Latin (English) → `Montserrat`

### 3. Timing

**If you provide VTT format:**
- Extracts exact start/end timestamps
- Splits into words
- Each word gets proportional duration

**If you provide plain text:**
- Estimates at 150 wpm (adjustable)
- Each word gets ~0.4s duration

### 4. Panel generation

Automatically creates two sections:
- "The Reality" (OLD rule)
- "How to Protect Yourself" (exceptions)

With hardcoded rows (you can edit these in the script).

### 5. Motif timings

Pre-places:
- Coin-stack graphic at frame 1050
- CTA card at frame 2340

(Edit these in the script if needed)

---

## 🎬 You are ready to do this:

### TODAY

1. **Provide your transcript** (even if it's messy):
   ```
   "here is my raw transcript for the video..."
   ```
   Or a file like `rawtrascript.txt`

2. I run:
   ```bash
   python py-scripts/parse_transcript.py your-transcript.txt
   ```

3. I wire it into `src/Root.tsx` (copy from `Root-example.tsx`)

4. You render:
   ```bash
   npm install  # one-time
   npm run render -- src/Root.tsx Yatri-Mortgage-Edit out/edit.mov
   ```

5. Stack the `.mov` file in CapCut over your base video

---

## 🛠️ If you want to tweak colors or timing

**Edit the script:**

```python
# py-scripts/parse_transcript.py

COLOR_MAP = {
    "my keyword": "yellow",   # Add custom keywords here
    "5%": "green",
    "restriction word": "red",
}
```

Then re-run:
```bash
python py-scripts/parse_transcript.py rawtrascript.txt
```

The JSON regenerates, and the video updates automatically on next render.

---

## 📦 What you'll have after rendering

```
out/
├─ edit.mov               ← Main render (ProRes 4444 alpha)
├─ edit0000.png          ← Frame sequence (fallback)
├─ ...
└─ edit2606.png          ← Last frame
```

**All files have true transparency.** Stack in CapCut:
1. Base video (bottom)
2. `edit.mov` (top)
3. Grade base, adjust opacity/blend modes, add SFX

---

## 🎯 Next step: Give me your transcript

Just paste your transcript (or attach the file), and I'll:
1. Parse it
2. Generate the JSON
3. Wire it into Remotion
4. Show you the preview

Then you can tweak colors, timing, or anything else before final render.

---

**TL;DR:**
> You → Transcript (raw text)  
> Me → JSON (auto-colored, timed)  
> Then → React components  
> Then → Video (ProRes alpha)  
> Then → CapCut (stack + grade)
