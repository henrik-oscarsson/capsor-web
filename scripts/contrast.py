"""WCAG 2 contrast ratios for every text/background pair used on capsor.se.

Colours are read from styles.css itself (the :root custom properties, plus
the literal footer text colour in .site-footer) so this check can't drift
silently out of sync with the stylesheet. Usage:

    python3 scripts/contrast.py [path/to/styles.css]

Defaults to the repo's own styles.css when no path is given.
"""

import re
import sys
from pathlib import Path

REQUIRED_VARS = ["orange", "black", "white", "warm", "muted", "muted-dark"]


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def parse_color(value, context):
    value = value.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3})", value)
    if m:
        h = m.group(1)
        return tuple(int(c * 2, 16) for c in h)
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", value)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", value)
    if m:
        return tuple(int(g) for g in m.groups())
    fail(f"could not parse colour value {value!r} ({context})")


def load_root_vars(css):
    m = re.search(r":root\s*\{([^}]*)\}", css)
    if not m:
        fail("no :root { ... } block found in styles.css")
    body = m.group(1)
    found = {}
    for name, value in re.findall(r"--([\w-]+)\s*:\s*([^;]+);", body):
        found[name] = value.strip()
    colors = {}
    for name in REQUIRED_VARS:
        if name not in found:
            fail(f"missing required custom property --{name} in :root")
        colors[name] = parse_color(found[name], f"--{name}")
    return colors


def load_footer_color(css):
    m = re.search(r"\.site-footer\s*\{([^}]*)\}", css)
    if not m:
        fail("no .site-footer { ... } rule found in styles.css")
    body = m.group(1)
    m2 = re.search(r"\bcolor\s*:\s*([^;]+);", body)
    if not m2:
        fail("no color: declaration found inside .site-footer { ... }")
    return parse_color(m2.group(1), ".site-footer color")


def luminance(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def main():
    css_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "styles.css"
    if not css_path.is_file():
        fail(f"stylesheet not found: {css_path}")
    css = css_path.read_text()

    root_vars = load_root_vars(css)
    ORANGE = root_vars["orange"]
    BLACK = root_vars["black"]
    WHITE = root_vars["white"]
    WARM = root_vars["warm"]
    MUTED = root_vars["muted"]
    MUTED_DARK = root_vars["muted-dark"]
    FOOTER = load_footer_color(css)

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


if __name__ == "__main__":
    main()
