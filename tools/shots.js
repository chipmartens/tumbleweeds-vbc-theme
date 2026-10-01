// node tools/shots.js <base-url> <out-dir> [slug ...]
// Full-length JPEGs of every page at 1440 and 390 (split into parts of 2400px), plus overflow, console and request checks.
// Works on the WordPress site and on the static v2 site (same paths). Example:
//   POSTBASE= node tools/shots.js http://127.0.0.1:9410/ _qa/wp
//   node tools/shots.js http://localhost:8981/ _qa/v2
const p = require('puppeteer-core'), fs = require('fs');
const base = (process.argv[2] || 'http://127.0.0.1:9410/').replace(/\/?$/, '/');
const out = process.argv[3] || '_qa/wp';
const only = process.argv.slice(4);
// WordPress keeps news posts at /<slug>/ (permalinks /%postname%/); the static v2 keeps them under /news/<slug>/. POSTBASE='' for WordPress.
const postBase = process.env.POSTBASE === undefined ? 'news/' : process.env.POSTBASE;
const pages = { home: '', coaches: 'our-coaches/', pat: 'coaches/pat-hennelly/', iuliia: 'coaches/iuliia-pakhomenko/', programs: 'programs/', tryouts: 'tryouts/', fees: 'fees-and-registration/', parents: 'for-parents/', sponsors: 'sponsors/', news: 'news/', 'news-post': postBase + 'what-we-will-publish-before-tryouts/', 'news-post2': postBase + 'info-session/', contact: 'contact/', privacy: 'privacy-policy/', e404: 'zzz-not-here/' };
const chrome = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await p.launch({ headless: 'new', executablePath: chrome });
  const report = [];
  for (const [slug, pth] of Object.entries(pages)) {
    if (only.length && !only.includes(slug)) continue;
    for (const [w, h, n] of [[1440, 900, 'd'], [390, 844, 'm']]) {
      const pg = await b.newPage();
      await pg.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
      const errs = [];
      pg.on('console', m => { if (m.type() === 'error' && !/404 \(Not Found\)/.test(m.text())) errs.push('console: ' + m.text()); });
      pg.on('pageerror', e => errs.push('pageerror: ' + e.message));
      pg.on('requestfailed', r => !/fonts\.g|googletagmanager/.test(r.url()) && errs.push('FAIL ' + r.url()));
      pg.on('response', r => { if (r.status() >= 400 && slug !== 'e404' || (r.status() >= 400 && r.url() !== base + pth)) errs.push(r.status() + ' ' + r.url()); });
      await pg.goto(base + pth, { waitUntil: 'networkidle0' });
      await pg.evaluate(async () => {
        document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager');
        document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in'));
        for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); }
        scrollTo(0, 0);
      });
      await new Promise(r => setTimeout(r, 1500));
      const m = await pg.evaluate(() => ({
        ov: document.documentElement.scrollWidth - innerWidth,
        H: document.documentElement.scrollHeight,
        hidden: [...document.querySelectorAll('.fade-up')].filter(e => parseFloat(getComputedStyle(e).opacity) < 0.99).length,
        unloaded: [...document.querySelectorAll('img.lazyload:not(.lazyloaded)')].length,
        wide: [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.right > innerWidth + 1 && getComputedStyle(e).position !== 'fixed' && !e.closest('.strip,.ticker,.statement,.site-footer,.drawer,.hero__badge,.hero,.footer,.sheetmenu,.badge'); }).slice(0, 3).map(e => e.className || e.tagName)
      }));
      const parts = Math.ceil(m.H / 2400);
      for (let i = 0; i < parts; i++) {
        const f = `${out}/${slug}-${n}${parts > 1 ? '-' + (i + 1) : ''}.jpg`;
        await pg.screenshot({ path: f, type: 'jpeg', quality: 78, captureBeyondViewport: true, clip: { x: 0, y: i * 2400, width: w, height: Math.min(2400, m.H - i * 2400) } });
      }
      const line = `${slug} ${n} H ${m.H} overflow ${m.ov} hiddenReveals ${m.hidden} unloadedImgs ${m.unloaded} wide ${JSON.stringify(m.wide)} errs ${JSON.stringify(errs)}`;
      console.log(line); report.push(line);
      await pg.close();
    }
  }
  fs.writeFileSync(`${out}/report.txt`, report.join('\n') + '\n');
  await b.close();
})();
