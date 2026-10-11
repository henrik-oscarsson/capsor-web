# Copy and CV Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition capsor.se and Henrik's CV around CTO-level leadership: a positioning brief, rewritten site copy with a light restructure, and a new two-page CV written in Markdown and rendered to PDF.

**Architecture:** `docs/positioning.md` is the source of truth for copy. `index.html` stays a single static page, and new CSS is added to its existing `<style>` block. The CV is `cv/cv.md` plus `cv/cv.css`, rendered by `md-to-pdf` (run via `npx`, using the locally installed Google Chrome) into `CV_Henrik_Oscarsson_en.pdf` at the repo root.

**Tech Stack:** Plain HTML/CSS, Markdown, `md-to-pdf@5` via `npx`, headless Google Chrome for screenshots, macOS `sips` for image resizing.

**Spec:** `docs/superpowers/specs/2026-10-11-copy-and-cv-refresh-design.md`

## Global Constraints

- Language: English. Website voice: first person. CV voice: implied first-person bullets, never "Henrik has…".
- Reuse the existing CSS variables (`--color-secondary: #4a90c4`, `--color-orange`, `--font-sans: DM Sans`, `--font-mono: IBM Plex Mono`). Add no new colours.
- No invented claims or metrics. Every claim must trace to the spec's positioning brief or to the full project history PDF.
- Proof points, verbatim: **3 teams → 1** (15 engineers), **1–2 days per feature, down from 1–2 weeks**, **under 6 months** (CIKO, April 2026 – present).
- Headlines, verbatim: H1 *Engineering teams that ship in days, not weeks.*; banner *Fewer rituals. More flow. Faster teams.*
- Contact: henrik@capsor.se · +46 (0)705 – 77 08 79 · capsor.se · Stockholm. No LinkedIn.
- Barnebys dates: May 2022 – Oct 2023.
- Chrome binary: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.
- Work on branch `copy-refresh`. End every commit message with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## File Map

| Path | Task | Responsibility |
|---|---|---|
| `docs/positioning.md` | 1 | Positioning brief: the copy source of truth |
| `henrik.jpg` | 2 | Portrait, resized to 480px on the long edge, used by both site and CV |
| `CV_Henrik_Oscarsson_full_en.pdf` | 2 | Full project history, copied from `~/Documents/Capsor/Konsultprofil/Konsultprofil_Henrik_Oscarsson_en_cto.pdf` |
| `index.html` | 2 | New copy, structure and CSS |
| `cv/cv.md` | 3 | CV content |
| `cv/cv.css` | 3 | CV print styling |
| `cv/md-to-pdf.config.js` | 3 | md-to-pdf config (stylesheet, output path, A4, local Chrome) |
| `CV_Henrik_Oscarsson_en.pdf` | 3 | Generated two-page CV (overwrites the current file) |
| `README.md` | 3 | Documents how to regenerate the CV |

"Tests" for this project are verification commands: grep for required and forbidden strings, a local link check, headless-Chrome screenshots inspected visually, and a PDF page count.

---

### Task 1: Positioning brief

**Files:**
- Create: `docs/positioning.md`

**Interfaces:**
- Produces: the copy source that Tasks 2 and 3 quote from. Headlines, proof points and principle titles must match this file exactly.

- [ ] **Step 1: Write `docs/positioning.md`**

