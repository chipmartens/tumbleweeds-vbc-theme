// node tools/v2_shots.js [base] [outdir] [onlyslug...]  -> full-length JPEGs (split <=2400px), overflow + console + request check
const p=require('puppeteer-core'),fs=require('fs'),path=require('path');
const base=(process.argv[2]||'http://localhost:8981/').replace(/\/?$/,'/');const out=process.argv[3]||'v2/_review';const only=process.argv.slice(4);
const pages={home:'',coaches:'our-coaches/',pat:'coaches/pat-hennelly/',iuliia:'coaches/iuliia-pakhomenko/',programs:'programs/',tryouts:'tryouts/',fees:'fees-and-registration/',parents:'for-parents/',sponsors:'sponsors/',news:'news/','news-post':'news/what-we-will-publish-before-tryouts/','news-post2':'news/info-session/',contact:'contact/'};
(async()=>{fs.mkdirSync(out,{recursive:true});const b=await p.launch({headless:'new',executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
for(const [slug,pth] of Object.entries(pages)){if(only.length&&!only.includes(slug))continue;
 for(const [w,h,n] of [[1440,900,'d'],[390,844,'m']]){const pg=await b.newPage();await pg.setViewport({width:w,height:h,deviceScaleFactor:1});
  const errs=[];pg.on('console',m=>m.type()==='error'&&errs.push(m.text()));pg.on('requestfailed',r=>!/fonts\.g/.test(r.url())&&errs.push('FAIL '+r.url()));pg.on('response',r=>r.status()>=400&&errs.push(r.status()+' '+r.url()));
  await pg.goto(base+pth,{waitUntil:'networkidle0'});
  await pg.evaluate(async()=>{document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager');document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in'));for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}scrollTo(0,0)});
  await new Promise(r=>setTimeout(r,1200));
  const m=await pg.evaluate(()=>({ov:document.documentElement.scrollWidth-innerWidth,H:document.documentElement.scrollHeight,wide:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+1&&getComputedStyle(e).position!=='fixed'&&!e.closest('.strip,.ticker,.statement,.footer,.sheetmenu,.badge,.hero')}).slice(0,3).map(e=>e.className||e.tagName)}));
  const parts=Math.ceil(m.H/2400);for(let i=0;i<parts;i++){const f=`${out}/${slug}-${n}${parts>1?'-'+(i+1):''}.jpg`;await pg.screenshot({path:f,type:'jpeg',quality:72,captureBeyondViewport:true,clip:{x:0,y:i*2400,width:w,height:Math.min(2400,m.H-i*2400)}})}
  console.log(slug,n,'H',m.H,'overflow',m.ov,'wide',JSON.stringify(m.wide),'errs',JSON.stringify(errs));await pg.close()}}
await b.close()})();
