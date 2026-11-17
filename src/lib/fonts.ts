/**
 * Loads the real Google Fonts this design uses, via @remotion/google-fonts
 * (so Chromium actually has them available at render time instead of
 * silently falling back to a default serif).
 */
import { loadFont as loadMontserrat } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadNotoDevanagari } from "@remotion/google-fonts/NotoSansDevanagari";
import { loadFont as loadNunito } from "@remotion/google-fonts/Nunito";
import { loadFont as loadArchivoBlack } from "@remotion/google-fonts/ArchivoBlack";

const { fontFamily: montserratFamily } = loadMontserrat("normal", {
  weights: ["700", "800"],
  subsets: ["latin"],
});
const { fontFamily: notoDevanagariFamily } = loadNotoDevanagari("normal", {
  weights: ["700"],
  subsets: ["devanagari"],
});
const { fontFamily: nunitoFamily } = loadNunito("normal", {
  weights: ["800"],
  subsets: ["latin"],
});
const { fontFamily: archivoBlackFamily } = loadArchivoBlack("normal", {
  weights: ["400"],
  subsets: ["latin"],
});

export const loadedFonts = {
  sans: montserratFamily,
  nepali: notoDevanagariFamily,
  cta: nunitoFamily,
  chunky: archivoBlackFamily,
};