```markdown
# Positioning — Henrik Oscarsson

Source of truth for capsor.se and the CV. Change copy here first, then carry it over.

## Audience

1. Recruiters, boards and founders hiring a CTO (primary).
2. Companies looking for an interim CTO or advisory help via Capsor (close second).

## Positioning statement

I make engineering teams faster by changing how they work, not by adding process. My 25 years of hands-on engineering in trading, payments and high-performance systems mean the advice holds up technically.

## Headlines

- **Primary:** Engineering teams that ship in days, not weeks.
- **Secondary:** Fewer rituals. More flow. Faster teams.

## Proof points — CIKO / Trygga, April 2026 – present

CIKO is a Swedish job security council (transition organisation). It builds its own platform, Trygga, and licenses it to other transition organisations in Sweden. Henrik is CTO and leads the Trygga build.

- **3 teams → 1** — 15 engineers working as one team, with tight, everyday communication.
- **Days, not weeks** — features ship in 1–2 days instead of 1–2 weeks.
- **Under 6 months** — how long the change took.

## How I work

1. **One standup, one topic.** The day's most important thing, not a ticket-by-ticket status round. Meetings stay short and relevant.
2. **Under half a day? Just do it.** No tickets and no permission needed for small fixes, tech debt or improvements. It creates flow and ownership, and the platform keeps getting better on its own.
3. **Work in twos and threes.** Small groups form around a task, so knowledge and a shared view of how we build spread naturally, without relying on documentation.
4. **Agentic by default.** Start with concrete, repetitive tasks ("build a UI component to our standards, with tests"), then move to agentic frameworks (e.g. Superpowers) that handle the orchestration.

## Technical depth

- Trading and exchanges: AMEX, Credit Suisse, NASDAQ OMX, SIX Telekurs, SFE.
- Crypto payments: Quickbit / Valuno Group (high-transaction, regulated).
- High-performance systems: real-time rendering, threading models, latency.
- Insurance: iFACTS. Healthtech: FRISQ. Marketplaces: Barnebys. Digital identity: Trust Anchor Group.
- Large delivery: tech lead for 16 developers in a 40-person e-commerce programme in London (ustwo / POWA).
- Also contracted by Nokia and Microsoft.

## Ways to work with me

- **Permanent CTO** — building or turning around an engineering organisation.
- **Interim CTO** — covering a critical phase or a leadership gap.
- **Advisory** — ways of working and AI-driven development for an existing team.
```

- [ ] **Step 2: Verify the required strings are present**

Run:
```bash
cd /Users/henrik/Code/Capsor-web/capsor-web && for s in "Engineering teams that ship in days, not weeks." "Fewer rituals. More flow. Faster teams." "3 teams → 1" "1–2 days" "Under 6 months" "One standup, one topic." "Under half a day? Just do it." "Work in twos and threes." "Agentic by default."; do grep -qF "$s" docs/positioning.md && echo "OK  $s" || echo "MISSING  $s"; done
```
Expected: nine lines starting with `OK`.

- [ ] **Step 3: Commit**

```bash
git add docs/positioning.md
git commit -m "Add positioning brief

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Website copy and light restructure

**Files:**
- Create: `henrik.jpg`, `CV_Henrik_Oscarsson_full_en.pdf`
- Modify: `index.html`: `<title>`/meta (lines 7–9), CSS (insert before the `/* Responsive */` comment at line 321, plus additions inside the `@media (max-width: 640px)` block), and the whole `<body>` (lines 365–476)

**Interfaces:**
- Consumes: copy from `docs/positioning.md` (Task 1).
- Produces: `henrik.jpg` at the repo root, which Task 3's CV also uses. The site links to `CV_Henrik_Oscarsson_en.pdf` (regenerated in Task 3) and `CV_Henrik_Oscarsson_full_en.pdf`.

- [ ] **Step 1: Add the assets**

```bash
cd /Users/henrik/Code/Capsor-web/capsor-web
sips -Z 480 /private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/images/1.jpg --out henrik.jpg
cp ~/Documents/Capsor/Konsultprofil/Konsultprofil_Henrik_Oscarsson_en_cto.pdf CV_Henrik_Oscarsson_full_en.pdf
sips -g pixelWidth -g pixelHeight henrik.jpg
```
Expected: `henrik.jpg` is about 427×480. If the source photo is missing from the scratchpad, stop and ask Henrik for the image.

- [ ] **Step 2: Write the failing check script**

Create `/private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/scratchpad/check-site.sh`:

```bash
#!/bin/bash
# Verifies index.html copy and local links. Run from the repo root.
f=index.html; fail=0
need() { grep -qF -- "$1" "$f" && echo "OK       $1" || { echo "MISSING  $1"; fail=1; }; }
forbid() { grep -qF -- "$1" "$f" && { echo "FORBIDDEN $1"; fail=1; } || echo "OK (gone) $1"; }
need "<title>Henrik Oscarsson — CTO · Capsor AB</title>"
need 'days, not weeks</span>.'
need "Fewer rituals. More flow."
need '<span class="white">Faster teams.</span>'
need "3 → 1"; need "1–2 days"; need "&lt; 6 months"
need "One standup, one topic."; need "Under half a day? Just do it."
need "Work in twos and threes."; need "Agentic by default."
need 'id="how"'; need 'id="work"'; need 'href="#how"'; need 'href="#work"'
need "CIKO"; need "Trygga"
forbid "Passion for"; forbid "Most recently, I'm serving as CTO at Valuno"; forbid ">Home<"
# every local href/src must exist on disk
for p in $(grep -oE '(href|src)="[^"#:]+"' "$f" | sed -E 's/^(href|src)="//; s/"$//'); do
  [ -e "$p" ] && echo "OK file  $p" || { echo "MISSING FILE $p"; fail=1; }
