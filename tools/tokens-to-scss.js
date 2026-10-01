#!/usr/bin/env node
// Rewrites the :root block in src/scss/app.scss (between the tokens:start / tokens:end markers)
// from tokens/brand-tokens.json. Change a token in the JSON, run `npm run tokens`, never edit the block by hand.
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const t = JSON.parse(fs.readFileSync(path.join(root, 'tokens/brand-tokens.json'), 'utf8'));
const L = [];
for (const [k, v] of Object.entries(t.color)) L.push(`--${k}: ${v.hex};`);
L.push(`--font-display: '${t.type.display.family}', 'Arial Narrow', sans-serif;`);
L.push(`--font-body: '${t.type.body.family}', system-ui, sans-serif;`);
for (const [k, v] of Object.entries(t.type.scale_px)) L.push(`--step-${k}: ${v}px;`);
for (const [k, v] of Object.entries(t.type.line_height)) L.push(`--lh-${k}: ${v};`);
for (const [k, v] of Object.entries(t.type.tracking)) L.push(`--tracking-${k}: ${v};`);
for (const [k, v] of Object.entries(t.space_px)) L.push(`--space-${k}: ${v}px;`);
for (const [k, v] of Object.entries(t.radius_px)) L.push(`--radius-${k}: ${v}px;`);
L.push(`--max-width: ${t.layout.max_width_px}px;`);
L.push(`--gutter-mobile: ${t.layout.gutter_mobile_px}px;`);
L.push(`--gutter-desktop: ${t.layout.gutter_desktop_px}px;`);
L.push(`--measure: ${t.layout.measure_ch}ch;`);
const block = `/* tokens:start (generated from tokens/brand-tokens.json by tools/tokens-to-scss.js, do not edit) */\n:root {\n  ${L.join('\n  ')}\n}\n/* tokens:end */`;
const f = path.join(root, 'src/scss/app.scss');
let s = fs.readFileSync(f, 'utf8');
const re = /\/\* tokens:start[\s\S]*?\/\* tokens:end \*\//;
if (!re.test(s)) { console.error('markers missing in app.scss'); process.exit(1); }
fs.writeFileSync(f, s.replace(re, block));
console.log('tokens written:', L.length);
