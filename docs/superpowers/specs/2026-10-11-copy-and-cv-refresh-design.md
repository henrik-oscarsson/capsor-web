# Copy and CV refresh — design

**Date:** 2026-10-11
**Status:** Approved in brainstorming, pending written-spec review

## Goal

Reposition Henrik Oscarsson (Capsor AB) as a CTO and senior technical leader whose edge is changing *how teams work*, backed by 25 years of hands-on depth. Deliver:

1. A positioning brief, the single source of truth for copy.
2. Rewritten website copy with a light restructure of `index.html`.
3. A new two-page, leadership-focused CV written in Markdown and rendered to PDF.

A visual redesign of the site is explicitly **out of scope**. It is a possible follow-up project once the copy is settled.

## Audience

- **Primary:** recruiters, boards and founders hiring a CTO. The site reads as Henrik's professional profile.
- **Secondary (close second):** companies looking for interim CTO or advisory help via Capsor.

## Voice

- **Website:** first person ("I help teams…"). Direct and conversational.
- **CV:** implied first-person bullets ("Merged three teams into one…"). No third person ("Henrik has…").
- **Language:** English.

## Files

| Path | Purpose |
|---|---|
| `docs/positioning.md` | Positioning brief (content below), the source for site and CV copy. |
| `index.html` | New copy and light restructure. |
| `henrik.jpg` | Portrait (B/W), used by both the site and the CV. Source: the image Henrik supplied. |
| `cv/cv.md` | New two-page CV source. |
| `cv/cv.css` | Print stylesheet matching the site's fonts and colours (DM Sans, IBM Plex Mono, `#4a90c4`, orange accent). |
| `CV_Henrik_Oscarsson_en.pdf` | **Generated** from `cv/cv.md`, overwriting the current file so existing links keep working. |
| `CV_Henrik_Oscarsson_full_en.pdf` | Full project history: a copy of `~/Documents/Capsor/Konsultprofil/Konsultprofil_Henrik_Oscarsson_en_cto.pdf`, the updated 6-page Word export that includes iFACTS, AMEX 2020 and Trust Anchor Group. To update it later, re-export from the `.docx` and copy it over. |

**PDF generation:** `npx md-to-pdf cv/cv.md` using `cv/cv.css`. It must use the locally installed Google Chrome (via `launch_options.executablePath`) to avoid downloading Chromium. The exact command goes in `README.md`.

## Positioning brief (content of `docs/positioning.md`)

**Positioning statement**
> I make engineering teams faster by changing how they work, not by adding process. My 25 years of hands-on engineering in trading, payments and high-performance systems mean the advice holds up technically.

**Headlines**
- Primary (site H1 and CV tagline basis): *Engineering teams that ship in days, not weeks.*
- Secondary (orange banner): *Fewer rituals. More flow. Faster teams.*

**Proof points**: CIKO / Trygga, April 2026 to present (under 6 months)
- **3 teams → 1**: 15 engineers working as one team, with tight, everyday communication.
- **Days, not weeks**: features ship in 1–2 days instead of 1–2 weeks.
- **Under 6 months**: how long the change took.

Context: CIKO is a Swedish job security council (transition organisation). It builds its own platform, Trygga, and licenses it to other transition organisations in Sweden. Henrik is CTO and leads the Trygga build.

**How I work** (four principles)
1. **One standup, one topic.** The day's most important thing, not a ticket-by-ticket status round. Meetings stay short and relevant.
2. **Under half a day? Just do it.** No tickets and no permission needed for small fixes, tech debt or improvements. It creates flow and ownership, and the platform keeps getting better on its own.
3. **Work in twos and threes.** Small groups form around a task, so knowledge and a shared view of how we build spread naturally, without relying on documentation.
4. **Agentic by default.** Start with concrete, repetitive tasks ("build a UI component to our standards, with tests"), then move to agentic frameworks (e.g. Superpowers) that handle the orchestration.

**Technical depth**
- Trading and exchanges: AMEX, Credit Suisse, NASDAQ OMX, SIX Telekurs, SFE.
- Crypto payments: Quickbit / Valuno (high-transaction, regulated).
- High-performance systems: real-time rendering, threading models, latency.
- Insurance: iFACTS. Healthtech: FRISQ. Marketplaces: Barnebys. Digital identity: Trust Anchor Group.
- Large delivery: tech lead for 16 developers in a 40-person e-commerce programme in London (ustwo / POWA).
- Also contracted by Nokia and Microsoft.

**Ways to work with me**
- **Permanent CTO**: building or turning around an engineering organisation.
- **Interim CTO**: covering a critical phase or a leadership gap.
- **Advisory**: ways of working and AI-driven development for an existing team.

## Website structure (`index.html`)

Reuse existing styles and colour variables. New CSS is limited to the results strip, the principles grid and the portrait.