done
exit $fail
```

Run: `bash /private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/scratchpad/check-site.sh`
Expected: FAIL, with several `MISSING` lines (e.g. the title, `3 → 1`) and `FORBIDDEN Passion for`.

- [ ] **Step 3: Update `<title>` and the meta description**

Replace lines 7–9 with:

```html
    <title>Henrik Oscarsson — CTO · Capsor AB</title>
    <meta name="description"
        content="Henrik Oscarsson is a CTO who makes engineering teams faster by changing how they work, not by adding process. 25 years in trading, payments and high-performance systems.">
```

- [ ] **Step 4: Add the new CSS**

Insert immediately before the `/* Responsive */` comment:

```css
        /* Intro with portrait */
        .intro {
            display: flex;
            align-items: center;
            gap: 2rem;
        }

        .portrait {
            width: 128px;
            height: 128px;
            border-radius: 50%;
            object-fit: cover;
            flex-shrink: 0;
        }

        /* Results strip */
        .results-lead {
            font-family: var(--font-mono);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--color-gray);
            margin-bottom: 1.25rem;
        }

        .results {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            list-style: none;
        }

        .result-value {
            display: block;
            font-family: var(--font-mono);
            font-size: clamp(2rem, 5vw, 2.75rem);
            font-weight: 500;
            line-height: 1.1;
            color: var(--color-secondary);
        }

        .result-label {
            display: block;
            margin-top: 0.5rem;
            color: #444;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        /* Principles grid */
        .principles {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.25rem;
            list-style: none;
            margin-top: 1.5rem;
        }

        .principles .roles {
            margin-top: 0;
            padding: 2rem;
        }

        .principle-num {
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: var(--color-secondary);
        }

        .principles h3 {
            font-size: 1.15rem;
            font-weight: 700;
            margin: 0.25rem 0 0.5rem;
        }

        /* Lists in content blocks */
        .content-block ul.plain {
            list-style: none;
            margin-top: 1.25rem;
            max-width: 720px;
        }

        .content-block ul.plain li {
            padding: 0.6rem 0;
            border-top: 1px solid rgba(0, 0, 0, 0.08);
            color: #444;
        }

        .content-block .links {
            margin-top: 1.25rem;
        }

        .content-block .links a {
            color: var(--color-secondary);
            font-weight: 500;
        }
```

Then add these rules inside the existing `@media (max-width: 640px) { ... }` block, after the `.roles { padding: 1.75rem; }` rule:

```css
            .intro {
                flex-direction: column;
                align-items: flex-start;
                gap: 1.25rem;
            }

            .results,
            .principles {
                grid-template-columns: 1fr;
            }
```

- [ ] **Step 5: Replace the `<body>` content**

Replace everything from `<body>` to `</body>` (inclusive) with:

```html
<body>
    <!-- Header -->
    <header>
        <nav>
            <a href="#" class="logo"><img src="CapsorWebSiteLogo.jpg" alt="Capsor AB" title="Capsor AB"></a>
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
                <li><a href="mailto:henrik@capsor.se" class="btn-nav">Get in Touch</a></li>
            </ul>
        </nav>
    </header>

    <!-- Hero Image -->
    <div class="hero-image">
        <img src="iStock-1291279253.jpg" alt="Ones and zeros — digital technology" loading="eager">
    </div>

    <!-- Hero -->
    <section class="hero">
        <h1>Engineering teams that ship in <span class="hero-accent">days, not weeks</span>.</h1>
    </section>

    <!-- About -->
    <section id="about">
        <div class="intro">
            <img src="henrik.jpg" alt="Henrik Oscarsson" class="portrait">
            <p class="about-text">I'm Henrik Oscarsson, CTO at CIKO, where I lead the team building Trygga, a
                platform CIKO uses itself and licenses to other transition organisations in Sweden. I make
                engineering teams faster by changing how they work, not by adding process. Behind that are 25 years
                of hands-on engineering in trading, payments and high-performance systems, so the advice holds up
                technically.</p>
        </div>
    </section>

    <!-- Results -->
    <div class="content-block">
        <p class="results-lead">At CIKO, in under six months</p>
        <ul class="results">
            <li>
                <span class="result-value">3 → 1</span>
                <span class="result-label">Three teams of 15 engineers, now working as one team with tight,
                    everyday communication.</span>
            </li>
            <li>
                <span class="result-value">1–2 days</span>
                <span class="result-label">Typical time to ship a feature, down from 1–2 weeks.</span>
            </li>
            <li>
                <span class="result-value">&lt; 6 months</span>
                <span class="result-label">From joining to a new way of working, in place and delivering.</span>
            </li>
        </ul>
    </div>

    <div class="divider">
        <hr>
    </div>

    <!-- How I work -->
    <div class="content-block" id="how">
        <h2>How I work<span class="dot">.</span></h2>
        <p>None of this is complicated. It's a handful of deliberate choices that remove friction and give people
            ownership.</p>
        <ol class="principles">
            <li class="roles">
                <span class="principle-num">01</span>
                <h3>One standup, one topic.</h3>
                <p>Instead of a ticket-by-ticket status round, each day's standup is about the single most important
                    thing for the team right now. Meetings stay short, and everyone leaves knowing what matters
                    today.</p>
            </li>
            <li class="roles">
                <span class="principle-num">02</span>
                <h3>Under half a day? Just do it.</h3>
                <p>Small fixes, tech debt and improvements don't need a ticket, a refinement session or permission.
                    That creates flow and ownership, and the platform keeps getting better on its own.</p>
            </li>
            <li class="roles">
                <span class="principle-num">03</span>
                <h3>Work in twos and threes.</h3>
                <p>When a task needs it, people group up in pairs or threes. Knowledge spreads naturally, and the
                    team builds a shared view of how we build things, without relying on documentation.</p>
            </li>
            <li class="roles">
                <span class="principle-num">04</span>
                <h3>Agentic by default.</h3>
                <p>I introduce AI by example: start with concrete, repetitive tasks like "build a UI component to our
                    standards, with tests", then move to agentic frameworks that handle the orchestration. Features
                    that used to take 1–2 weeks now ship in 1–2 days.</p>
            </li>
        </ol>
    </div>

    <!-- Banner -->
    <div class="passion-banner">
        <div class="inner">
            <h2>Fewer rituals. More flow. <span class="white">Faster teams.</span></h2>
        </div>
    </div>

    <!-- Track record -->
    <div class="content-block">
        <h2>Track record<span class="dot">.</span></h2>
        <p>My advice on ways of working holds up because I've spent 25 years building the systems myself, often
            where latency, reliability and scale aren't negotiable. Before CIKO, I was CTO at Valuno Group (formerly
            Quickbit), setting the technical standard for crypto payments in a high-transaction, regulated
            environment.</p>
        <ul class="plain">
            <li><strong>Trading and exchanges</strong> — AMEX in New York, Credit Suisse in London, NASDAQ OMX,
                SIX Telekurs, SFE in Australia.</li>
            <li><strong>High-performance systems</strong> — real-time trading terminals, threading models,
                latency-critical clients.</li>
            <li><strong>Product platforms</strong> — Barnebys (marketplaces), FRISQ (healthtech), iFACTS
                (insurance), Trust Anchor Group (digital identity).</li>
            <li><strong>Large-scale delivery</strong> — tech lead for 16 developers in a 40-person e-commerce
                programme in London.</li>
            <li><strong>Also contracted by</strong> — Nokia and Microsoft.</li>
        </ul>
        <p class="links"><a href="CV_Henrik_Oscarsson_en.pdf" target="_blank" rel="noopener">Read my CV (PDF)</a>
            &nbsp;·&nbsp; <a href="CV_Henrik_Oscarsson_full_en.pdf" target="_blank" rel="noopener">Full project
                history (PDF)</a></p>
    </div>

    <div class="divider">
        <hr>
    </div>

    <!-- Work with me -->
    <div class="content-block" id="work">
        <h2>Work with me<span class="dot">.</span></h2>
        <p>I'm currently CTO at CIKO, and always happy to talk about what's next. Through Capsor, I work in three
            ways:</p>
        <ul class="plain">
            <li><strong>Permanent CTO</strong> — building an engineering organisation, or turning one around.</li>
            <li><strong>Interim CTO</strong> — covering a critical phase or a leadership gap, with a clear
                handover.</li>
            <li><strong>Advisory</strong> — helping an existing team adopt leaner ways of working and AI-driven
                development.</li>
        </ul>
    </div>

    <!-- CTA -->
    <div class="cta">
        <div class="cta-box">
            <h2>Let's talk</h2>
            <p>Whether you're hiring a CTO, need a steady hand through a critical phase, or want your team shipping
                in days instead of weeks, I'd be glad to hear what you're working on.</p>
            <a href="mailto:henrik@capsor.se" class="btn-cta">Get in Touch</a>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <span>&copy; 2008-2026 Capsor AB. All Rights Reserved.</span>
    </footer>
