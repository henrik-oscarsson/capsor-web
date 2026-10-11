# Site redesign: design

**Date:** 2026-10-11
**Status:** Approved in brainstorming, pending written-spec review
**Builds on:** `2026-10-11-copy-and-cv-refresh-design.md` (copy is settled; this spec changes presentation, not message)

## Goal

Redesign capsor.se in "Direction B · Bold split": an orange hero with a full-height portrait, sections alternating white and black, and a palette reduced to the brand orange plus black and white. The aim is for the site to read as one confident personal brand for a CTO, rather than a template. All current copy is kept, except for the explicit hero adjustment described below.

Mockups from the session (reference only, git-ignored): `.superpowers/brainstorm/36642-1791746761/content/full-page-b.html` (approved whole page) and `mobile-hero.html` (option A chosen).

## Out of scope

- Dark mode (explicitly declined).
- Copy changes other than the hero adjustment below.
- New pages, a blog, a static site generator, or JavaScript beyond the existing one-line menu toggle.
- Animations.
- A new favicon.

## File structure

| Path | Purpose |
|---|---|
| `index.html` | Markup and content only; links `styles.css`. |
| `styles.css` | All site styling (moved out of the inline `<style>` block). |
| `assets/logo.svg` | Recreated logo: "Capsor" in Cocktail Shaker converted to outlines, plus the orange square outline. |
| `assets/henrik.jpg` | High-resolution greyscale portrait for the hero, generated from the original 1355×1523 source (`/private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/images/1.jpg`; this is session scratch space, so if it's gone, ask Henrik for the photo again). Resized to 1000px on the long edge, greyscale, JPEG quality about 82. |
| `henrik.jpg` (root) | **Unchanged.** Still used by the CV (`cv/cv.md` references `/henrik.jpg`). |
| `scripts/build-logo.mjs` | One-off Node script that converts the text to SVG paths with `opentype.js`. It reads the font from Henrik's local path and writes `assets/logo.svg`. The font file is never committed or published. |
| `.gitignore` | New. Contains `.superpowers/` and `node_modules/`. |
| Removed | `iStock-1291279253.jpg`, `CapsorWebSiteLogo.jpg`. |

The site stays a static site served by GitHub Pages from `master` with no build step. `scripts/build-logo.mjs` is a dev-only tool run once; its output is committed.

## Visual system

### Colours

Defined as CSS custom properties in `styles.css`. These are the only colours used.

| Token | Value | Use |
|---|---|---|
| `--orange` | `rgb(230, 139, 20)` | Hero panel, CTA band, numbers and label in "How I work" (on black), link underlines, block behind "Faster teams." |
| `--black` | `#111` | Text, "How I work" band, footer, buttons |
| `--white` | `#fff` | Page background |
| `--warm` | `#f5f2ed` | Track record background |
| `--muted` | `#555` on light backgrounds, `#bbb` on black | Secondary text |
| `--rule-dark` | `#444` | Rules on the black band |
| `--rule-warm` | `#d8d2c8` | Rules on the warm background |

The current blue (`#4a90c4`) and lime (`#9DFF20`) are removed from the site.

**Contrast:** every text/background pair must meet WCAG AA (4.5:1 for body text, 3:1 for text ≥24px, or ≥18.66px bold). White on orange and orange on white are both 2.60:1, so **orange is never a text colour on white, and white is never a text colour on orange**. Measured pairs: black on orange 7.25, orange on black 7.25, #555 on white 7.46, #bbb on black 9.84, #555 on warm 6.68, #999 on black 6.63, black on warm 16.91.

Accent treatments (chosen by Henrik in the contrast comparison):
- **Hero "days, not weeks." (option B):** black text with a white highlighter stroke underneath, `box-shadow: inset 0 -0.32em 0 var(--white)`.
- **Statement "Faster teams." (option E):** black text on an orange block, `background: var(--orange); padding: 0 0.1em; box-decoration-break: clone`.

### Typography

- **DM Sans** (400, 500, 700) for text and headings; **IBM Plex Mono** (400, 500) for uppercase labels and result numbers. Both from Google Fonts, as today.
- Hero H1: `clamp(2.25rem, 5.5vw, 4rem)`, weight 700, letter-spacing −0.035em, line-height 1.05.
- Statement: `clamp(2.5rem, 7vw, 5rem)`, uppercase, weight 700, letter-spacing −0.04em, line-height 1.02.
- Section labels: IBM Plex Mono, 0.75rem, uppercase, letter-spacing 0.1em.
- Body: 1.05rem, line-height 1.7.

### Layout

- Content max width 1100px, side padding `clamp(1.25rem, 4vw, 3rem)`. All sections use the same inner width, so their left and right edges line up (the lesson from the earlier 720px mismatch).
- Single breakpoint at 720px (phone layout below it).

### Logo

- `assets/logo.svg`: "Capsor" set in Cocktail Shaker (regular glyphs; no alternates), converted to paths and filled `#111`, with an orange square outline (`--orange`) behind "Ca". Proportions match the current `CapsorWebSiteLogo.jpg`: square ≈ 41% of total width and ≈ 93% of total height, top-left aligned; text overlaps the square's right edge, and the "p" descender extends below the square.
- Transparent background; a `viewBox` that crops tightly; `role="img"` and `<title>Capsor AB</title>`.
- Shown in the header at 40px tall on desktop and 32px on a phone.

## Page structure

| # | Section | Background | Desktop | Phone (<720px) |
|---|---|---|---|---|
| 1 | Header | White, sticky, bottom border `#eee` | Logo · How I work · Work with me · CV · *Get in touch* (black pill) | Logo + existing menu toggle |
| 2 | Hero | `--orange` panel + portrait | Grid 1.45fr / 1fr, min-height 560px; text vertically centred; portrait `object-fit: cover`, full height | Text block first, then portrait as a 300px-tall wide crop (`object-position: 50% 30%`) |
| 3 | Results | White | Lead label "At CIKO, since April 2026", then 3 columns with a 3px black top rule, mono number (black) and label (`--muted`) | Stacked |
| 4 | How I work (`#how`) | `--black` | Orange label "How I work", a one-line H2, then a 2×2 grid; each item has a `#444` top rule, an orange mono number, a bold title and `#bbb` text | One column |
| 5 | Statement | White | "Fewer rituals.<br>More flow.<br>Faster teams." uppercase, with the last line as black text on an orange block (option E) | Smaller per clamp |
| 6 | Track record | `--warm` | Two columns (1fr / 1.1fr): left has the label, H2 and story paragraph plus the CV links; right has the domain list with `--rule-warm` separators | Stacked |
| 7 | Work with me (`#work`) | White | Label, intro line, three cards with a 2px black border and 10px radius | Stacked |
| 8 | CTA | `--orange` | "Let's talk." + paragraph on the left, black pill button on the right | Stacked |
| 9 | Footer | `--black`, text `#999` | "© 2008–2026 Capsor AB" left, `henrik@capsor.se` right | Stacked, centred |

### Copy mapping

Copy comes from the current `index.html` and `docs/positioning.md`. Changes:

- **Hero:** label "Henrik Oscarsson · CTO"; H1 "Engineering teams that ship in <span>days, not weeks.</span>" (span in black with a white highlighter stroke underneath, option B); paragraph "I make engineering teams faster by changing how they work, not by adding process. CTO at CIKO, building Trygga." Buttons: *Get in touch* (`mailto:henrik@capsor.se`) and *Read my CV* (`CV_Henrik_Oscarsson_en.pdf`, new tab).
- The old intro paragraph (`#about`) is removed; the hero line above replaces it.
- **How I work H2:** "Four deliberate choices that remove friction and give people ownership." This replaces the current intro sentence "None of this is complicated. It's a handful of deliberate choices…".
- **Track record H2:** "25 years building the systems myself." The paragraph keeps its current wording minus the now-redundant opening clause: "Often where latency, reliability and scale aren't negotiable. Before CIKO, I was CTO at Valuno Group, and I've spent many years working in high-transaction environments, most of them trading systems." The domain list keeps all five current items, including "Also contracted by — Nokia and Microsoft".
- **CTA:** H2 "Let's talk." and the current paragraph.
- Everything else is verbatim from the current page: results, principles text, work-with-me items.

## Accessibility

- Visible `:focus-visible` outline (2px, offset 3px; black on light backgrounds, orange on black).
- Portrait alt text: "Henrik Oscarsson". Logo SVG has a title. The visually hidden "Three teams to one" label is kept.
- Heading order: one H1 (hero); H2 per section; H3 for principles and cards.
- No content conveyed by colour alone.

## CV restyle

In `cv/cv.css` only: replace `--blue` usages (title line, H2 section headings) with `--ink` (#111). Keep the orange header rule and bullet markers. Regenerate `CV_Henrik_Oscarsson_en.pdf`; it must stay exactly two pages.

## Verification

- Update `check-site.sh` for the new structure. Required strings: headline, statement, the three result values, the four principle titles, `id="how"`, `id="work"`, `assets/logo.svg`, `styles.css`. Forbidden: `iStock`, `CapsorWebSiteLogo`, `#4a90c4`, `#9DFF20` (in `index.html` and `styles.css`). Every local `href`/`src` in `index.html` must exist.
- Screenshots at 1280px desktop and at a true 375px viewport using the Chrome DevTools Protocol device-metrics override (not `--window-size`, which clamps to about 500px on this machine). Check for: no horizontal overflow, correct stacking, the logo is sharp, and the hero portrait is well cropped.
- Contrast: compute ratios for every text/background pair actually used in `styles.css`, list them in the report, and confirm each meets the thresholds above. In particular, no white text on orange and no orange text on white.
- CV: page count = 2, inspected visually.

## Deploy note

capsor.se and www.capsor.se are cached separately by GitHub's CDN for up to 10 minutes after a push, so the two can briefly differ.
