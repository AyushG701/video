/**
 * KineticWord.tsx — Single word with spring pop + color logic.
 *
 * Renders as an inline flex child (no absolute positioning of its own) so a
 * parent flex row can lay multiple words out left-to-right as a real caption
 * line. Animates in via spring pop, and fades out after `exitFrame` so lines
 * don't persist forever once popped in.
 */

import React from "react";
import { spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { SPRING_CONFIG, getColorByTag, palette } from "../lib/spring";

interface KineticWordProps {
  word: string;
  colorTag: "yellow" | "green" | "red" | "white" | "navy";
  fontSize?: number;
  fontWeight?: 400 | 600 | 700 | 800 | 900;
  fontFamily?: string;
  startFrame?: number;
  duration?: number;
  exitFrame?: number; // frame at which this word starts fading out
  exitDuration?: number;
  rotation: number; // fixed tilt, derived by the caller from a stable seed (e.g. word index)
}

export const KineticWord: React.FC<KineticWordProps> = ({
  word,
  colorTag,
  fontSize = 46,
  fontWeight = 700,
  fontFamily = "Montserrat",
  startFrame = 0,
  duration = 12,
  exitFrame,
  exitDuration = 4,
  rotation,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relativeFrame = frame - startFrame;

  const scale = relativeFrame >= 0
    ? spring({
        fps,
        frame: relativeFrame,
        config: SPRING_CONFIG,
        durationInFrames: duration,
      })
    : 0;

  const yOffset = relativeFrame >= 0
    ? interpolate(relativeFrame, [0, duration], [40, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : 40;

  const enterOpacity = relativeFrame >= 0 ? Math.min(relativeFrame / 3, 1) : 0;

  const exitOpacity = exitFrame !== undefined && frame > exitFrame
    ? interpolate(frame, [exitFrame, exitFrame + exitDuration], [1, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : 1;

  const opacity = Math.min(enterOpacity, exitOpacity);
  const color = getColorByTag(colorTag);

  if (opacity <= 0) return null;

  return (
    <span
      style={{
        display: "inline-block",
        transform: `scale(${scale}) translateY(-${yOffset}px) rotate(${rotation}deg)`,
        opacity,
        fontSize,
        fontWeight,
        fontFamily,
        color,
        textShadow: `0 2px 8px ${palette.captionShadow}`,
        whiteSpace: "nowrap",
        WebkitFontSmoothing: "antialiased",
      }}
    >
      {word}
    </span>
  );
};
