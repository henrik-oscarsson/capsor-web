# capsor-web

This is the Capsor AB website. It is a plain one page html site.

## Copy

`docs/positioning.md` is the source of truth for the site and CV copy. Update it first.

## CV

The two-page CV is written in `cv/cv.md` and styled by `cv/cv.css`. To regenerate `CV_Henrik_Oscarsson_en.pdf` (needs Node and Google Chrome):

    PUPPETEER_SKIP_DOWNLOAD=1 npx --yes md-to-pdf@5 cv/cv.md --config-file cv/md-to-pdf.config.js

Run it from the repository root. It needs an internet connection: `cv/cv.css` loads DM Sans and IBM Plex Mono from Google Fonts, and without them the CV falls back to system fonts and may run past two pages.

Check that it is still two pages after editing.

`CV_Henrik_Oscarsson_full_en.pdf` is the full project history. Its source is the Word file `~/Documents/Capsor/Konsultprofil/Konsultprofil_Henrik_Oscarsson_en_cto.docx`. Export it to PDF and copy it over this file.
