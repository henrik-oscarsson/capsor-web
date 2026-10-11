# Site Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild capsor.se in "Direction B · Bold split" with an orange hero, a full-height portrait, alternating white and black sections and a recreated SVG logo, and restyle the CV PDF to match.

**Architecture:** Plain static site served by GitHub Pages from `master`. `index.html` holds the markup, `styles.css` holds all styling and `assets/` holds the logo SVG and hero portrait. The logo is generated once by a dev-only Node script (`scripts/build-logo.mjs`, using `opentype.js`) from Henrik's local Cocktail Shaker font; only the SVG output is committed. Verification uses a repo shell script (`scripts/check-site.sh`), a contrast script (`scripts/contrast.py`) and headless-Chrome screenshots.

**Tech Stack:** HTML, CSS, Node 22 with `opentype.js@1.3.4` (dev only), Python 3 with Pillow (installed), macOS `sips`, Google Chrome headless, `md-to-pdf@5` for the CV.

**Spec:** `docs/superpowers/specs/2026-10-11-site-redesign-design.md`

## Global Constraints

- Branch `redesign`. End every commit message with the line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. If you are a different model, use your own model name in that line.
- Colours: only `--orange: rgb(230, 139, 20)`, `--black: #111`, `--white: #fff`, `--warm: #f5f2ed`, `--muted: #555`, `--muted-dark: #bbb`, `--rule-dark: #444`, `--rule-warm: #d8d2c8`, plus `#eee` (header border) and `#999` (footer text). Never `#4a90c4` or `#9DFF20`.
- Never orange text on white and never white text on orange (both 2.60:1). Hero accent "days, not weeks." is black text with a white highlighter stroke. "Faster teams." is black text on an orange block.
- Fonts: DM Sans (400, 500, 700) and IBM Plex Mono (400, 500) from Google Fonts.
- Content max width 1100px, side padding `clamp(1.25rem, 4vw, 3rem)`. One breakpoint: phone layout at `max-width: 719px`.
- No JavaScript beyond the existing one-line menu toggle. No animations or transitions.
- The font file `CocktailShaker.otf` must never be committed or copied into the repo. Its path is `/Users/henrik/Documents/Capsor/Code/Mjukvara/Fonts/Cocktail Shaker OT/CocktailShaker.otf`.
- `henrik.jpg` at the repo root stays unchanged (the CV uses `/henrik.jpg`).
- Chrome binary: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.
- Scratch directory for screenshots and temporary files: `/private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/scratchpad` (call it `$S`).

## File Map

| Path | Task | Responsibility |
|---|---|---|
| `.gitignore` | 1 | Ignore `.superpowers/` and `node_modules/` |
| `package.json`, `package-lock.json` | 1 | Dev dependency `opentype.js` |
| `scripts/build-logo.mjs` | 1 | Generates `assets/logo.svg` from the font |
| `assets/logo.svg` | 1 | Logo |
| `assets/henrik.jpg` | 2 | Hero portrait (1000px long edge, greyscale) |
| `styles.css` | 2 | All site CSS |
| `index.html` | 2 | Rewritten markup |
| `scripts/check-site.sh` | 2 | Copy and link checks |
| `scripts/contrast.py` | 2 | WCAG contrast check for the palette pairs |
| `iStock-1291279253.jpg`, `CapsorWebSiteLogo.jpg` | 2 | Deleted |
| `cv/cv.css`, `CV_Henrik_Oscarsson_en.pdf` | 3 | Blue swapped for black; PDF regenerated |

---

### Task 1: Recreated SVG logo

**Files:**
- Create: `.gitignore`, `package.json` (via npm), `package-lock.json`, `scripts/build-logo.mjs`, `assets/logo.svg`

**Interfaces:**
- Produces: `assets/logo.svg`. It has a tight `viewBox`, no fixed `width`/`height` attributes, `role="img"` and `<title>Capsor AB</title>`. Task 2 shows it with `<img src="assets/logo.svg" alt="Capsor AB">` at CSS height 40px (32px on phones).

