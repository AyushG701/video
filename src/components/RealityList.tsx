/**
 * RealityList.tsx — Icon tile rows with slide-up animation.
 *
 * Props:
 *   - rows: array of {icon, label, value?, color?}
 *   - startFrame: when first row enters
 *   - gapPx: space between rows (default 120)
 *   - iconSize: tile size (default 64)
 *   - rowDuration: slide animation length in frames (default 10)
 *
 * Animation: each row slides up (Y: 60 → 0) easeOutBack, staggered.
 */

import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

interface ListRow {
  icon: React.ReactNode; // SVG or img
  label: string;
  value?: string;
  color?: string; // override tile color
}

interface RealityListProps {
  title?: string;
  rows: ListRow[];
  startFrame?: number;
  gapPx?: number;
  iconSize?: number;
  rowDuration?: number;
  x?: number;
  y?: number;
  fontFamily?: string;
  fontSize?: number;
}

export const RealityList: React.FC<RealityListProps> = ({
  title,
  rows,
  startFrame = 0,
  gapPx = 120,
  iconSize = 64,
  rowDuration = 10,
  x = 80,
  y = 120,
  fontFamily = "Montserrat",
  fontSize = 46,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleRelativeFrame = frame - startFrame;
  const titleOpacity = titleRelativeFrame >= 0 ? Math.min(titleRelativeFrame / 6, 1) : 0;
  const titleY = titleRelativeFrame >= 0
    ? interpolate(titleRelativeFrame, [0, 10], [20, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
    : 20;

  return (
    <div style={{ position: "absolute", left: x, top: y }}>
      {title && (
        <h2
          style={{
            fontSize: 32,
            fontWeight: 800,
            fontFamily,
            color: "#1B2A4A",
            marginBottom: 40,
            opacity: titleOpacity,
            transform: `translateY(${titleY}px)`,
          }}
        >
          {title}
        </h2>
      )}

      {rows.map((row, idx) => {
        const rowStartFrame = startFrame + idx * 3; // 3-frame stagger
        const relativeFrame = frame - rowStartFrame;

        // Slide up: Y 60 → 0
        const yTranslate = relativeFrame >= 0
          ? interpolate(relativeFrame, [0, rowDuration], [60, 0], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            })
          : 60;

        const opacity = relativeFrame >= 0 ? Math.min(relativeFrame / 2, 1) : 0;

        return (
          <div
            key={idx}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 20,
              marginBottom: gapPx - 40,
              transform: `translateY(${yTranslate}px)`,
              opacity,
            }}
          >
            {/* Icon tile */}
            <div
              style={{
                width: iconSize,
                height: iconSize,
                borderRadius: 12,
                backgroundColor: row.color || "#F2C230",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexShrink: 0,
              }}
            >
              {row.icon}
            </div>

            {/* Text: label + value */}
            <div style={{ display: "flex", flexDirection: "column" }}>
              <div
                style={{
                  fontSize,
                  fontWeight: 700,
                  fontFamily,
                  color: "#1B2A4A",
                  whiteSpace: "nowrap",
                }}
              >
                {row.label}
              </div>
              {row.value && (
                <div
                  style={{
                    fontSize: fontSize * 0.8,
                    fontWeight: 600,
                    color: "#666",
                    marginTop: 4,
                  }}
                >
                  {row.value}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
