/**
 * CaptionLine.tsx — One on-screen caption line: a left-to-right flex row of
 * KineticWord, positioned once per line. Words pop in on their own real
 * timing (startFrame/endFrame from data/words.json) and the whole line
 * fades out shortly after its last word ends, just before the next line's
 * first word pops in.
 */
import React from "react";
import { useCurrentFrame } from "remotion";

export interface CaptionWordData {
  text: string;
  startFrame: number;
  endFrame: number;
  colorTag: "yellow" | "green" | "red" | "white" | "navy";
  fontFamily: string;
  fontSize: number;
  fontWeight: 400 | 600 | 700 | 800 | 900;
}

import { KineticWord } from "./KineticWord";

interface CaptionLineProps {
  words: CaptionWordData[];
  x: number;
  y: number;
  maxWidth?: number;
  exitHoldFrames?: number; // grace frames after last word before fading out
}

// Deterministic pseudo-random tilt per word, seeded by its text+start so it
// never changes across re-renders (Remotion re-renders every frame).
function seededRotation(seed: string): number {
  let h = 0;
  for (let i = 0; i < seed.length; i++) {
    h = (h * 31 + seed.charCodeAt(i)) | 0;
  }
  const normalized = ((h % 1000) / 1000) - 0.5; // -0.5..0.5
  return normalized * 8; // ±4°
}

export const CaptionLine: React.FC<CaptionLineProps> = ({
  words,
  x,
  y,
  maxWidth = 880,
  exitHoldFrames = 6,
}) => {
  const frame = useCurrentFrame();
  if (words.length === 0) return null;

  const lineStart = words[0].startFrame;
  const lineEnd = Math.max(...words.map((w) => w.endFrame));
  const lineExitFrame = lineEnd + exitHoldFrames;

  // Don't render at all outside this line's active window (perf + safety,
  // in case two lines' windows are computed to overlap slightly).
  if (frame < lineStart - 2 || frame > lineExitFrame + 8) return null;

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        maxWidth,
        display: "flex",
        flexWrap: "wrap",
        gap: "0 14px",
        alignItems: "baseline",
      }}
    >
      {words.map((w, i) => (
        <KineticWord
          key={`${w.text}-${w.startFrame}-${i}`}
          word={w.text}
          colorTag={w.colorTag}
          fontSize={w.fontSize}
          fontWeight={w.fontWeight}
          fontFamily={w.fontFamily}
          startFrame={w.startFrame}
          duration={Math.max(w.endFrame - w.startFrame, 6)}
          exitFrame={lineExitFrame}
          rotation={seededRotation(`${w.text}-${w.startFrame}`)}
        />
      ))}
    </div>
  );
};