**Reference measurements** (taken from the current `CapsorWebSiteLogo.jpg`, 200×89 px):
- Orange square outline: outer box x 0–83, y 0–83 (84 px square), stroke about 2.2 px.
- Black text bounding box: x 5–195, y 13–87.
- The script scales these numbers so that the font's real text width maps onto the 190 px reference width.

- [ ] **Step 1: Write `.gitignore` and install the dependency**

`.gitignore`:
```
.superpowers/
node_modules/
```

Then run:
```bash
cd /Users/henrik/Code/Capsor-web/capsor-web
npm init -y >/dev/null
npm install --save-dev opentype.js@1.3.4
```
Expected: `package.json` lists `"opentype.js": "^1.3.4"` under `devDependencies`, and `node_modules/` exists but is git-ignored (`git status --short` must not show `node_modules`).

- [ ] **Step 2: Write `scripts/build-logo.mjs`**

```js
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
```

- [ ] **Step 3: Generate the logo**

Run: `node scripts/build-logo.mjs`
Expected: the output line starts `wrote …/assets/logo.svg`. The reported text-height drift should be under 8%; a larger drift means the regular glyphs don't match the original, so stop and report it.

- [ ] **Step 4: Compare against the original visually**

Render both at the same height:
```bash
S=/private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/scratchpad
cd /Users/henrik/Code/Capsor-web/capsor-web
cat > $S/logo-compare.html <<EOF
<html><body style="margin:0;padding:20px;background:#fff">
<img src="file://$PWD/CapsorWebSiteLogo.jpg" style="height:178px;display:block;margin-bottom:20px">
<img src="file://$PWD/assets/logo.svg" style="height:178px;display:block;margin-bottom:20px">
<div style="background:#111;padding:10px;display:inline-block"><img src="file://$PWD/assets/logo.svg" style="height:60px;display:block;background:transparent"></div>
</body></html>
EOF
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files --window-size=520,520 --screenshot="$S/logo-compare.png" "file://$S/logo-compare.html"
```
Open `$S/logo-compare.png` with the Read tool. Expected:
- The SVG (second image) matches the original (first image): same lettering, the orange square behind "Ca", the "p" descender below the square, and similar proportions.
- The SVG is crisp.
- On the black strip the background is transparent (the square and text sit directly on black; the black text is barely visible, which is expected).

If the square's position relative to the text is visibly off, adjust only the `REF` numbers, re-run Steps 3–4, and record the final values in your report.

- [ ] **Step 5: Validate the SVG**

Run:
```bash
python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse('assets/logo.svg'); print('valid xml')"
grep -c "<title" assets/logo.svg
git status --short
```
Expected: `valid xml`; `1`; no `.otf` file and no `node_modules` in the status output.

- [ ] **Step 6: Commit**

