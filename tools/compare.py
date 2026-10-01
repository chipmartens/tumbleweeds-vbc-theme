#!/usr/bin/env python3
"""Side by side: WordPress (left) vs static v2 (right), full page stitched, cut into chunks.
python3 tools/compare.py [slug ...]   reads _qa/wp and _qa/v2 (from tools/shots.js), writes _qa/cmp/<slug>-<d|m>-<n>.jpg"""
import sys, glob, os
from PIL import Image, ImageDraw
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_qa")
os.makedirs(f"{root}/cmp", exist_ok=True)

def stitch(d, slug, n):
    parts = sorted(glob.glob(f"{root}/{d}/{slug}-{n}-*.jpg"), key=lambda p: int(p.rsplit("-", 1)[1][:-4])) or glob.glob(f"{root}/{d}/{slug}-{n}.jpg")
    ims = [Image.open(p) for p in parts]
    if not ims:
        return None
    W = ims[0].width
    H = sum(i.height for i in ims)
    out = Image.new("RGB", (W, H), "white")
    y = 0
    for i in ims:
        out.paste(i, (0, y)); y += i.height
    return out

slugs = sys.argv[1:] or sorted({os.path.basename(p).rsplit("-", 2)[0] if p.count("-") > 1 else p for p in []})
if not slugs:
    names = set()
    for p in glob.glob(f"{root}/wp/*.jpg"):
        b = os.path.basename(p)[:-4]
        parts = b.split("-")
        # slug-d or slug-d-1 ; slug may contain '-'
        if parts[-1].isdigit():
            parts = parts[:-1]
        names.add("-".join(parts[:-1]))
    slugs = sorted(names)
for slug in slugs:
    for n, scale, chunk in (("d", 0.5, 2000), ("m", 1.0, 1700)):
        a, b = stitch("wp", slug, n), stitch("v2", slug, n)
        if not a or not b:
            continue
        H = max(a.height, b.height)
        gap = 24
        W = a.width + b.width + gap
        canvas = Image.new("RGB", (W, H), (255, 0, 255))
        canvas.paste(a, (0, 0)); canvas.paste(b, (a.width + gap, 0))
        canvas = canvas.resize((int(W * scale), int(H * scale)))
        ch = int(chunk * scale) if n == "d" else chunk
        k = 0
        for y in range(0, canvas.height, ch):
            c = canvas.crop((0, y, canvas.width, min(canvas.height, y + ch)))
            c.save(f"{root}/cmp/{slug}-{n}-{k+1}.jpg", quality=80)
            k += 1
        print(slug, n, "WP", a.size, "v2", b.size, "chunks", k)
