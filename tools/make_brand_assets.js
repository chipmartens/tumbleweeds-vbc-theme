// node tools/make_brand_assets.js
// Renders the sharing picture (1200x630) and the favicon set from the traced mark with headless Chrome.
// Outputs go to src/img (then `npm run build` copies them to assets/img).
const p = require('puppeteer-core'), fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '..');
const chrome = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const mark = f => 'file://' + path.join(root, 'src/img', f);
const social = `<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600&family=Figtree:wght@400;500;600&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0}
body{width:1200px;height:630px;background:#172111;color:#f3ebdf;font-family:Figtree,sans-serif;position:relative;overflow:hidden}
.wreath{position:absolute;right:-150px;top:-60px;width:760px;opacity:.1}
.logo{position:absolute;left:72px;top:64px;display:flex;align-items:center;gap:20px}
.logo img{width:72px;height:72px}
.logo span{font:600 34px/1 "Barlow Condensed",sans-serif;letter-spacing:.06em;text-transform:uppercase}
h1{position:absolute;left:72px;bottom:150px;width:760px;font:500 84px/0.98 Figtree,sans-serif;letter-spacing:-2.4px}
h1 em{font:italic 400 92px/0.98 "Instrument Serif",serif;color:#d6a650;letter-spacing:-1px}
.foot{position:absolute;left:72px;bottom:64px;display:flex;gap:16px;align-items:center;font:500 22px/1 Figtree,sans-serif;color:rgba(243,235,223,.75)}
.dot{width:10px;height:10px;border-radius:50%;background:#c8963e}
</style>
<img class="wreath" src="${mark('tumbleweeds-official-mark-reverse.svg')}">
<div class="logo"><img src="${mark('tumbleweeds-official-mark-reverse.svg')}"><span>Tumbleweeds</span></div>
<h1>Developing athletes from the <em>ground up.</em></h1>
<div class="foot"><span class="dot"></span>Kamloops youth volleyball club</div>`;
const icon = (bg, pad) => `<!doctype html><style>*{margin:0}body{width:512px;height:512px;background:${bg};display:grid;place-items:center}img{width:${pad}%}</style><img src="${mark('tumbleweeds-official-mark-reverse.svg')}">`;
(async () => {
  const b = await p.launch({ headless: 'new', executablePath: chrome });
  const shot = async (html, w, h, out, type, scale = 1) => {
    const pg = await b.newPage(); await pg.setViewport({ width: w, height: h, deviceScaleFactor: scale });
    const tmp = path.join(root, 'tools', '_tmp.html'); fs.writeFileSync(tmp, html);
    await pg.goto('file://' + tmp, { waitUntil: 'networkidle0' }); await pg.evaluate(() => document.fonts.ready);
    await pg.screenshot({ path: path.join(root, 'src/img', out), type, ...(type === 'jpeg' ? { quality: 88 } : {}) });
    await pg.close(); fs.unlinkSync(tmp);
  };
  await shot(social, 1200, 630, 'tumbleweeds-social.jpg', 'jpeg');
  // icons: pine tile with the reverse mark. 512 and 192 are full tiles; 180 (apple touch) and 32 (tab) scaled from the same artwork.
  for (const [n, size] of [['icon-512.png', 512], ['icon-192.png', 192], ['apple-touch-icon.png', 180], ['favicon-32.png', 32]]) {
    const html = icon('#172111', size <= 32 ? 84 : 70).replace('512px', size + 'px').replace('512px', size + 'px');
    await shot(html, size, size, n, 'png');
  }
  await b.close();
})();