```bash
git add .gitignore package.json package-lock.json scripts/build-logo.mjs assets/logo.svg
git commit -m "Recreate logo as SVG from Cocktail Shaker

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Rebuild the page (Direction B)

**Files:**
- Create: `assets/henrik.jpg`, `styles.css`, `scripts/check-site.sh`, `scripts/contrast.py`
- Modify: `index.html` (full rewrite)
- Delete: `iStock-1291279253.jpg`, `CapsorWebSiteLogo.jpg`

**Interfaces:**
- Consumes: `assets/logo.svg` (Task 1).
- Produces: the final site. `scripts/check-site.sh` stays in the repo for future edits.

- [ ] **Step 1: Generate the hero portrait**

```bash
cd /Users/henrik/Code/Capsor-web/capsor-web
SRC=/private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/images/1.jpg
test -f "$SRC" || { echo "SOURCE PHOTO MISSING — stop and ask Henrik for it"; exit 1; }
python3 - <<'EOF'
from PIL import Image, ImageOps
src = '/private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/images/1.jpg'
im = ImageOps.exif_transpose(Image.open(src)).convert('L')
im.thumbnail((1000, 1000))
im.save('assets/henrik.jpg', 'JPEG', quality=82, optimize=True, progressive=True)
print(im.size)
EOF
ls -la assets/henrik.jpg
```
Expected: about `(890, 1000)`, file size under 200 KB.

- [ ] **Step 2: Write the check script (failing first)**

Create `scripts/check-site.sh`:
```bash
#!/bin/bash
# Verifies index.html/styles.css copy, palette rules and local links. Run from the repo root.
cd "$(dirname "$0")/.." || exit 1
fail=0
need()   { grep -qF -- "$2" "$1" && echo "OK        $2" || { echo "MISSING   $2 ($1)"; fail=1; }; }
forbid() { grep -qiF -- "$2" "$1" && { echo "FORBIDDEN $2 ($1)"; fail=1; } || echo "OK (none) $2 ($1)"; }
H=index.html; C=styles.css
[ -f "$C" ] || { echo "MISSING styles.css"; exit 1; }
need $H '<link rel="stylesheet" href="styles.css">'
need $H 'src="assets/logo.svg"'
need $H 'src="assets/henrik.jpg"'
need $H 'Engineering teams that ship in <span class="hl-white">days, not weeks.</span>'
need $H 'Fewer rituals.<br>More flow.<br><span class="block">Faster teams.</span>'
need $H '3 → 1'; need $H '1–2 days'; need $H '&lt; 6 months'
need $H 'One standup, one topic.'; need $H 'Under half a day? Just do it.'
need $H 'Work in twos and threes.'; need $H 'Agentic by default.'
need $H 'id="how"'; need $H 'id="work"'; need $H 'href="#how"'; need $H 'href="#work"'
need $H 'Four deliberate choices that remove friction and give people ownership.'
need $H '25 years building the systems myself.'
need $H 'CTO at CIKO, building Trygga.'
need $H 'Nokia and Microsoft'
for f in $H $C; do
  forbid $f 'iStock'; forbid $f 'CapsorWebSiteLogo'; forbid $f '#4a90c4'; forbid $f '#9DFF20'; forbid $f 'transition'; forbid $f 'animation'
done
forbid $H '<style'
for p in $(grep -oE '(href|src)="[^"#:]+"' $H | sed -E 's/^(href|src)="//; s/"$//'); do
  [ -e "$p" ] && echo "OK file   $p" || { echo "MISSING FILE $p"; fail=1; }
done
exit $fail
```
Run: `chmod +x scripts/check-site.sh && scripts/check-site.sh; echo "exit $?"`
Expected: `exit 1`, with MISSING lines (e.g. `styles.css`) — the RED state.

- [ ] **Step 3: Write `styles.css`**

```css
*,
*::before,
*::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --orange: rgb(230, 139, 20);
    --black: #111;
    --white: #fff;
    --warm: #f5f2ed;
    --muted: #555;
    --muted-dark: #bbb;
    --rule-dark: #444;
    --rule-warm: #d8d2c8;
    --font-sans: 'DM Sans', system-ui, -apple-system, sans-serif;
    --font-mono: 'IBM Plex Mono', monospace;
    --max-width: 1100px;
    --pad: clamp(1.25rem, 4vw, 3rem);
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: var(--font-sans);
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--black);
    background: var(--white);
}

img {
    display: block;
    max-width: 100%;
}

a {
    color: inherit;
}

:focus-visible {
    outline: 2px solid var(--black);
    outline-offset: 3px;
}

.band-dark :focus-visible,
.site-footer :focus-visible {
    outline-color: var(--orange);
}

.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* Layout */
.wrap {
    max-width: var(--max-width);
    margin: 0 auto;
    padding-left: var(--pad);
    padding-right: var(--pad);
}

.section {
    padding-top: 5rem;
    padding-bottom: 5rem;
}

.label {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
}

h2 {
    font-size: clamp(1.6rem, 3vw, 2.1rem);
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.02em;
    margin-bottom: 1.25rem;
}

/* Buttons */
.btn {
    display: inline-block;
    border-radius: 999px;
    font-weight: 700;
    font-size: 1rem;
    line-height: 1.2;
    text-decoration: none;
    padding: 0.8rem 1.6rem;
}

.btn-dark {
    background: var(--black);
    color: var(--white);
    border: 2px solid var(--black);
}

.btn-dark:hover {
    background: #333;
    border-color: #333;
}

.btn-outline {
    color: var(--black);
    border: 2px solid var(--black);
}

