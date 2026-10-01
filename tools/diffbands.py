#!/usr/bin/env python3
"""Where do WordPress and v2 differ? Per page and width, mean pixel difference in 200px bands (0-255).
Needs tools/shots.js output in _qa/wp and _qa/v2. Bands above the threshold are listed with their y position."""
import sys, glob, os
from PIL import Image, ImageChops, ImageFilter
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_qa")
thr = float(sys.argv[1]) if len(sys.argv) > 1 else 6
def stitch(d, slug, n):
    parts = sorted(glob.glob(f"{root}/{d}/{slug}-{n}-*.jpg"), key=lambda p: int(p.rsplit("-", 1)[1][:-4])) or glob.glob(f"{root}/{d}/{slug}-{n}.jpg")
    ims = [Image.open(p).convert("L") for p in parts]
    if not ims: return None
    out = Image.new("L", (ims[0].width, sum(i.height for i in ims)))
    y = 0
    for i in ims: out.paste(i, (0, y)); y += i.height
    return out
slugs = sorted({os.path.basename(p)[:-4].rsplit("-", 1)[0] if os.path.basename(p)[:-4].rsplit("-", 1)[1].isdigit() else os.path.basename(p)[:-4] for p in glob.glob(f"{root}/wp/*.jpg")})
slugs = sorted({s.rsplit("-", 1)[0] for s in slugs if s[-2:] in ("-d", "-m")} | {s[:-2] for s in slugs if s[-2:] in ("-d", "-m")})
slugs = [s for s in slugs if s not in ("e404",) and not s.endswith(("-d", "-m"))]
for slug in slugs:
    for n in ("d", "m"):
        a, b = stitch("wp", slug, n), stitch("v2", slug, n)
        if not a or not b: continue
        h = min(a.height, b.height)
        d = ImageChops.difference(a.crop((0, 0, a.width, h)).filter(ImageFilter.GaussianBlur(1.2)), b.crop((0, 0, b.width, h)).filter(ImageFilter.GaussianBlur(1.2)))
        bands = []
        for y in range(0, h, 200):
            c = d.crop((0, y, d.width, min(h, y + 200)))
            m = sum(c.getdata()) / (c.width * c.height)
            if m > thr: bands.append((y, round(m, 1)))
        total = sum(d.getdata()) / (d.width * d.height)
        print(f"{slug:11} {n} {a.height:5}/{b.height:5} mean {total:4.1f} bands>{thr}: {bands[:8]}")