</body>
```

- [ ] **Step 6: Run the check script**

Run: `bash /private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/scratchpad/check-site.sh`
Expected: exit 0. Every line starts with `OK`, and there are no `MISSING`/`FORBIDDEN` lines.

- [ ] **Step 7: Screenshot at desktop and mobile width, then inspect**

```bash
cd /Users/henrik/Code/Capsor-web/capsor-web
S=/private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/scratchpad
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CH" --headless=new --disable-gpu --hide-scrollbars --window-size=1280,4200 --screenshot="$S/site-desktop.png" "file://$PWD/index.html"
"$CH" --headless=new --disable-gpu --hide-scrollbars --window-size=375,7000 --screenshot="$S/site-mobile.png" "file://$PWD/index.html"
```
Open both PNGs with the Read tool. Expected:
- Desktop: round portrait beside the intro; three results in one row; principles in a 2×2 grid; orange banner reads "Fewer rituals. More flow. Faster teams." with the last part in white.
- Mobile: no content cut off at the right edge; the portrait sits above the intro text; results and principles stack in one column.

Fix any CSS issue and repeat this step until both look right.

- [ ] **Step 8: Commit**

```bash
git add index.html henrik.jpg CV_Henrik_Oscarsson_full_en.pdf
git commit -m "Rewrite site copy around CTO positioning

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Two-page leadership CV