.btn-outline:hover {
    background: var(--black);
    color: var(--white);
}

/* Header */
.site-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--white);
    border-bottom: 1px solid #eee;
}

.site-header nav {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 0.9rem;
    padding-bottom: 0.9rem;
}

.logo img {
    height: 40px;
    width: auto;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 2rem;
    list-style: none;
}

.nav-links a {
    font-size: 0.95rem;
    font-weight: 500;
    text-decoration: none;
}

.nav-links a:not(.btn):hover {
    text-decoration: underline;
    text-decoration-color: var(--orange);
    text-decoration-thickness: 2px;
    text-underline-offset: 5px;
}

.nav-links .btn {
    padding: 0.5rem 1.25rem;
    font-size: 0.9rem;
}

.mobile-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
}

.mobile-toggle span {
    display: block;
    width: 24px;
    height: 2px;
    margin: 5px 0;
    background: var(--black);
}

/* Hero */
.hero {
    display: grid;
    grid-template-columns: 1.45fr 1fr;
    min-height: 560px;
}

.hero-text {
    background: var(--orange);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-top: 4.5rem;
    padding-bottom: 4.5rem;
    padding-right: var(--pad);
    /* Align the text with the content column of the sections below. */
    padding-left: max(var(--pad), calc((100vw - var(--max-width)) / 2 + var(--pad)));
}

.hero .label {
    color: var(--black);
}

.hero h1 {
    font-size: clamp(2.25rem, 5.5vw, 4rem);
    font-weight: 700;
    line-height: 1.05;
    letter-spacing: -0.035em;
    margin-bottom: 1.25rem;
}

.hl-white {
    box-shadow: inset 0 -0.32em 0 var(--white);
    box-decoration-break: clone;
    -webkit-box-decoration-break: clone;
}

.hero-lede {
    font-size: 1.15rem;
    max-width: 34rem;
    margin-bottom: 2rem;
}

.hero-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
}

.hero-photo {
    position: relative;
    overflow: hidden;
    background: var(--black);
}

.hero-photo img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: 50% 25%;
}

/* Results */
.results {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2.5rem;
    list-style: none;
}

.results li {
    border-top: 3px solid var(--black);
    padding-top: 1rem;
}

.result-value {
    display: block;
    font-family: var(--font-mono);
    font-size: clamp(2.2rem, 4.5vw, 3rem);
    font-weight: 500;
    line-height: 1.1;
}

.result-label {
    display: block;
    margin-top: 0.6rem;
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--muted);
}

/* How I work */
.band-dark {
    background: var(--black);
    color: var(--white);
}

.band-dark .label {
    color: var(--orange);
}

.band-dark h2 {
    max-width: 40rem;
}

.principles {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem 3rem;
    list-style: none;
    margin-top: 2.5rem;
}

.principles li {
    border-top: 1px solid var(--rule-dark);
    padding-top: 1.25rem;
}

.principle-num {
    font-family: var(--font-mono);
    font-size: 0.9rem;
    color: var(--orange);
}

.principles h3 {
    font-size: 1.25rem;
    line-height: 1.3;
    margin: 0.35rem 0 0.5rem;
}

.principles p {
    color: var(--muted-dark);
}

/* Statement */
.statement {
    font-size: clamp(2.5rem, 7vw, 5rem);
    font-weight: 700;
    line-height: 1.02;
    letter-spacing: -0.04em;
    text-transform: uppercase;
}

.statement .block {
    background: var(--orange);
    padding: 0 0.1em;
    box-decoration-break: clone;
    -webkit-box-decoration-break: clone;
}

/* Track record */
.band-warm {
    background: var(--warm);
}

.track {
    display: grid;
    grid-template-columns: 1fr 1.1fr;
    gap: 3.5rem;
}

.track p {
    color: var(--muted);
}

.links {
    margin-top: 1.5rem;
}

.links a {
    font-weight: 700;
    color: var(--black);
    text-decoration: underline;
    text-decoration-color: var(--orange);
    text-decoration-thickness: 3px;
    text-underline-offset: 5px;
}

.domains {
    list-style: none;
}

