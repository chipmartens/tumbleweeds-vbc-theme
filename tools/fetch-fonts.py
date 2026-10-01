#!/usr/bin/env python3
"""Download the latin subset of Barlow + Barlow Condensed (OFL) into assets/fonts and print the @font-face CSS.
Run once; the woff2 files are committed so the theme works offline."""
import re, urllib.request, pathlib
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
URL = "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&display=swap"
req = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA})).read()
css = req(URL).decode()
out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "fonts"
out.mkdir(parents=True, exist_ok=True)
faces = []
for block in re.findall(r"/\* (\S+) \*/\s*(@font-face \{.*?\})", css, re.S):
    subset, face = block
    if subset != "latin":
        continue
    fam = re.search(r"font-family: '([^']+)'", face).group(1)
    wt = re.search(r"font-weight: (\d+)", face).group(1)
    url = re.search(r"url\((https[^)]+)\)", face).group(1)
    fn = f"{fam.lower().replace(' ', '-')}-{wt}.woff2"
    (out / fn).write_bytes(req(url))
    faces.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};font-display:swap;src:url('../fonts/{fn}') format('woff2');}}")
print("\n".join(faces))
