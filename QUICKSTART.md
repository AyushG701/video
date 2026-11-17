# Quick Start — Yatri Video Editor

## What you have

A **Remotion-based video editing engine** ready to go. Zero hardcoding of captions/graphics — everything feeds from your transcript JSON.

```
E:\video-edit\video/
├─ src/
│  ├─ components/
│  │  ├─ KineticWord.tsx       (word pops with spring + color)
│  │  ├─ RealityList.tsx       (icon tile rows)
│  │  └─ CoinStack.tsx         (coins + house + arrow)
│  ├─ lib/spring.ts           (design system + spring config)
│  └─ Root.tsx                (main composition)
├─ design-systems/            (design spec JSON)
├─ data/                       (your transcript goes here)
├─ assets/                     (emoji, icons, SFX)
├─ CLAUDE.md                   (agent rules)
└─ README.md                   (full docs)
```

## Your next steps

### 1. Install & setup (5 min)

```bash
cd E:\video-edit\video
npm install
python py-scripts/00_download_assets.py
```

This downloads Fluent emoji + Lucide icons.

### 2. Create your transcript JSON

Place it in `data/your-video.json` using the template: `data/transcript-template.json`

**Key fields:**
- `captions[]` — word-by-word (text, startFrame, endFrame, colorTag)
- `panels[]` — icon rows (title, rows with icon/label)
- `motifs[]` — animations (coin-stack, arrows, etc.)
- `sfx[]` — sound hits (file path, startFrame)

**Color tags:**
- `"yellow"` = subject nouns (5% Scheme, Retained Savings)
- `"green"` = money/percentages (5%, 10%, 6 months)
- `"red"` = restrictions/negatives (cannot, defeats, change)
- `"white"` = neutral words
- `"navy"` = static labels

### 3. Build your composition

Edit `src/Root.tsx`:

```tsx
import { KineticWord } from "./components/KineticWord";
import { RealityList } from "./components/RealityList";
import { CoinStack } from "./components/CoinStack";
import transcriptData from "../data/your-video.json";

export const MyVideo = () => {
  return (
    <div style={{ width: 1080, height: 1920, backgroundColor: "#000" }}>
      {/* Video frame */}
      <div style={{ /* styles */ }}>
        Video layer here
      </div>

      {/* Kinetic captions */}
      {transcriptData.captions.map((cap, i) => (
        <KineticWord
          key={i}
          word={cap.text}
          x={cap.x || 540}
          y={cap.y || 960}
          colorTag={cap.colorTag}
          fontFamily={cap.fontFamily}
          startFrame={cap.startFrame}
          duration={cap.endFrame - cap.startFrame}
        />
      ))}

      {/* Icon rows */}
      {transcriptData.panels.map((panel, i) => (
        <RealityList
          key={i}
          title={panel.title}
          rows={panel.rows.map(row => ({
            icon: <div>icon</div>, // load from assets
            label: row.label,
            value: row.value,
          }))}
          startFrame={panel.startFrame}
        />
      ))}

      {/* Coin stack motif */}
      {transcriptData.motifs
        .filter(m => m.type === "coin-stack")
        .map((motif, i) => (
          <CoinStack
            key={i}
            coinImagePath="assets/emoji3d/coin_3d.png"
            houseImagePath="assets/emoji3d/house_3d.png"
            startFrame={motif.startFrame}
            x={motif.x}
            y={motif.y}
          />
        ))}
    </div>
  );
};
```

### 4. Preview

```bash
npm run dev
```

Browser opens. Edit `src/Root.tsx`, save, it hot-reloads.

### 5. Render

```bash
npm run render -- src/Root.tsx Yatri-Video-Edit out/my-video.mov
```

Outputs: `out/my-video.mov` (ProRes 4444, transparent alpha).

### 6. Stack in CapCut

1. Import your base video clip (the raw footage)
2. Stack the `.mov` layers on top (captions, graphics, motifs)
3. Add SFX from your `data/my-video.json` sfx list
4. Export final

## Key design principles

✓ **Springs only** — no linear fades. All motion uses `spring({damping: 12, stiffness: 200})`
✓ **Devanagari safe** — Noto Sans Devanagari, split by word (not character)
✓ **Color semantics** — yellow/green/red/white/navy mean specific things
✓ **Transparent output** — ProRes 4444 alpha, not merged video
✓ **30fps lock** — no 24/30 mismatches

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "npm not found" | Install Node.js from nodejs.org |
| "Devanagari looks broken" | Font loading issue. Check `@remotion/google-fonts` is working. |
| "Alpha has dark edges" | Render with `--prores-profile=4444 --pixel-format=yuva444p10le` |
| "Fonts not loading" | Make sure fonts are on Google Fonts. See `src/lib/spring.ts` |

## Next: I need you to provide

1. **Your transcript JSON** — captions with timing, colors, etc. (use template as guide)
2. **Raw video** — `raw1.MOV` already in the folder
3. **Any custom assets** — if you have logos, etc., drop them in `assets/brand/`

Then I'll wire everything into the composition and you can render.

---

**You're in control.** I build components, you feed data. No auto-transcription, no guessing — just clean React that reads your design system.