**Files:**
- Create: `cv/cv.md`, `cv/cv.css`, `cv/md-to-pdf.config.js`
- Modify: `README.md`, `CV_Henrik_Oscarsson_en.pdf` (regenerated)

**Interfaces:**
- Consumes: `henrik.jpg` at the repo root (Task 2); copy from `docs/positioning.md` (Task 1).
- Produces: `CV_Henrik_Oscarsson_en.pdf` at the repo root (linked from `index.html`).

Note on ordering: page 1 lists CIKO, Valuno, FRISQ and Barnebys in reverse-chronological order. FRISQ (Oct 2023 – Dec 2024) is more recent than Barnebys, so it stays on page 1 as a short entry instead of moving to page 2 as the spec sketched. That keeps the timeline honest.

- [ ] **Step 1: Write the md-to-pdf config**

Create `cv/md-to-pdf.config.js`:

```js
const path = require('path');

const root = path.join(__dirname, '..');

module.exports = {
	basedir: root,
	stylesheet: [path.join(__dirname, 'cv.css')],
	dest: path.join(root, 'CV_Henrik_Oscarsson_en.pdf'),
	pdf_options: {
		format: 'A4',
		margin: { top: '16mm', right: '16mm', bottom: '16mm', left: '16mm' },
		printBackground: true,
	},
	launch_options: {
		executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	},
};
```

