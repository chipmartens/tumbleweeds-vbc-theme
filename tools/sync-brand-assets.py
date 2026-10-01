#!/usr/bin/env python3
"""Copy the finished brand assets from the project (../brand/logo, ../assets/cutouts) into the theme.
Run when brand/logo/READY.txt or assets/cutouts/READY.txt changes. The theme repo stays self-contained.
 - logo SVGs  -> assets/img/brand/
 - cutouts    -> assets/img/people/<slug>.png (resized to 900px wide, optimised)
 - tokens     -> tokens/brand-tokens.json (read by tools/tokens-to-scss.js)"""
import pathlib, shutil
from PIL import Image
root = pathlib.Path(__file__).resolve().parent.parent
proj = root.parent
brand = root / "assets/img/brand"; brand.mkdir(parents=True, exist_ok=True)
for f in (proj / "brand/logo").glob("*.svg"):
    shutil.copy(f, brand / f.name)
(root / "assets/img/people").mkdir(parents=True, exist_ok=True)
for slug in ("pat-hennelly", "iuliia-pakhomenko"):
    src = proj / f"assets/cutouts/{slug}-headshoulders.png"
    if not src.exists():
        print("missing", src); continue
    im = Image.open(src).convert("RGBA")
    im.thumbnail((900, 900))
    im.save(root / f"assets/img/people/{slug}.png", optimize=True)
(root / "tokens").mkdir(exist_ok=True)
shutil.copy(proj / "brand/brand-tokens.json", root / "tokens/brand-tokens.json")
print("synced")
