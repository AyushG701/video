# Yatri Mortgage Video Editor

A Remotion-based video editing engine for creating clean, information-dense explainer videos. Clones the Yatri mortgage reference design language with kinetic captions, icon tiles, and animated graphics.

## Quick start

### 1. Install dependencies

```bash
npm install
```

### 2. Download assets

```bash
pip install requests
python py-scripts/00_download_assets.py
```

This downloads:
- 18 Fluent 3D emoji (house, coins, arrows, etc.)
- 20 Lucide SVG icons (bank, ruler, calendar, etc.)
- Creates checklist for manual SFX download

### 3. Prepare your transcript

Create a JSON file with your caption data. Example:

```json
{
  "fps": 30,
  "captions": [
    {
      "text": "पैसा थोरै",
      "startFrame": 0,
      "endFrame": 72,
      "colorTag": "yellow",
      "font": "Noto Sans Devanagari"
    },
    {
      "text": "सुख छैन",
      "startFrame": 72,
      "endFrame": 150,
      "colorTag": "white"
    }
  ],
  "panels": [
    {
      "title": "The Reality",
      "startFrame": 240,
      "rows": [
        {
          "icon": "bank",
          "label": "OLD: Bank Policy",
          "value": "5% Deposit"
        }
      ]
    }
  ]
}
```

### 4. Build your composition

Edit `src/Root.tsx` to wire in your transcript data. Use the provided components:

- **KineticWord** — single word with spring pop + color
- **RealityList** — icon tile rows with slide-up animation
- **CoinStack** — the signature "coins + house + arrow" graphic

### 5. Preview & render

```bash
# Preview in browser
npm run dev

# Render as ProRes 4444 (alpha) for CapCut
npm run render -- src/Root.tsx Yatri-Video-Edit out/my-edit.mov

# Or PNG sequence (fallback)
npm run render:sequence
```

## Design system

All design decisions live in `design-systems/yatri-mortgage-nepali.json`:
- Colors (yellow, green, red, navy)
- Fonts (Noto Sans Devanagari, Montserrat, etc.)
- Motion params (spring config, timing)
- Layout (video frame size, panel position)

**Read it before building components.**

## Agent rules (CLAUDE.md)

Agent instructions for consistent editing:
- Nepali text must be split by word (not character) to preserve Devanagari conjuncts
- Springs only (no linear fades)
- Color logic: yellow = nouns, green = money, red = restrictions, white = neutral, navy = labels
- Output: ProRes 4444 alpha layers (not merged video)

## Component reference

### KineticWord

```tsx
<KineticWord
  word="पैसा"
  x={540}
  y={960}
  colorTag="yellow"
  fontSize={46}
  fontFamily="Noto Sans Devanagari"
  startFrame={0}
  duration={12}
/>
```

### RealityList

```tsx
<RealityList
  title="The Reality"
  rows={[
    { icon: <BankIcon />, label: "OLD: Bank Policy" },
    { icon: <RulerIcon />, label: "Minimum Criteria" },
  ]}
  startFrame={240}
/>
```

### CoinStack

```tsx
<CoinStack
  coinImagePath="assets/emoji3d/coin_3d.png"
  houseImagePath="assets/emoji3d/house_3d.png"
  startFrame={1050}
  x={540}
  y={600}
/>
```

## Workflow

1. **You provide** → transcript JSON (captions, timing, colors)
2. **I build** → React components that render the edit
3. **Export** → transparent ProRes 4444 layers
4. **Stack in CapCut** → grade the base, layer graphics, add SFX

## Export checklist

Before declaring done:
- [ ] All ProRes files have true alpha (corner pixel = `rgba(0,0,0,0)`)
- [ ] 30fps lock (no 24/30 drift)
- [ ] Devanagari renders correctly (no broken conjuncts)
- [ ] All colors match the design system
- [ ] All timing matches the reference or design spec

## Troubleshooting

**"Devanagari looks wrong"**
→ Chromium (Remotion) handles it. If wrong, check the font is loaded correctly via `@remotion/google-fonts`.

**"Alpha is dark/has fringes"**
→ Make sure you render as `--prores-profile=4444 --pixel-format=yuva444p10le`. PNG sequence is a fallback if needed.

**"My SFX are too loud/quiet"**
→ Normalize to -16dB peak before import. CapCut will read the meta anyway, but clear SFX mixes easier.

## Stack

- **Remotion** — React video engine (handles Devanagari, springs, alpha)
- **@remotion/google-fonts** — font loading (Noto Sans Devanagari, etc.)
- **@remotion/animation-utils** — spring physics
- **TypeScript** — type safety
- **FFmpeg** (optional) — post-processing, loudness normalization

## License

This project uses:
- Fluent Emoji (Microsoft, MIT)
- Lucide icons (ISC)
- Kenney SFX (CC0)
- Noto Sans Devanagari (OFL)

All commercial-safe. See `assets/manifest.json` for per-file attribution.
