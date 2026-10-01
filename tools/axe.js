// node tools/axe.js <base-url>   Runs axe-core on every page at 1440 and 390. Prints serious/critical counts and each violation.
const p = require('puppeteer-core'), axe = require('axe-core');
const base = (process.argv[2] || 'http://127.0.0.1:9420/').replace(/\/?$/, '/');
const pages = ['', 'our-coaches/', 'coaches/pat-hennelly/', 'coaches/iuliia-pakhomenko/', 'programs/', 'tryouts/', 'fees-and-registration/', 'for-parents/', 'sponsors/', 'news/', 'what-we-will-publish-before-tryouts/', 'info-session/', 'contact/', 'privacy-policy/', 'zzz-not-here/'];
const chrome = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async () => {
  const b = await p.launch({ headless: 'new', executablePath: chrome });
  let total = 0; const all = [];
  for (const pth of pages) for (const w of [1440, 390]) {
    const pg = await b.newPage(); await pg.setViewport({ width: w, height: 900 });
    await pg.goto(base + pth, { waitUntil: 'load', timeout: 120000 });
    await pg.evaluate(async () => { document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); document.querySelectorAll('.fade-up').forEach(e => { e.style.opacity = 1; e.style.transform = 'none'; }); });
    await new Promise(r => setTimeout(r, 1200));
    await pg.evaluate(axe.source);
    const r = await pg.evaluate(() => axe.run(document, { resultTypes: ['violations'] }));
    const bad = r.violations.filter(v => ['serious', 'critical'].includes(v.impact));
    total += bad.reduce((n, v) => n + v.nodes.length, 0);
    for (const v of bad) all.push(`${pth || 'home'} @${w} ${v.impact} ${v.id} x${v.nodes.length}: ${v.nodes.slice(0, 2).map(n => n.target.join(' ')).join(' | ')}`);
    await pg.close();
  }
  console.log(all.join('\n')); console.log('SERIOUS+CRITICAL nodes:', total);
  await b.close();
})();