.domains li {
    border-top: 1px solid var(--rule-warm);
    padding: 0.85rem 0;
    line-height: 1.5;
}

.domains li:last-child {
    border-bottom: 1px solid var(--rule-warm);
}

.domains strong {
    display: block;
}

.domains span {
    color: var(--muted);
}

/* Work with me */
.work-intro {
    color: var(--muted);
    max-width: 40rem;
}

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    list-style: none;
    margin-top: 2rem;
}

.cards li {
    border: 2px solid var(--black);
    border-radius: 10px;
    padding: 1.5rem;
}

.cards h3 {
    font-size: 1.2rem;
    margin-bottom: 0.4rem;
}

.cards p {
    color: var(--muted);
    font-size: 0.98rem;
    line-height: 1.6;
}

/* CTA */
.band-orange {
    background: var(--orange);
}

.cta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
}

.cta h2 {
    font-size: clamp(2rem, 4vw, 2.75rem);
    margin-bottom: 0.5rem;
}

.cta p {
    max-width: 36rem;
}

.cta .btn {
    white-space: nowrap;
}

/* Footer */
.site-footer {
    background: var(--black);
    color: #999;
    font-size: 0.9rem;
}

.site-footer .wrap {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    padding-top: 1.75rem;
    padding-bottom: 1.75rem;
}

.site-footer a {
    color: #999;
}

