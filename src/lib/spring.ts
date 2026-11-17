/**
 * Spring physics config from design system.
 * Pass to Remotion's spring() animation.
 */
export const SPRING_CONFIG = {
  damping: 12,
  stiffness: 200,
  mass: 1,
};

/**
 * Color logic (meaning-matched to design system).
 */
export const colorTags = {
  yellow: "#F2C230",   // subject nouns (5% Scheme, Retained Savings, etc.)
  green: "#2E9E4F",    // money / percentages
  red: "#E23B2E",      // restrictions / negatives
  white: "#FFFFFF",    // neutral
  navy: "#1B2A4A",     // labels
};

/**
 * Map a caption tag to its color.
 */
export function getColorByTag(tag: "yellow" | "green" | "red" | "white" | "navy"): string {
  return colorTags[tag];
}

/**
 * Design system palette.
 */
export const palette = {
  ink: "#1B2A4A",
  caption: "#FFFFFF",
  captionShadow: "#00000066",
  yellow: "#F2C230",
  red: "#E23B2E",
  green: "#2E9E4F",
  panelBg: "#F7F6F2",
  dotGrid: "#D9D6CF",
};

/**
 * Font families (load via @remotion/google-fonts).
 */
export const fonts = {
  nepali: "Noto Sans Devanagari",
  sans: "Montserrat",
  chunky: "Archivo Black",
  mono: "JetBrains Mono",
  cta: "Nunito",
};
