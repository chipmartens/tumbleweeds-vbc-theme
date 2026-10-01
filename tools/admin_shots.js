// node tools/admin_shots.js <base-url> <out-dir>
// Logs in to a LOCAL Playground (admin / password) and screenshots the editor screens a volunteer uses.
const p = require('puppeteer-core'), fs = require('fs');
const base = (process.argv[2] || 'http://127.0.0.1:9410/').replace(/\/?$/, '/');
const out = process.argv[3] || '_qa/admin';
if (!/^http:\/\/(127\.0\.0\.1|localhost)/.test(base)) { console.error('local sites only'); process.exit(1); }
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await p.launch({ headless: 'new', executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  const pg = await b.newPage(); await pg.setViewport({ width: 1440, height: 1000 });
  const errs = [];
  pg.on('pageerror', e => errs.push('pageerror ' + e.message));
  pg.on('console', m => m.type() === 'error' && errs.push('console ' + m.text().slice(0, 160)));
  await pg.goto(base + 'wp-login.php', { waitUntil: 'networkidle0' });
  await pg.type('#user_login', 'admin'); await pg.type('#user_pass', 'password');
  await Promise.all([pg.waitForNavigation({ waitUntil: 'networkidle0' }), pg.click('#wp-submit')]);
  const ids = await pg.evaluate(async (base) => {
    const get = async (u) => (await (await fetch(base + u)).text());
    const t = await get('wp-admin/edit.php?post_type=page');
    const m = [...t.matchAll(/post=(\d+)&amp;action=edit[^>]*>([^<]+)<\/a>/g)].map(x => [x[1], x[2]]);
    const c = await get('wp-admin/edit.php?post_type=coach');
    const cm = [...c.matchAll(/post=(\d+)&amp;action=edit[^>]*>([^<]+)<\/a>/g)].map(x => [x[1], x[2]]);
    return { pages: m, coaches: cm };
  }, base);
  console.log(JSON.stringify(ids));
  const find = (list, name) => (list.find(x => x[1].includes(name)) || [])[0];
  const targets = [
    ['club-settings', 'wp-admin/admin.php?page=club-settings'],
    ['edit-home', `wp-admin/post.php?post=${find(ids.pages, 'Home')}&action=edit`],
    ['edit-fees', `wp-admin/post.php?post=${find(ids.pages, 'Fees')}&action=edit`],
    ['edit-coach', `wp-admin/post.php?post=${ids.coaches[0] && ids.coaches[0][0]}&action=edit`],
    ['menus', 'wp-admin/nav-menus.php'],
    ['pages-list', 'wp-admin/edit.php?post_type=page'],
  ];
  for (const [name, path] of targets) {
    await pg.goto(base + path, { waitUntil: 'networkidle0' });
    await new Promise(r => setTimeout(r, 1200));
    const h = await pg.evaluate(() => document.documentElement.scrollHeight);
    await pg.screenshot({ path: `${out}/${name}.png`, fullPage: false });
    await pg.screenshot({ path: `${out}/${name}-full.jpg`, type: 'jpeg', quality: 70, fullPage: true });
    const notices = await pg.evaluate(() => [...document.querySelectorAll('.notice-error, .error, .php-error, b')].filter(e => /warning|notice|fatal|deprecated/i.test(e.textContent)).map(e => e.textContent.slice(0, 120)));
    console.log(name, 'height', h, 'phpNotices', JSON.stringify(notices));
  }
  console.log('errors', JSON.stringify(errs));
  await b.close();
})();