/* Phone */
@media (max-width: 719px) {
    .mobile-toggle {
        display: block;
    }

    .nav-links {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
        padding: 1.25rem var(--pad);
        background: var(--white);
        border-bottom: 1px solid #eee;
    }

    .nav-links.open {
        display: flex;
    }

    .logo img {
        height: 32px;
    }

    .hero {
        grid-template-columns: 1fr;
        min-height: 0;
    }

    .hero-text {
        padding: 2.75rem var(--pad);
    }

    .hero-photo {
        height: 300px;
    }

    .hero-photo img {
        object-position: 50% 30%;
    }

    .section {
        padding-top: 3.5rem;
        padding-bottom: 3.5rem;
    }

    .results,
    .principles,
    .track,
    .cards {
        grid-template-columns: 1fr;
    }

    .results {
        gap: 1.75rem;
    }

    .track {
        gap: 2rem;
    }

    .cta {
        flex-direction: column;
        align-items: flex-start;
    }

    .site-footer .wrap {
        flex-direction: column;
        align-items: center;
        gap: 0.4rem;
        text-align: center;
    }
}
```

- [ ] **Step 4: Rewrite `index.html`**

Replace the entire file with:

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Henrik Oscarsson — CTO · Capsor AB</title>
    <meta name="description"
        content="Henrik Oscarsson is a CTO who makes engineering teams faster by changing how they work, not by adding process. 25 years in trading and payments.">
    <link rel="icon" href="favicon.ico" type="image/png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap"
        rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>

<body>
    <!-- Header -->
    <header class="site-header">
        <nav class="wrap">
            <a href="#" class="logo"><img src="assets/logo.svg" alt="Capsor AB" width="96" height="43"></a>
            <button type="button" class="mobile-toggle" aria-label="Toggle menu"
                onclick="document.querySelector('.nav-links').classList.toggle('open')">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-links">
                <li><a href="#how">How I work</a></li>
                <li><a href="#work">Work with me</a></li>
                <li><a href="CV_Henrik_Oscarsson_en.pdf" target="_blank" rel="noopener">CV</a></li>
                <li><a href="mailto:henrik@capsor.se" class="btn btn-dark">Get in touch</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <!-- Hero -->
        <section class="hero">
            <div class="hero-text">
                <p class="label">Henrik Oscarsson · CTO</p>
                <h1>Engineering teams that ship in <span class="hl-white">days, not weeks.</span></h1>
                <p class="hero-lede">I make engineering teams faster by changing how they work, not by adding
                    process. CTO at CIKO, building Trygga.</p>
                <div class="hero-actions">
                    <a href="mailto:henrik@capsor.se" class="btn btn-dark">Get in touch</a>
                    <a href="CV_Henrik_Oscarsson_en.pdf" class="btn btn-outline" target="_blank" rel="noopener">Read
                        my CV</a>
                </div>
            </div>
            <div class="hero-photo">
                <img src="assets/henrik.jpg" alt="Henrik Oscarsson" width="890" height="1000">
            </div>
        </section>

        <!-- Results -->
        <section class="section">
            <div class="wrap">
                <p class="label">At CIKO, since April 2026</p>
                <ul class="results">
                    <li>
                        <span class="result-value"><span aria-hidden="true">3 → 1</span><span
                                class="visually-hidden">Three teams to one</span></span>
                        <span class="result-label">Three teams, 15 engineers in total, now working as one team with
                            tight, everyday communication.</span>
                    </li>
                    <li>
                        <span class="result-value">1–2 days</span>
                        <span class="result-label">Typical time to ship a feature, down from 1–2 weeks.</span>
                    </li>
                    <li>
                        <span class="result-value">&lt; 6 months</span>
                        <span class="result-label">From joining to a new way of working, in place and
                            delivering.</span>
                    </li>
                </ul>
            </div>
        </section>

        <!-- How I work -->
        <section class="section band-dark" id="how">
            <div class="wrap">
                <p class="label">How I work</p>
                <h2>Four deliberate choices that remove friction and give people ownership.</h2>
                <ol class="principles">
                    <li>
                        <span class="principle-num">01</span>
                        <h3>One standup, one topic.</h3>
                        <p>Instead of a ticket-by-ticket status round, each day's standup is about the single most
                            important thing for the team right now. Meetings stay short, and everyone leaves knowing
                            what matters today.</p>
                    </li>
                    <li>
                        <span class="principle-num">02</span>
                        <h3>Under half a day? Just do it.</h3>
                        <p>Small fixes, tech debt and improvements don't need a ticket, a refinement session or
                            permission. That creates flow and ownership, and the platform keeps getting better on its
                            own.</p>
                    </li>
                    <li>
                        <span class="principle-num">03</span>
                        <h3>Work in twos and threes.</h3>
                        <p>When a task needs it, people group up in pairs or threes. Knowledge spreads naturally, and
                            the team builds a shared view of how we build things, without relying on
                            documentation.</p>
                    </li>
                    <li>
                        <span class="principle-num">04</span>
                        <h3>Agentic by default.</h3>
                        <p>I introduce AI by example: start with concrete, repetitive tasks like "build a UI component
                            to our standards, with tests", then move to agentic frameworks that handle the
                            orchestration.</p>
                    </li>
                </ol>
            </div>
        </section>

        <!-- Statement -->
        <section class="section">
            <div class="wrap">
                <p class="statement">Fewer rituals.<br>More flow.<br><span class="block">Faster teams.</span></p>
            </div>
        </section>

        <!-- Track record -->
        <section class="section band-warm">
            <div class="wrap track">
                <div>
                    <p class="label">Track record</p>
                    <h2>25 years building the systems myself.</h2>
                    <p>Often where latency, reliability and scale aren't negotiable. Before CIKO, I was CTO at Valuno
                        Group, and I've spent many years working in high-transaction environments, most of them
                        trading systems.</p>
                    <p class="links"><a href="CV_Henrik_Oscarsson_en.pdf" target="_blank" rel="noopener">Read my CV
                            (PDF)</a> &nbsp;·&nbsp; <a href="CV_Henrik_Oscarsson_full_en.pdf" target="_blank"
                            rel="noopener">Full project history (PDF)</a></p>
                </div>
                <ul class="domains">
                    <li><strong>Trading and exchanges</strong> <span>AMEX in New York, Credit Suisse in London, NASDAQ
                            OMX, SIX Telekurs, SFE in Australia.</span></li>
                    <li><strong>High-performance systems</strong> <span>Real-time trading terminals, threading models,
                            latency-critical clients.</span></li>
                    <li><strong>Product platforms</strong> <span>Barnebys (marketplaces), FRISQ (healthtech), iFACTS
                            (insurance), Trust Anchor Group (digital identity).</span></li>
                    <li><strong>Large-scale delivery</strong> <span>Tech lead for 16 developers in a 40-person
                            e-commerce programme in London.</span></li>
                    <li><strong>Also contracted by</strong> <span>Nokia and Microsoft.</span></li>
                </ul>
            </div>
        </section>

        <!-- Work with me -->
        <section class="section" id="work">
            <div class="wrap">
                <p class="label">Work with me</p>
                <p class="work-intro">I'm currently CTO at CIKO, and always happy to talk about what's next. Through
                    Capsor, I work in three ways:</p>
                <ul class="cards">
                    <li>
                        <h3>Permanent CTO</h3>
                        <p>Building an engineering organisation, or turning one around.</p>
                    </li>
                    <li>
                        <h3>Interim CTO</h3>
                        <p>Covering a critical phase or a leadership gap, with a clear handover.</p>
                    </li>
                    <li>
                        <h3>Advisory</h3>
                        <p>Helping an existing team adopt leaner ways of working and AI-driven development.</p>
                    </li>
                </ul>
            </div>
        </section>

        <!-- CTA -->
        <section class="section band-orange">
            <div class="wrap cta">
                <div>
                    <h2>Let's talk.</h2>
                    <p>Whether you're hiring a CTO, need a steady hand through a critical phase, or want your team
                        shipping in days instead of weeks, I'd be glad to hear what you're working on.</p>
                </div>
                <a href="mailto:henrik@capsor.se" class="btn btn-dark">Get in touch</a>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="wrap">
            <span>&copy; 2008–2026 Capsor AB</span>
            <a href="mailto:henrik@capsor.se">henrik@capsor.se</a>
        </div>
    </footer>
</body>

</html>
```