1. `<title>`: "Henrik Oscarsson — CTO · Capsor AB". Meta description built from the positioning statement.
2. Nav: How I work (`#how`) · Work with me (`#work`) · CV · *Get in Touch* button. Remove "Home".
3. Hero image: unchanged.
4. H1: *Engineering teams that ship in <accent>days, not weeks</accent>.*
5. Intro (`#about`): 2–3 sentences covering who Henrik is, his CTO role at CIKO building Trygga, and the positioning statement. Includes a small round portrait (`henrik.jpg`).
6. Results strip (new): three columns, each with a large value in IBM Plex Mono and a short label. Values: `3 → 1` (teams, 15 engineers), `1–2 days` (per feature, down from weeks), `< 6 months` (to get there). Columns stack on mobile (≤640px).
7. How I work (`#how`): the four principles as a numbered 2×2 grid using the `.roles` card style. Single column on mobile. This replaces the "Building Strong Teams…" and "AI-First Engineering" sections.
8. Orange banner: *Fewer rituals. More flow. <white>Faster teams.</white>* This replaces "Passion for Software".
9. Track record: a short paragraph on technical depth, a compact list of domains and clients, and links to the CV and the full project history. This replaces "Recent Roles".
10. Work with me (`#work`): three short items (permanent, interim, advisory).
11. CTA: same black box, rewritten text, same `mailto:` button.
12. Footer: unchanged.

## CV structure (`cv/cv.md`, two A4 pages)

**Page 1: leadership**
- Header: name; "CTO · Engineering leadership & AI-driven development"; henrik@capsor.se, +46 (0)705 – 77 08 79, capsor.se, Stockholm; portrait. No LinkedIn unless Henrik supplies a URL.
- Profile: 3–4 sentences from the positioning statement.
- **CTO, CIKO (Trygga)**, Apr 2026 – present: 4–5 bullets with the proof points and how they were achieved (rituals, the half-day rule, small groups, rolling out agentic development).
- **CTO, Valuno Group (formerly Quickbit)**, Jan 2025 – Mar 2026. One entry showing the progression from Engineering Manager & Solution Architect (Jan–Apr 2025) to CTO (May 2025). Bullets: set the technical standard for crypto payments in a high-transaction, regulated environment; hired and built the team; mentoring and coaching; simplified the stack to fewer frameworks and languages; AI-first delivery.
- **Solution Architect & Tech Lead, Barnebys**, May 2022 – Oct 2023: architecture and performance; continuous deployment with at least daily deploys; mentoring.

**Page 2: depth**
- **Senior Developer, FRISQ**, Oct 2023 – Dec 2024. Short and presented honestly as a hands-on role: healthtech care-plan platform, FHIR, Angular/React, Spring Boot, GCP.
- **Earlier career (2000–2021)**: one line each, newest first:
  - Trust Anchor Group (Nov 2020 – Mar 2021): architected and built a Xamarin/.NET app for digital IDs and contracts.
  - AMEX (Sep 2020): architected an API (MERN) for an HR skills-management framework.
  - iFACTS (Feb 2019 – May 2020): performance-focused senior developer on an insurance and claims platform (.NET Core).
  - TFF (Jun 2017 – Dec 2018): tech lead and architect, performance review and improvements of a WPF/.NET system.
  - ustwo / POWA, London (Feb – Sep 2015): tech lead for 16 developers in a 40-person, £1M e-commerce programme.
  - NASDAQ OMX (Aug – Oct 2012): improved the performance of an electricity-certificate trading client (threading model, C++/MFC).
  - SIX Telekurs (2004 – 2012, several assignments): architect of the SIX Edge real-time trading terminal, including a DirectX real-time grid and MiFID support.
  - Credit Suisse, London (May 2010 – Jul 2011): software architect on a new FX and options trading system.
  - Atlantic Airways (Jun 2009 – Dec 2010): built an RFID tool-tracking system end-to-end, hardware and software.
  - SFE, Australia (Aug 2006 – Mar 2007): UI architect on a clearing and settlement system.
  - Collectum (Mar – Aug 2006): security and access-control model.
  - Tattersalls (Jun 2003 – Mar 2004): applications for an online gaming platform.
  - AMEX, New York (2000 – 2003): lead developer and designer of an equity-trading front-end migration from OpenVMS to .NET, including teaching the team C#.
- **Employment:** Capsor AB (founder, 2008–), dipod (founder, 2007–2008), Canvisa Consulting (software architect, 2004–2007), CATS (software developer, 2000–2004).
- **Skills:** Leadership: ways of working, team design, hiring, mentoring, C-suite steering groups, agentic/AI-driven development. Technical: architecture, performance, AWS/GCP/Azure, .NET/C#, Java, React, blockchain.
- **Education & training:** M.Sc. Computer Engineering, Uppsala University (2000); Designing and Building AI Products and Services, MIT xPro (2024); Certified Scrum Master (2009); Project Manager, Learning Tree (2006); Graphic Design & Communication, Berghs (2012).
- Footer: "Full project history: capsor.se/CV_Henrik_Oscarsson_full_en.pdf".

## Verification

- The site renders correctly at desktop width and at 375px (no horizontal scroll, strip and grid stack). All anchors and links resolve, including both PDFs.
- The generated CV PDF is exactly two A4 pages, the photo renders, and there are no orphaned headings.
- Every claim in the copy traces back to the brief or to Henrik's CV and notes. No invented metrics.

## Open items and follow-ups (not blocking)

- Henrik to confirm the Barnebys start date (he suspects it was earlier than May 2022). The remaining gap, Apr 2021 – Apr 2022, is left as is for now.
- Possible later project: a visual redesign of the site.