- [ ] **Step 2: Write the stylesheet**

Create `cv/cv.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
	--blue: #4a90c4;
	--orange: rgb(230, 139, 20);
	--ink: #111;
	--text: #333;
	--muted: #666;
}

html { font-size: 9.6pt; }

body {
	font-family: 'DM Sans', system-ui, sans-serif;
	color: var(--text);
	line-height: 1.45;
	margin: 0;
}

.cv-header {
	display: flex;
	align-items: center;
	gap: 18px;
	padding-bottom: 10px;
	border-bottom: 3px solid var(--orange);
	margin-bottom: 10px;
}

.cv-photo {
	width: 84px;
	height: 84px;
	border-radius: 50%;
	object-fit: cover;
}

h1 {
	font-size: 2.3rem;
	color: var(--ink);
	margin: 0;
	letter-spacing: -0.02em;
	line-height: 1.1;
}

.cv-title {
	font-size: 1.15rem;
	font-weight: 500;
	color: var(--blue);
	margin: 2px 0;
}

.cv-contact {
	font-family: 'IBM Plex Mono', monospace;
	font-size: 0.85rem;
	color: var(--muted);
	margin: 0;
}

h2 {
	font-family: 'IBM Plex Mono', monospace;
	font-size: 0.9rem;
	font-weight: 500;
	text-transform: uppercase;
	letter-spacing: 0.08em;
	color: var(--blue);
	border-bottom: 1px solid #ddd;
	padding-bottom: 3px;
	margin: 14px 0 6px;
	break-after: avoid;
}

h3 {
	font-size: 1.1rem;
	color: var(--ink);
	margin: 10px 0 0;
	break-after: avoid;
}

.meta {
	font-family: 'IBM Plex Mono', monospace;
	font-size: 0.82rem;
	color: var(--muted);
	margin: 0 0 3px;
}

p { margin: 0 0 4px; }

ul { margin: 2px 0 0; padding-left: 16px; }

li { margin: 1px 0; }

li::marker { color: var(--orange); }

ul.timeline { list-style: none; padding-left: 0; }

ul.timeline li {
	display: grid;
	grid-template-columns: 82px 1fr;
	gap: 8px;
	padding: 2px 0;
	break-inside: avoid;
}

.when {
	font-family: 'IBM Plex Mono', monospace;
	font-size: 0.82rem;
	color: var(--muted);
	padding-top: 1px;
}

.page-break { break-before: page; }

.cv-footer {
	margin-top: 14px;
	font-family: 'IBM Plex Mono', monospace;
	font-size: 0.82rem;
	color: var(--muted);
}
```

- [ ] **Step 3: Write the CV content**

Create `cv/cv.md`:

