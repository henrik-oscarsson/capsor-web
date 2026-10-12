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
need $H 'id="how"'; need $H 'id="notes"'; need $H 'href="#how"'; need $H 'href="#notes"'
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

forbid $H 'Permanent CTO'; forbid $H 'Interim CTO'; forbid $H 'hiring a CTO'; forbid $H "what's next"
exit $fail
