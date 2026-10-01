// node tools/crawl.js <base-url>
// Follows every internal link, image and script from the home page. Prints each non-200 and the totals.
const base = (process.argv[2] || 'http://127.0.0.1:9410/').replace(/\/?$/, '/');
const origin = new URL(base).origin;
const seen = new Set(), queue = [base], bad = [], assets = new Set();
const abs = (u, from) => { try { return new URL(u, from).href.split('#')[0]; } catch (e) { return null; } };
(async () => {
  let pages = 0;
  while (queue.length) {
    const u = queue.shift(); if (seen.has(u)) continue; seen.add(u);
    const r = await fetch(u, { redirect: 'follow' }); pages++;
    if (r.status !== 200) { bad.push(r.status + ' ' + u); continue; }
    const html = await r.text();
    for (const m of html.matchAll(/(?:href|src|data-src)=["']([^"']+)["']/g)) {
      const a = abs(m[1], u); if (!a || !a.startsWith(origin) || /^(mailto|tel):/.test(m[1])) continue;
      if (/\.(css|js|svg|png|jpe?g|webp|gif|woff2?)(\?|$)/i.test(a)) assets.add(a);
      else if (!/wp-(admin|login|json)|xmlrpc|feed|\?/.test(a)) queue.push(a);
    }
    for (const m of html.matchAll(/(?:data-srcset|srcset)=["']([^"']+)["']/g)) for (const s of m[1].split(',')) { const a = abs(s.trim().split(' ')[0], u); if (a && a.startsWith(origin)) assets.add(a); }
  }
  for (const a of assets) { const r = await fetch(a); if (r.status !== 200) bad.push(r.status + ' asset ' + a); }
  console.log('pages', pages, 'assets', assets.size, 'bad', JSON.stringify(bad));
})();
