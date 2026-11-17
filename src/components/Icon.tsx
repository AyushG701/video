/**
 * Icon.tsx — Renders one of the downloaded Lucide SVGs (assets/icons/*.svg,
 * ISC license) recolored via a CSS mask, so a single monochrome line-icon
 * file can be tinted to any color (navy for list rows, white for motifs)
 * without needing separate colored SVG exports.
 */
import React from "react";
import { staticFile } from "remotion";

interface IconProps {
  name: string;
  size?: number;
  color?: string;
}

export const Icon: React.FC<IconProps> = ({ name, size = 32, color = "#1B2A4A" }) => {
  const url = staticFile(`assets/icons/${name}.svg`);
  return (
    <div
      style={{
        width: size,
        height: size,
        backgroundColor: color,
        WebkitMaskImage: `url(${url})`,
        maskImage: `url(${url})`,
        WebkitMaskRepeat: "no-repeat",
        maskRepeat: "no-repeat",
        WebkitMaskPosition: "center",
        maskPosition: "center",
        WebkitMaskSize: "contain",
        maskSize: "contain",
        flexShrink: 0,
      }}
    />
  );
};
