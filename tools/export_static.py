#!/usr/bin/env python3
"""Static snapshot of the running site into preview/ (relative links, works from file:// and GitHub Pages).
usage: python3 tools/export_static.py [http://127.0.0.1:9400]"""
import json, re, sys, pathlib, shutil, urllib.request, urllib.parse
base = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:9400").rstrip("/")
root = pathlib.Path(__file__).resolve().parent.parent
out = root / "preview"
shutil.rmtree(out, ignore_errors=True); out.mkdir()
seed = json.load(open(root / "seed/content.json"))
paths = [""] + [p["slug"] for p in seed["pages"] if not p.get("front_page")] + ["coaches/" + c["slug"] for c in seed["coaches"][:2]] + [p["slug"] for p in seed["posts"]]
get = lambda u: urllib.request.urlopen(u).read()
theme = "wp-content/themes/tumbleweeds-vbc/"
assets = set()

def rel(depth): return "../" * depth

for p in paths:
    html = get(f"{base}/{p}{'/' if p else ''}").decode()
    depth = len([x for x in p.split("/") if x])
    pre = rel(depth)
    html = re.sub(r'<link[^>]+(wp-json|xmlrpc|EditURI|shortlink|canonical)[^>]*>\s*', "", html)
    html = re.sub(r'<meta name="robots"[^>]*>', '<meta name="robots" content="noindex">', html)
    def sub(m):
        attr, url = m.group(1), m.group(2)
        path = url[len(base):].lstrip("/").split("#")[0].split("?")[0]
        frag = ("#" + url.split("#")[1]) if "#" in url else ""
        if path.startswith("wp-content/") or path.startswith("wp-includes/"):
            assets.add(path); return f'{attr}="{pre}{path}{frag}"'
        return f'{attr}="{pre}{path}{"/" if path else ""}index.html{frag}"'
    html = re.sub(r'(href|src)=["\'](' + re.escape(base) + r'[^"\']*)["\']', sub, html)
    def srcset(m):
        parts = []
        for item in m.group(1).split(","):
            u, *w = item.strip().split(" ")
            path = u[len(base):].lstrip("/"); assets.add(path); parts.append(pre + path + (" " + w[0] if w else ""))
        return 'srcset="' + ", ".join(parts) + '"'
    html = re.sub(r'srcset="([^"]+)"', srcset, html)
    html = re.sub(r'<script[^>]*wp-includes[^>]*></script>', "", html)
    d = out / p; d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html)
# theme assets straight from disk (css, js, fonts, img); uploads over HTTP
for sub in ("assets",):
    shutil.copytree(root / sub, out / theme / sub)
for a in sorted(assets):
    if a.startswith(theme):
        continue
    f = out / a; f.parent.mkdir(parents=True, exist_ok=True)
    try: f.write_bytes(get(f"{base}/{a}"))
    except Exception as e: print("skip", a, e)
# file:// blocks CSS masks from separate files, so inline the mark into the preview CSS
import base64
css = out / theme / "assets/css/app.min.css"
mark = base64.b64encode((root / "assets/img/brand/tumbleweeds-mark.svg").read_bytes()).decode()
css.write_text(css.read_text().replace("../img/brand/tumbleweeds-mark.svg", "data:image/svg+xml;base64," + mark))
print("exported", len(paths), "pages,", len(assets), "assets ->", out)
