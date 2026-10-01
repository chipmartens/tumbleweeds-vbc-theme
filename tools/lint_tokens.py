#!/usr/bin/env python3
"""Token lint: lists px/rgba literals in app.scss outside the :root block. A literal in a block means a token is missing.
Allowed: 0, 1px hairlines, 2px outlines, 50%/100%, aspect ratios, transforms, grid fr templates."""
import re, sys, pathlib
src = pathlib.Path(__file__).resolve().parent.parent / "src/scss/app.scss"
txt = src.read_text()
start = txt.index(":root {")
depth, i = 0, start
while True:
    c = txt[i]
    if c == "{": depth += 1
    if c == "}":
        depth -= 1
        if depth == 0: break
    i += 1
body = txt[i + 1:]
hits = []
for n, line in enumerate(txt[:i + 1].count("\n") + 1 and body.split("\n"), 1):
    code = line.split("//")[0]
    if re.search(r"[^-\w](\d+(\.\d+)?px)", code) and not re.search(r"(^|[^\w-])(0|1|2)px", code.replace("1px solid", "").replace("2px", "")) is None:
        pass
    for m in re.finditer(r"(?<![\w.-])(-?\d+(?:\.\d+)?)px", code):
        v = float(m.group(1))
        if v in (0, 1, 2, -1): continue
        if "media" in code or "@include" in code and "media" in code: continue
        hits.append((n, code.strip()))
        break
    if re.search(r"rgba?\(", code) and "var(--" not in code.split("rgba")[0][-3:]:
        hits.append((n, code.strip()))
seen = set(); out = []
for n, c in hits:
    if (n, c) not in seen: seen.add((n, c)); out.append((n, c))
for n, c in out: print(f"{n:5} {c}")
print("literals:", len(out))
