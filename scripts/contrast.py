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
