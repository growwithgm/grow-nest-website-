#!/usr/bin/env python3
"""Make the light logo variants and favicons from assets/img/grownest-logo.png.

The source logo is blue and grey on white. This script:
  1. removes the white background (anti-aliased edges become alpha),
  2. recolours it for the night sky:
       blue letters          -> #EEF0F7
       green arrow gradient  -> same hues, lightened
       grey "S" and tagline  -> #B8BCC6
  3. writes logo-light.png (with tagline) and logo-wordmark-light.png (GROW NEST only),
  4. crops the W-arrow onto a #0A0E1C rounded square for the favicons.

Run from the repo root:  python3 tools/make-logos.py
Needs Pillow and NumPy.
"""
import base64
import colorsys
import io
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
SRC = IMG / "grownest-logo.png"

INK_LIGHT = np.array([0xEE, 0xF0, 0xF7], float)
GREY_LIGHT = np.array([0xB8, 0xBC, 0xC6], float)
NIGHT = (0x0A, 0x0E, 0x1C, 255)


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def hue_deg(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = rgb.max(axis=-1)
    mn = rgb.min(axis=-1)
    d = mx - mn + 1e-9
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4))
    return h * 60.0


def blur(x, r=4, passes=3):
    """Approximate Gaussian blur: repeated separable box filters."""
    k = 2 * r + 1
    for _ in range(passes):
        for axis in (0, 1):
            pad = [(0, 0), (0, 0)]
            pad[axis] = (r + 1, r)
            c = np.cumsum(np.pad(x, pad, mode="edge"), axis=axis)
            x = (np.take(c, range(k, c.shape[axis]), axis=axis) - np.take(c, range(0, c.shape[axis] - k), axis=axis)) / k
    return x


def smooth_over(values, mask, r=4):
    """Average `values` over nearby pixels where `mask` is set (normalised convolution)."""
    m = mask.astype(float)
    return blur(values * m, r) / np.maximum(blur(m, r), 1e-6), blur(m, r)


def recolour(src):
    """Return an RGBA float array (0..255) of the light logo."""
    c = src.astype(float)
    # Colour-to-alpha against white: the smallest channel says how much ink there is.
    a = (255.0 - c.min(axis=-1)) / 255.0
    safe = np.maximum(a, 1e-4)[..., None]
    fg = np.clip(255.0 - (255.0 - c) / safe, 0, 255)  # un-mixed ink colour

    # Absolute chroma, not saturation: grey ink un-mixes to near black, where
    # saturation is unstable.
    chroma = fg.max(axis=-1) - fg.min(axis=-1)
    hue = hue_deg(fg)

    # JPEG noise makes the colour of thin edges unreliable, so classify solid
    # pixels only and let every pixel take the average class of its solid neighbours.
    solid = a > 0.5
    coloured = solid & (chroma > 60)
    is_col, _ = smooth_over(coloured.astype(float), solid, r=3)
    smooth_hue, _ = smooth_over(hue, coloured, r=4)

    # Solid letter blue un-mixes to alpha ~0.98 and solid grey to ~0.62, so scale
    # each class to reach full opacity on solid strokes.
    alpha = is_col * np.clip(a / 0.78, 0, 1) + (1 - is_col) * np.clip(a / 0.6, 0, 1)
    alpha[alpha < 0.06] = 0

    # Arrow weight: letter blue sits at hue ~195; the arrow runs teal (~185) to green (~140).
    w = smoothstep(193.0, 180.0, smooth_hue)
    arrow = np.zeros_like(fg)
    idx = w > 0
    hsv = np.stack([smooth_hue[idx] / 360.0], axis=-1)
    arrow[idx] = np.array([colorsys.hls_to_rgb(h, 0.64, 0.58) for h in hsv[:, 0]]) * 255.0

    col = INK_LIGHT * (1 - w[..., None]) + arrow * w[..., None]
    out = np.zeros(c.shape[:2] + (4,), float)
    out[..., :3] = GREY_LIGHT * (1 - is_col[..., None]) + col * is_col[..., None]
    out[..., 3] = alpha * 255.0
    return out


