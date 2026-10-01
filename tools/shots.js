#!/usr/bin/env node
// Full-page screenshots at 390 and 1440 plus checks (horizontal scroll, console errors, failed requests, fonts).
// usage: node tools/shots.js [baseUrl] [outDir]   (default http://127.0.0.1:9400 and screenshots/)
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');
const base = (process.argv[2] || 'http://127.0.0.1:9400').replace(/\/$/, '');
const out = path.resolve(process.argv[3] || path.join(__dirname, '..', 'screenshots'));
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const pages = ['', 'our-coaches', 'coaches/pat-hennelly', 'programs', 'tryouts', 'fees-and-registration', 'for-parents', 'sponsors', 'news', 'info-session-sunday-october-4', 'contact'];
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new' });
  const report = [];
  for (const w of [390, 1440]) {
    for (const p of pages) {
      const pg = await b.newPage();
      await pg.setViewport({ width: w, height: w === 390 ? 844 : 900, deviceScaleFactor: 1 });
      const errs = [], failed = [];
      pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
      pg.on('requestfailed', r => failed.push(r.url()));
      pg.on('response', r => { if (r.status() >= 400) failed.push(r.status() + ' ' + r.url()); });
      await pg.goto(`${base}/${p}${p ? '/' : ''}`, { waitUntil: 'networkidle0', timeout: 60000 });
      await pg.evaluate(async () => { await document.fonts.ready; for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); } window.scrollTo(0, 0); });
      await pg.waitForNetworkIdle({ idleTime: 400 });
      const m = await pg.evaluate(() => ({
        overflow: document.documentElement.scrollWidth - window.innerWidth,
        fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight),
        h1: (document.querySelector('h1') || {}).innerText,
        title: document.title,
      }));
      const name = (p || 'home').replace(/\//g, '-') + '-' + w + '.png';
      await pg.screenshot({ path: path.join(out, name), fullPage: true });
      report.push({ page: p || 'home', w, overflow: m.overflow, errs, failed, h1: m.h1, fonts: m.fonts.length });
      await pg.close();
    }
  }
  await b.close();
  fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 2));
  for (const r of report) console.log(r.w, r.page.padEnd(26), 'overflow', r.overflow, 'errs', r.errs.length, 'failed', r.failed.length, 'fonts', r.fonts);
})();
