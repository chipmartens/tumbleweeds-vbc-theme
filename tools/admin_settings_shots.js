// node tools/admin_settings_shots.js <local-url> <out-dir>  Club settings, every new tab, at 1440 and 390 (local Playground only).
const p = require('puppeteer-core'), fs = require('fs');
const base = (process.argv[2] || 'http://127.0.0.1:9420/').replace(/\/?$/, '/'), out = process.argv[3] || '_qa/admin';
if (!/^http:\/\/(127\.0\.0\.1|localhost)/.test(base)) process.exit(1);
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await p.launch({ headless: 'new', executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  const pg = await b.newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message));
  await pg.setViewport({ width: 1440, height: 1000 });
  await pg.goto(base + 'wp-login.php', { waitUntil: 'load', timeout: 120000 });
  await pg.type('#user_login', 'admin'); await pg.type('#user_pass', 'password');
  await Promise.all([pg.waitForNavigation({ waitUntil: 'load', timeout: 120000 }), pg.click('#wp-submit')]);
  for (const [w, h, n] of [[1440, 1000, 'd'], [390, 900, 'm']]) {
    await pg.setViewport({ width: w, height: h });
    await pg.goto(base + 'wp-admin/admin.php?page=club-settings', { waitUntil: 'load', timeout: 120000 });
    await new Promise(r => setTimeout(r, 2500));
    for (const tab of ['Registration', 'Contact and social', 'Footer', 'Other wording', 'Sharing and analytics']) {
      await pg.evaluate(t => { [...document.querySelectorAll('.acf-tab-button')].find(a => a.textContent.trim() === t)?.click(); }, tab);
      await new Promise(r => setTimeout(r, 500));
      await pg.screenshot({ path: `${out}/settings-${tab.toLowerCase().replace(/ /g, '-')}-${n}.png` });
    }
  }
  console.log('errors', JSON.stringify(errs)); await b.close();
})();