After writing it, set the logo `<img>` `width`/`height` attributes to the SVG's actual aspect ratio at 43px tall. Read the `viewBox` from `assets/logo.svg` and compute width = round(43 × vbW / vbH). Do the same check for the hero photo: its `width`/`height` attributes must equal the real pixel size printed in Step 1.

- [ ] **Step 5: Delete the old assets**

```bash
git rm -q iStock-1291279253.jpg CapsorWebSiteLogo.jpg
```

- [ ] **Step 6: Run the check script (GREEN)**

Run: `scripts/check-site.sh; echo "exit $?"`
Expected: `exit 0`, and every line starts with `OK`.

- [ ] **Step 7: Contrast check**

Create `scripts/contrast.py`:
```python
"""WCAG 2 contrast ratios for every text/background pair used on capsor.se."""

def luminance(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

ORANGE, BLACK, WHITE, WARM = (230, 139, 20), (17, 17, 17), (255, 255, 255), (245, 242, 237)
MUTED, MUTED_DARK, FOOTER = (85, 85, 85), (187, 187, 187), (153, 153, 153)

# (description, foreground, background, minimum ratio)
PAIRS = [
    ("body text on white", BLACK, WHITE, 4.5),
    ("muted text on white", MUTED, WHITE, 4.5),
    ("text on orange (hero, CTA)", BLACK, ORANGE, 4.5),
    ("hero accent: black on white highlight", BLACK, WHITE, 4.5),
    ("statement block: black on orange", BLACK, ORANGE, 3.0),
    ("white text on black band", WHITE, BLACK, 4.5),
    ("muted-dark text on black band", MUTED_DARK, BLACK, 4.5),
    ("orange label/numbers on black", ORANGE, BLACK, 4.5),
    ("text on warm", BLACK, WARM, 4.5),
    ("muted text on warm", MUTED, WARM, 4.5),
    ("footer text on black", FOOTER, BLACK, 4.5),
    ("button text: white on black", WHITE, BLACK, 4.5),
]

failed = False
for name, fg, bg, minimum in PAIRS:
    r = ratio(fg, bg)
    ok = r >= minimum
    failed |= not ok
    print(f"{'PASS' if ok else 'FAIL'}  {r:5.2f}:1  (min {minimum})  {name}")
raise SystemExit(1 if failed else 0)
```
Run: `python3 scripts/contrast.py; echo "exit $?"`
Expected: every line `PASS`, `exit 0`. Also confirm with `grep -n "color: var(--orange)\|color: var(--white)" styles.css` that orange text only appears inside `.band-dark` rules (`.band-dark .label`, `.principle-num`) and white text only in `.band-dark` and `.btn-dark`/`.btn-outline:hover`.