```markdown
<header class="cv-header">
<img src="henrik.jpg" alt="Henrik Oscarsson" class="cv-photo">
<div>
<h1>Henrik Oscarsson</h1>
<p class="cv-title">CTO · Engineering leadership &amp; AI-driven development</p>
<p class="cv-contact">henrik@capsor.se · +46 (0)705 – 77 08 79 · capsor.se · Stockholm</p>
</div>
</header>

## Profile

CTO who makes engineering teams faster by changing how they work, not by adding process. At CIKO, I turned three teams of 15 engineers into one and introduced agentic development, so features now ship in 1–2 days instead of 1–2 weeks. The change took under six months. Behind it are 25 years of hands-on engineering in trading, payments and high-performance systems for AMEX, Credit Suisse, NASDAQ OMX and SIX Telekurs, so the advice holds up technically. Comfortable in C-suite steering groups, anchoring technology decisions in the business and the other way round.

## Experience

### CTO — CIKO (Trygga)

<p class="meta">Apr 2026 – present · Stockholm</p>

CIKO is a Swedish job security council. Trygga is its own platform, which it also licenses to other transition organisations in Sweden.

- Turned three teams into one 15-person engineering team with tight, everyday communication, in under six months.
- Replaced ticket-by-ticket status meetings with one daily standup on the single most important topic.
- Removed tickets, refinement and approvals for anything under half a day, creating flow and ownership and a platform that keeps improving.
- Introduced working in pairs and threes to spread knowledge and a shared engineering approach.
- Rolled out agentic, AI-driven development (Claude, Superpowers). Features now ship in 1–2 days instead of 1–2 weeks.

### CTO — Valuno Group (formerly Quickbit)

<p class="meta">Jan 2025 – Mar 2026 · Engineering Manager &amp; Solution Architect, then CTO from May 2025</p>

Crypto payment solutions in a high-transaction environment with built-in monitoring and surveillance.

- Set the technical standard and direction for the payment platform (AWS, GCP, blockchain).
- Hired and built the engineering team; mentored and coached engineers.
- Simplified the platform to fewer moving parts, frameworks and languages.
- Introduced an AI-first approach to increase productivity and speed of delivery.

### Fullstack Developer — FRISQ

<p class="meta">Oct 2023 – Dec 2024</p>

Hands-on role building a community service for managing and sharing digital care plans: Angular and React frontends, Spring Boot microservices, FHIR integrations, Google Cloud. Also improved architecture and performance.

### Solution Architect &amp; Tech Lead — Barnebys Group

<p class="meta">May 2022 – Oct 2023</p>

White-label auction platform that gives Nordic auction houses an online presence.

- Improved the overall architecture, project structure and information flow, with significant performance gains.
- Established continuous deployment, with the team deploying at least once a day (Azure, Docker, Microsoft Orleans).
- Mentored developers.

<div class="page-break"></div>

## Earlier career

<ul class="timeline">
<li><span class="when">2020 – 21</span><span><strong>Trust Anchor Group</strong> — Architect and developer of a Xamarin/.NET app for managing digital IDs and contracts.</span></li>
<li><span class="when">2020</span><span><strong>AMEX</strong> — Architect and developer of an API (MongoDB, Express, React, Node.js) for an HR skills-management framework.</span></li>
<li><span class="when">2019 – 20</span><span><strong>iFACTS</strong> — Senior developer focused on performance in a large insurance and claims platform (.NET Core, SQL Server).</span></li>
<li><span class="when">2017 – 18</span><span><strong>TFF</strong> — Tech lead and architect: performance review and improvements of a WPF/.NET client, middleware and backend.</span></li>
<li><span class="when">2015</span><span><strong>ustwo / POWA Technologies, London</strong> — Tech lead for 16 developers in a 40-person, £1M e-commerce programme. Reviewed the backend and API libraries, and supervised mobile app development.</span></li>
<li><span class="when">2012</span><span><strong>NASDAQ OMX</strong> — Greatly improved the performance of an electricity-certificate trading client by reworking its threading model and model/view design (C++, MFC).</span></li>
<li><span class="when">2004 – 12</span><span><strong>SIX Telekurs</strong> — Architect and senior developer on the SIX Edge real-time trading terminal across several assignments: a DirectX real-time grid, MiFID support, order management and .NET migrations.</span></li>
<li><span class="when">2010 – 11</span><span><strong>Credit Suisse, London</strong> — Software architect on a new FX and options trading system, from pre-study to delivery (with HiQ and ustwo).</span></li>
<li><span class="when">2009 – 10</span><span><strong>Atlantic Airways</strong> — Built an RFID tool-tracking system end to end, hardware and software.</span></li>
<li><span class="when">2006 – 07</span><span><strong>SFE, Australia</strong> — UI architect and front-end lead on a clearing and settlement system.</span></li>
<li><span class="when">2006</span><span><strong>Collectum</strong> — Designed a security and access-control model for a multi-tier .NET platform (PKI).</span></li>
<li><span class="when">2003 – 04</span><span><strong>Tattersalls, Australia</strong> — Applications for an online gaming platform (Java, encrypted XML data).</span></li>
<li><span class="when">2000 – 03</span><span><strong>AMEX, New York</strong> — Front-end developer on a new equity trading system, then designer and lead developer of its migration from OpenVMS to .NET, including teaching the team C#.</span></li>
</ul>

## Employment

<ul class="timeline">
<li><span class="when">2008 –</span><span><strong>Founder, Capsor AB</strong> — consultancy through which the assignments above were delivered.</span></li>
<li><span class="when">2007 – 08</span><span><strong>Founder, dipod</strong></span></li>
<li><span class="when">2004 – 07</span><span><strong>Software Architect, Canvisa Consulting AB</strong></span></li>
<li><span class="when">2000 – 04</span><span><strong>Software Developer, CATS AB</strong></span></li>
</ul>

## Skills

**Leadership:** ways of working, team design and turnarounds, hiring, mentoring and coaching, C-suite steering groups, agentic and AI-driven development.

**Technical:** architecture and performance, AWS, GCP, Azure, .NET / C#, Java, React, Node.js, blockchain.

## Education &amp; training

<ul class="timeline">
<li><span class="when">2024</span><span>Designing and Building AI Products and Services, MIT xPro</span></li>
<li><span class="when">2012</span><span>Graphic Design &amp; Communication, Berghs School of Communication</span></li>
<li><span class="when">2009</span><span>Certified Scrum Master, London</span></li>
<li><span class="when">2006</span><span>Project Manager, Learning Tree</span></li>
<li><span class="when">2000</span><span>M.Sc. Computer Engineering, Uppsala University</span></li>
</ul>

<p class="cv-footer">Full project history: capsor.se/CV_Henrik_Oscarsson_full_en.pdf</p>
```

