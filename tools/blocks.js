// node tools/blocks.js <slug> [width]  : heights of every top-level block on WordPress vs v2, to find where a page drifts.
const p = require('puppeteer-core');
const slug = process.argv[2] || '', w = +(process.argv[3] || 390);
const sels = 'body > header.hero, body > header.phero, body > .ticker, main > *, body > .band, body > footer, body > .footer';
(async () => {
  const b = await p.launch({ headless: 'new', executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  const out = {};
  for (const [k, base] of [['wp', 'http://127.0.0.1:9410/'], ['v2', 'http://localhost:8981/']]) {
    const pg = await b.newPage(); await pg.setViewport({ width: w, height: 900 });
    await pg.goto(base + slug, { waitUntil: 'networkidle0' });
    out[k] = await pg.evaluate(s => [...document.querySelectorAll(s)].map(e => ({ c: (e.className || e.tagName).toString().split(' ').slice(0, 2).join('.'), h: Math.round(e.getBoundingClientRect().height) })), sels);
    await pg.close();
  }
  const n = Math.max(out.wp.length, out.v2.length);
  for (let i = 0; i < n; i++) { const a = out.wp[i] || {}, c = out.v2[i] || {}; console.log(String(i).padStart(2), (a.c || '').padEnd(28), String(a.h).padStart(5), (c.c || '').padEnd(28), String(c.h).padStart(5), a.h - c.h ? '  <-- ' + (a.h - c.h) : ''); }
  await b.close();
})();
