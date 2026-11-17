# How to Render Your Video

Your `src/Root.tsx` is ready. It reads `data/captions.json` (auto-generated from `rawtrascript.txt`) and renders all the kinetic elements.

## 1️⃣ Install dependencies (one-time)

```powershell
cd E:\video-edit\video
npm install
```

This installs Remotion, React, fonts, and all the components.

## 2️⃣ Preview in browser (optional)

```powershell
npm run dev
```

Opens `http://localhost:3000` in your browser. You'll see the composition with:
- ✓ Your captions popping in with spring physics
- ✓ Icon rows sliding up
- ✓ Coin-stack graphic animating
- ✓ CTA card sliding in
- ✓ All timing from your transcript

**Hot-reload:** Edit `src/Root.tsx`, save, it updates in the browser instantly.

## 3️⃣ Render to video (the final step)

```powershell
npm run render -- src/Root.tsx Yatri-Mortgage-Edit out/my-edit.mov
```

**Output:** `out/my-edit.mov` (ProRes 4444, transparent alpha, ~87 seconds)

This will take **5-15 minutes** depending on your CPU. Remotion renders via Chromium, so it's real-time accurate.

### Render options:

**Faster (PNG sequence, fallback):**
```powershell
npm run render:sequence -- src/Root.tsx Yatri-Mortgage-Edit out/my-edit
```

**Higher quality (if you need it):**
```powershell
remotion render src/Root.tsx Yatri-Mortgage-Edit out/my-edit.mov `
  --codec=prores `
  --prores-profile=4444 `
  --pixel-format=yuva444p10le `
  --scale=1 `
  --concurrency=4
```

## 4️⃣ What you get

```
out/
├─ my-edit.mov    ← 1080×1920, transparent alpha, 87s, ~200MB
└─ (or PNG sequence if you used :sequence)
```

**All files have true transparency** (corner pixel = `rgba(0,0,0,0)`).

## 5️⃣ Stack in CapCut

1. Create a new project in CapCut (1080×1920)
2. Import your base video (`raw1.MOV`)
3. Stack the rendered layer on top (`my-edit.mov`)
4. Adjust opacity / blend modes as needed
5. Add SFX (you'll do this manually based on your timing)
6. Export final

---

## ⚙️ If you need to adjust colors or timing

### Change caption colors

Edit `py-scripts/parse_transcript.py`:

```python
COLOR_MAP = {
    "my keyword": "yellow",
    "5% Deposit": "green",
    "restriction": "red",
}
```

Then re-parse:
```powershell
python py-scripts/parse_transcript.py rawtrascript.txt
```

The JSON updates, and the video updates on next render.

### Change animation timing

Edit `src/Root.tsx` and adjust `startFrame` or `duration` values, then re-render.

### Change fonts or sizes

Edit the component files (`src/components/*.tsx`), save, then re-render.

---

## 🎯 Checklist before final export

- [ ] Preview looks good (`npm run dev`)
- [ ] All captions have correct colors
- [ ] Icon rows slide in at the right timing
- [ ] Coin-stack animates smoothly
- [ ] CTA appears at the end
- [ ] Duration matches your video (~87s)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "npm not found" | Install Node.js from nodejs.org |
| "Port 3000 in use" | Kill the process or use `npm run dev -- --port 4000` |
| Render takes forever | Reduce `--concurrency` or close other apps |
| "Module not found" | Run `npm install` again |
| Fonts look broken | Check `src/lib/spring.ts` — fonts load from Google Fonts |
| Alpha has dark edges | Use `--prores-profile=4444 --pixel-format=yuva444p10le` |

---

## Ready?

```powershell
npm install
npm run render -- src/Root.tsx Yatri-Mortgage-Edit out/my-edit.mov
```

Then watch the magic happen. ✨