- [ ] **Step 4: Generate the PDF**

```bash
cd /Users/henrik/Code/Capsor-web/capsor-web
PUPPETEER_SKIP_DOWNLOAD=1 npx --yes md-to-pdf@5 cv/cv.md --config-file cv/md-to-pdf.config.js
ls -la CV_Henrik_Oscarsson_en.pdf
```
Expected: the command exits 0, and `CV_Henrik_Oscarsson_en.pdf` has a fresh timestamp. If md-to-pdf ignores `dest` and writes `cv/cv.pdf` instead, move it: `mv cv/cv.pdf CV_Henrik_Oscarsson_en.pdf`. Then update the README command in Step 7 to include that `mv`.

- [ ] **Step 5: Verify exactly two pages**

```bash
python3 -c "import re;d=open('CV_Henrik_Oscarsson_en.pdf','rb').read();print(len(re.findall(rb'/Type\s*/Page(?!s)',d)))"
```
Expected: `2`. If it prints `3`, shrink `html { font-size }` in `cv/cv.css` by 0.2pt steps (no lower than 9pt) and regenerate. If it's still 3 at 9pt, shorten the profile to three sentences.

- [ ] **Step 6: Inspect the PDF visually**

Open `CV_Henrik_Oscarsson_en.pdf` with the Read tool. Expected:
- Page 1: round photo, name, blue title, orange rule; Profile; CIKO, Valuno, FRISQ and Barnebys.
- Page 2 starts with "Earlier career"; dates sit in a left column; the footer link is at the end.
- DM Sans renders (not Times). No heading sits alone at the bottom of a page.

- [ ] **Step 7: Document the build in the README**

Replace `README.md` with:

```markdown
# capsor-web

This is the Capsor AB website. It is a plain one page html site.

## Copy

`docs/positioning.md` is the source of truth for the site and CV copy. Update it first.

## CV

The two-page CV is written in `cv/cv.md` and styled by `cv/cv.css`. To regenerate `CV_Henrik_Oscarsson_en.pdf` (needs Node and Google Chrome):

    PUPPETEER_SKIP_DOWNLOAD=1 npx --yes md-to-pdf@5 cv/cv.md --config-file cv/md-to-pdf.config.js

Check that it is still two pages after editing.

`CV_Henrik_Oscarsson_full_en.pdf` is the full project history. Its source is the Word file `~/Documents/Capsor/Konsultprofil/Konsultprofil_Henrik_Oscarsson_en_cto.docx`. Export it to PDF and copy it over this file.
```

- [ ] **Step 8: Re-run the site check (the CV link target now exists in its new form)**

Run: `bash /private/tmp/claude-501/-Users-henrik-Code-Capsor-web-capsor-web/c8010a1e-be9f-47f5-bdbc-12c541160c14/scratchpad/check-site.sh`
Expected: exit 0.

- [ ] **Step 9: Commit**

```bash
git add cv/ README.md CV_Henrik_Oscarsson_en.pdf
git commit -m "Add two-page leadership CV built from Markdown

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
