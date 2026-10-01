// node tools/make_pdf.js docs/launch-guide.md  (needs pandoc) -> docs/launch-guide.pdf, printed by headless Chrome
const { execSync } = require('child_process'), p = require('puppeteer-core'), fs = require('fs'), path = require('path');
const md = path.resolve(process.argv[2]), out = md.replace(/\.md$/, '.pdf'), html = md.replace(/\.md$/, '.tmp.html');
const css = `<style>@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;600&display=swap');
body{font:11pt/1.5 Figtree,sans-serif;color:#172111;max-width:none;margin:0}h1{font-size:24pt;margin:0 0 8pt}h2{font-size:15pt;margin:20pt 0 6pt;border-top:2px solid #c8963e;padding-top:10pt}
table{border-collapse:collapse;width:100%;margin:8pt 0}td,th{border:1px solid #d9cfbd;padding:5pt 7pt;text-align:left;vertical-align:top;font-size:10pt}th{background:#f3ebdf}
code{background:#f3ebdf;padding:1pt 3pt;font-size:9.5pt}a{color:#172111}ul.task-list{list-style:none;padding-left:4pt}h2,table,li{break-inside:avoid}</style>`;
execSync(`pandoc "${md}" -f gfm -t html5 -s --metadata title="Launching the Tumbleweeds website" -H /dev/stdin -o "${html}"`, { input: css });
(async () => {
  const b = await p.launch({ headless: 'new', executablePath: process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  const pg = await b.newPage(); await pg.goto('file://' + html, { waitUntil: 'networkidle0' });
  await pg.pdf({ path: out, format: 'Letter', margin: { top: '0.7in', bottom: '0.7in', left: '0.8in', right: '0.8in' }, printBackground: true });
  await b.close(); fs.unlinkSync(html); console.log(out);
})();
