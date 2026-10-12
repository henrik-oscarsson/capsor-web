// Generates assets/logo.svg from the Cocktail Shaker font (dev-only; the font is never committed).
// Usage: node scripts/build-logo.mjs [path/to/CocktailShaker.otf]
import opentype from 'opentype.js';
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const FONT = process.argv[2] ??
	'/Users/henrik/Documents/Capsor/Code/Mjukvara/Fonts/Cocktail Shaker OT/CocktailShaker.otf';
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = join(ROOT, 'assets', 'logo.svg');

// Reference geometry measured from the original 200×89 px logo.
const REF = {
	square: { x: 0, y: 0, size: 84, stroke: 2.2 },
	text: { x1: 5, y1: 13, x2: 195, y2: 87 },
	canvas: { w: 196, h: 88 },
};
const ORANGE = 'rgb(230, 139, 20)';
const INK = '#111';

const font = opentype.loadSync(FONT);
const raw = font.getPath('Capsor', 0, 0, 100);
const bb = raw.getBoundingBox();

// Scale: font units → output units so the text width matches the reference width.
const k = (bb.x2 - bb.x1) / (REF.text.x2 - REF.text.x1);
const dx = REF.text.x1 * k - bb.x1;
const dy = REF.text.y1 * k - bb.y1;
const path = font.getPath('Capsor', dx, dy, 100);
const d = path.toPathData(2);

const textHeightRef = (REF.text.y2 - REF.text.y1) * k;
const textHeightActual = bb.y2 - bb.y1;
const drift = Math.abs(textHeightActual - textHeightRef) / textHeightRef;

const s = REF.square;
const half = (s.stroke * k) / 2;
const r = (n) => Math.round(n * 100) / 100;
const vbW = r(REF.canvas.w * k);
// Text bottom after translation is bb.y2 + dy; keep the reference canvas height unless the descender reaches further.
const vbH = r(Math.max(REF.canvas.h * k, bb.y2 + dy + 1));

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${vbW} ${vbH}" role="img" aria-labelledby="logo-title">
<title id="logo-title">Capsor AB</title>
<rect x="${r(s.x * k + half)}" y="${r(s.y * k + half)}" width="${r(s.size * k - 2 * half)}" height="${r(s.size * k - 2 * half)}" fill="none" stroke="${ORANGE}" stroke-width="${r(s.stroke * k)}"/>
<path d="${d}" fill="${INK}"/>
</svg>
`;

mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(OUT, svg);
console.log(`wrote ${OUT}  viewBox 0 0 ${vbW} ${vbH}  scale k=${r(k)}  text-height drift ${(drift * 100).toFixed(1)}%`);
