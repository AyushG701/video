/**
 * CoinStack.tsx — The "retained savings vs. restriction" motif: a stack of
 * money tiles topped with a house, swept by a red down-arrow.
 *
 * Built entirely from the real downloaded Lucide SVGs (assets/icons/) via
 * the Icon component — no 3D emoji renders, since none were ever sourced
 * for this project (CLAUDE.md requires search_assets() for those, and that
 * tool isn't available in this environment).
 */

import React from "react";
import { spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { SPRING_CONFIG, palette } from "../lib/spring";
import { Icon } from "./Icon";

interface CoinStackProps {
  startFrame?: number;
  coinCount?: number;
  x?: number;
  y?: number;
  coinSize?: number;
  arrowLength?: number;
}

export const CoinStack: React.FC<CoinStackProps> = ({
  startFrame = 0,
  coinCount = 4,
  x = 540,
  y = 600,
  coinSize = 84,
  arrowLength = 220,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: "translate(-50%, -50%)",
      }}
    >
      {Array.from({ length: coinCount }).map((_, idx) => {
        const coinStartFrame = startFrame + idx * 2;
        const relativeFrame = frame - coinStartFrame;
        if (relativeFrame < 0) return null;

        const progress = spring({
          fps,
          frame: relativeFrame,
          config: SPRING_CONFIG,
          durationInFrames: 12,
        });
        const offset = coinSize * idx * 0.42;

        return (
          <div
            key={`coin-${idx}`}
            style={{
              position: "absolute",
              width: coinSize,
              height: coinSize,
              left: -coinSize / 2,
              top: -coinSize / 2 - offset,
              transform: `translateY(${(1 - progress) * 60}px)`,
              opacity: progress,
              backgroundColor: palette.yellow,
              borderRadius: 12,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 4px 12px rgba(0,0,0,0.25)",
            }}
          >
            <Icon name="banknote" size={coinSize * 0.55} color={palette.ink} />
          </div>
        );
      })}

      {(() => {
        const houseStartFrame = startFrame + coinCount * 2;
        const relativeFrame = frame - houseStartFrame;
        if (relativeFrame < 0) return null;

        const progress = spring({
          fps,
          frame: relativeFrame,
          config: SPRING_CONFIG,
          durationInFrames: 12,
        });
        const topOffset = coinSize * coinCount * 0.42 + coinSize * 0.3;

        return (
          <div
            style={{
              position: "absolute",
              width: coinSize * 1.1,
              height: coinSize * 1.1,
              left: -coinSize * 0.55,
              top: -coinSize / 2 - topOffset,
              transform: `translateY(${(1 - progress) * 40}px)`,
              opacity: progress,
              backgroundColor: palette.ink,
              borderRadius: 12,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 4px 12px rgba(0,0,0,0.25)",
            }}
          >
            <Icon name="house" size={coinSize * 0.6} color={palette.caption} />
          </div>
        );
      })()}

      {(() => {
        const arrowStartFrame = startFrame + coinCount * 2 + 4;
        const relativeFrame = frame - arrowStartFrame;

        const arrowOffset = relativeFrame >= 0
          ? interpolate(relativeFrame, [0, 14], [-arrowLength / 2, arrowLength / 2], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            })
          : -arrowLength / 2;

        if (relativeFrame < -4) return null;

        return (
          <div
            style={{
              position: "absolute",
              left: arrowOffset - 20,
              top: coinSize * 0.6,
              opacity: relativeFrame >= -4 ? 1 : 0,
            }}
          >
            <Icon name="arrow-down" size={48} color={palette.red} />
          </div>
        );
      })()}
    </div>
  );
};