- [ ] **Step 8: Screenshots and visual inspection**

Desktop:
```bash
S=/private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/scratchpad
cd /Users/henrik/Code/Capsor-web/capsor-web
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CH" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=3000 --window-size=1440,5200 --screenshot="$S/redesign-desktop.png" "file://$PWD/index.html"
```
Phone, at a true 375px viewport. `--window-size` clamps to about 500px on this machine, so use the Chrome DevTools Protocol helper:
```bash
"$CH" --headless=new --disable-gpu --hide-scrollbars --remote-debugging-port=9333 about:blank >/dev/null 2>&1 &
CHPID=$!
sleep 2
python3 $S/cdp_shot.py "file://$PWD/index.html" 375 6200 $S/redesign-mobile.png
kill $CHPID
```
(`$S/cdp_shot.py` already exists. Its arguments are URL, width, height and output path; it expects Chrome on port 9333. If it's missing, stop and report it.)

Open both PNGs with the Read tool, in sections if they're tall. Expected:
- **Desktop:**
  - The header shows a crisp logo.
  - Hero: the orange panel is on the left, with the text's left edge lined up with the section content below. The portrait fills the right side at full height. "days, not weeks." has a white bar under it.
  - Results are in 3 columns. The black band has a 2×2 grid.
  - The statement's last line sits on an orange block.
  - Track record has a warm background in two columns, with the domain list on the right.
  - Work with me shows 3 outlined cards. The CTA is an orange band with the button on the right. The footer is black.
  - All sections share the same left and right content edges.
- **Phone (375px):**
  - Nothing overflows horizontally, and the menu toggle is visible.
  - The hero text comes first, then a 300px-tall portrait crop with the face visible.
  - Every grid is one column, and the CTA button sits below its text.

Fix any CSS issue (minimal changes, and record them in your report), then repeat this step.

- [ ] **Step 9: Commit**

```bash
git add index.html styles.css assets/henrik.jpg scripts/check-site.sh scripts/contrast.py
git commit -m "Redesign site: bold orange hero, black band, SVG logo

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
(The `git rm` from Step 5 is already staged and goes into this commit.)

---

### Task 3: CV restyle to the new palette

**Files:**
- Modify: `cv/cv.css`, `CV_Henrik_Oscarsson_en.pdf` (regenerated)

**Interfaces:**
- Consumes: nothing from Tasks 1–2.
- Produces: the regenerated `CV_Henrik_Oscarsson_en.pdf` (the site links to it).

- [ ] **Step 1: Swap the blue for black**

In `cv/cv.css`:
- In `:root`, delete the line `--blue: #4a90c4;`.
- Replace every `var(--blue)` with `var(--ink)`. Today these are `.cv-title { color }` and `h2 { color }`.

Then verify: `grep -n "blue\|4a90c4" cv/cv.css`. Expected: no output.

- [ ] **Step 2: Regenerate and check the page count**

```bash
cd /Users/henrik/Code/Capsor-web/capsor-web
PUPPETEER_SKIP_DOWNLOAD=1 npx --yes md-to-pdf@5 cv/cv.md --config-file cv/md-to-pdf.config.js
python3 -c "import re;d=open('CV_Henrik_Oscarsson_en.pdf','rb').read();print(len(re.findall(rb'/Type\s*/Page(?!s)',d)))"
```
Expected: `2`. Colour changes don't affect layout, so it shouldn't change. If it isn't 2, stop and report it; don't touch the font size.

- [ ] **Step 3: Inspect the PDF**

Open `CV_Henrik_Oscarsson_en.pdf` with the Read tool. Expected:
- The title line and section headings are black, with no blue anywhere.
- The orange rule under the header and the orange bullets are unchanged.
- The photo renders, and page 2 starts with "Earlier career".

- [ ] **Step 4: Commit**

```bash
git add cv/cv.css CV_Henrik_Oscarsson_en.pdf
git commit -m "Restyle CV headings from blue to black

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
