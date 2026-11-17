/**
 * Root.tsx — Four separate alpha-exportable Remotion compositions, per
 * CLAUDE.md: "Root.tsx is one <Composition> per effect (Captions, Panel,
 * Motifs, CTA). Each exports separately as alpha." The raw footage
 * (raw1.MOV) is NOT baked in here — it stays on CapCut's own timeline;
 * these four layers render with transparent backgrounds and stack on top
 * of it there.
 *
 * A fifth composition ("Preview-Stacked") bakes the real H.264 footage in
 * underneath all four layers for QC only — never export it as a final
 * deliverable, it exists purely to sanity-check layering/sync on screen.
 */

import React from "react";
import { Composition, staticFile, Video, useCurrentFrame, useVideoConfig, interpolate, spring, AbsoluteFill } from "remotion";
import { RealityList } from "./components/RealityList";
import { CoinStack } from "./components/CoinStack";
import { CaptionLine, CaptionWordData } from "./components/CaptionLine";
import { Icon } from "./components/Icon";
import captionsData from "../data/captions.json";
import { palette, fonts } from "./lib/spring";
import "./lib/fonts";

const EXIT_HOLD_FRAMES = 6;
const CANVAS = { width: 1080, height: 1920 };
const VIDEO_CARD = { x: 40, y: 180, w: 1000, h: 640, radius: 28 };

// ---------- Captions layer ----------
const CaptionsLayer: React.FC = () => {
  const frame = useCurrentFrame();
  const lines = captionsData.lines as CaptionWordData[][];
  const activeLine = lines.find((line) => {
    const start = line[0].startFrame;
    const end = Math.max(...line.map((w) => w.endFrame)) + EXIT_HOLD_FRAMES + 8;
    return frame >= start - 2 && frame <= end;
  });
  if (!activeLine) return null;
  return (
    <CaptionLine
      words={activeLine}
      x={VIDEO_CARD.x + 40}
      y={VIDEO_CARD.y + VIDEO_CARD.h - 140}
      maxWidth={VIDEO_CARD.w - 80}
    />
  );
};

// ---------- Panel layer (frame chrome + dotted info panel + icon rows) ----------
const PanelLayer: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      {/* Logo mark (generic placeholder — swap in the real client logo/name) */}
      <div
        style={{
          position: "absolute",
          left: 540,
          top: 60,
          transform: "translateX(-50%)",
          width: 64,
          height: 64,
          borderRadius: 12,
          backgroundColor: palette.yellow,
        }}
      />

      {/* Video card border ring — hollow in the middle so CapCut's footage
          shows through; only the rounded white border itself is opaque. */}
      <div
        style={{
          position: "absolute",
          left: VIDEO_CARD.x,
          top: VIDEO_CARD.y,
          width: VIDEO_CARD.w,
          height: VIDEO_CARD.h,
          borderRadius: VIDEO_CARD.radius,
          border: `6px solid ${palette.caption}`,
          boxShadow: "0 8px 24px rgba(0,0,0,0.15)",
          boxSizing: "border-box",
        }}
      />

      {/* Info panel with dot grid */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 860,
          width: 1080,
          height: 1060,
          backgroundColor: palette.panelBg,
          backgroundImage: `radial-gradient(circle, ${palette.dotGrid} 2px, transparent 2px)`,
          backgroundSize: "48px 48px",
        }}
      />

      {captionsData.panels.map((panel, panelIdx) => {
        const nextPanel = captionsData.panels[panelIdx + 1];
        const fadeOutStart = nextPanel ? nextPanel.startFrame - 10 : Infinity;
        const panelOpacity = frame >= fadeOutStart
          ? interpolate(frame, [fadeOutStart, fadeOutStart + 10], [1, 0], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            })
          : 1;

        return (
          <div key={`panel-${panelIdx}`} style={{ opacity: panelOpacity }}>
            <RealityList
              title={panel.title}
              x={80}
              y={900}
              startFrame={panel.startFrame}
              rows={panel.rows.map((row) => ({
                icon: <Icon name={row.iconName} size={32} color={palette.ink} />,
                label: row.label,
                value: row.value,
              }))}
            />
          </div>
        );
      })}
    </>
  );
};

// ---------- Motifs layer (coin-stack / arrow) ----------
const MotifsLayer: React.FC = () => {
  return (
    <>
      {captionsData.motifs
        .filter((m) => m.type === "coin-stack")
        .map((motif, idx) => (
          <CoinStack
            key={`motif-${idx}`}
            startFrame={motif.startFrame}
            x={motif.x ?? 860}
            y={motif.y ?? 280}
            coinCount={motif.coinCount ?? 4}
          />
        ))}
    </>
  );
};

// ---------- CTA layer ----------
const CTALayer: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <>
      {captionsData.motifs
        .filter((m) => m.type === "cta-card")
        .map((motif, idx) => {
          const relativeFrame = frame - motif.startFrame;
          if (relativeFrame < 0) return null;

          const progress = spring({
            fps,
            frame: Math.min(relativeFrame, 14),
            config: { damping: 12, stiffness: 200, mass: 1 },
          });
          const yOff = interpolate(progress, [0, 1], [80, 0], { extrapolateRight: "clamp" });
          const opacity = Math.min(relativeFrame / 4, 1);

          return (
            <div
              key={`cta-${idx}`}
              style={{
                position: "absolute",
                left: (motif.x ?? 540) - 180,
                top: (motif.y ?? 1800) + yOff,
                width: 360,
                padding: 32,
                backgroundColor: palette.ink,
                borderRadius: 20,
                color: palette.caption,
                textAlign: "center",
                fontSize: 24,
                fontWeight: 800,
                fontFamily: fonts.cta,
                opacity,
                boxShadow: "0 8px 32px rgba(0,0,0,0.3)",
              }}
            >
              {motif.text}
            </div>
          );
        })}
    </>
  );
};

// ---------- QC-only stacked preview (bakes real footage in; never export this one) ----------
const PreviewStacked: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: palette.panelBg, fontFamily: fonts.sans }}>
    <div
      style={{
        position: "absolute",
        left: VIDEO_CARD.x,
        top: VIDEO_CARD.y,
        width: VIDEO_CARD.w,
        height: VIDEO_CARD.h,
        borderRadius: VIDEO_CARD.radius,
        overflow: "hidden",
        backgroundColor: "#000",
      }}
    >
      <Video src={staticFile("raw1_h264.mp4")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
    </div>
    <PanelLayer />
    <CaptionsLayer />
    <MotifsLayer />
    <CTALayer />
  </AbsoluteFill>
);

export const RemotionRoot: React.FC = () => {
  const common = {
    durationInFrames: captionsData.meta.durationFrames,
    fps: captionsData.meta.fps,
    width: CANVAS.width,
    height: CANVAS.height,
  };
  return (
    <>
      <Composition id="Captions" component={CaptionsLayer} {...common} />
      <Composition id="Panel" component={PanelLayer} {...common} />
      <Composition id="Motifs" component={MotifsLayer} {...common} />
      <Composition id="CTA" component={CTALayer} {...common} />
      <Composition id="Preview-Stacked" component={PreviewStacked} {...common} />
    </>
  );
};