def to_image(arr):
    return Image.fromarray(np.clip(arr + 0.5, 0, 255).astype(np.uint8), "RGBA")


def crop_alpha(im, pad=0):
    box = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    l, t, r, b = box
    return im.crop((max(l - pad, 0), max(t - pad, 0), min(r + pad, im.width), min(b + pad, im.height)))


def resize(im, size):
    # Resample with premultiplied alpha so edges do not pick up a dark fringe.
    return im.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


def fit_height(im, h):
    return resize(im, (round(im.width * h / im.height), h))


def fit_width(im, w):
    return resize(im, (w, round(im.height * w / im.width)))


def icon(mark, size, radius_frac=0.22, pad_frac=0.14, rounded=True):
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    if rounded:
        d.rounded_rectangle((0, 0, size - 1, size - 1), radius=round(size * radius_frac), fill=NIGHT)
    else:
        d.rectangle((0, 0, size - 1, size - 1), fill=NIGHT)
    inner = size * (1 - 2 * pad_frac)
    s = inner / max(mark.width, mark.height)
    m = resize(mark, (max(1, round(mark.width * s)), max(1, round(mark.height * s))))
    tile.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return tile


def find_bands(alpha):
    """Rows that hold ink, grouped into bands (GROW, NEST, tagline)."""
    rows = (alpha > 20).any(axis=1)
    bands, start = [], None
    for y, on in enumerate(rows):
        if on and start is None:
            start = y
        elif not on and start is not None:
            bands.append((start, y))
            start = None
    if start is not None:
        bands.append((start, len(rows)))
    return [b for b in bands if b[1] - b[0] > 20]


def main():
    src = np.asarray(Image.open(SRC).convert("RGB"))
    light = to_image(recolour(src))
    alpha = np.asarray(light.getchannel("A"))
    bands = find_bands(alpha)
    assert len(bands) >= 3, f"expected GROW / NEST / tagline bands, got {bands}"
    grow, nest, tagline = bands[0], bands[1], bands[2]

    full = crop_alpha(light, pad=6)
    fit_width(full, 720).save(IMG / "logo-light.png", optimize=True)

    word = light.crop((0, grow[0], light.width, nest[1]))
    word = crop_alpha(word, pad=2)
    fit_height(word, 128).save(IMG / "logo-wordmark-light.png", optimize=True)

    # The W with its arrow: the rightmost letter of the GROW band.
    grow_strip = alpha[grow[0]:grow[1]]
    cols = (grow_strip > 20).any(axis=0)
    xs = np.where(cols)[0]
    # Walk left from the right edge until the gap before the W.
    x1 = xs.max() + 1
    x = x1 - 1
    while x > 0 and not (cols[x] == 0 and cols[x - 1] == 0 and cols[x - 2] == 0):
        x -= 1
    w_mark = crop_alpha(light.crop((x, grow[0], x1, grow[1])), pad=0)

    icon(w_mark, 32, pad_frac=0.06).save(IMG / "favicon-32.png", optimize=True)
    # iOS rounds the corners itself, so the touch icon is a full square.
    icon(w_mark, 180, pad_frac=0.16, rounded=False).save(IMG / "apple-touch-icon.png", optimize=True)

    big = icon(w_mark, 128, pad_frac=0.1, rounded=False)
    buf = io.BytesIO()
    big.save(buf, "PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        'viewBox="0 0 128 128">'
        '<clipPath id="r"><rect width="128" height="128" rx="28"/></clipPath>'
        f'<image clip-path="url(#r)" width="128" height="128" href="data:image/png;base64,{b64}"/>'
        "</svg>\n"
    )
    (IMG / "favicon.svg").write_text(svg)

    print("bands", bands, "W x-range", (x, x1))
    for name in ("logo-light.png", "logo-wordmark-light.png", "favicon-32.png", "apple-touch-icon.png", "favicon.svg"):
        p = IMG / name
        print(f"{name:26s} {p.stat().st_size:>7d} bytes", Image.open(p).size if p.suffix == ".png" else "")


if __name__ == "__main__":
    main()
