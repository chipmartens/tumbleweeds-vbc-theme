const p=require('puppeteer-core');const base='http://localhost:8981/';
(async()=>{const b=await p.launch({headless:'new',executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const pg=await b.newPage();
// nav widths
for(const w of [1440,1280,1100,1024,768,390]){await pg.setViewport({width:w,height:800});await pg.goto(base+'tryouts/',{waitUntil:'networkidle0'});
 const r=await pg.evaluate(()=>{const n=document.querySelector('.nav');const k=[...n.children].filter(e=>getComputedStyle(e).display!=='none');const last=k[k.length-1].getBoundingClientRect();return {navOver:n.scrollWidth-n.clientWidth,lastRight:Math.round(last.right),vw:innerWidth,docOver:document.documentElement.scrollWidth-innerWidth,overlap:(()=>{let o=0;for(let i=1;i<k.length;i++)if(k[i].getBoundingClientRect().left<k[i-1].getBoundingClientRect().right-1)o++;return o})()}});console.log('nav',w,JSON.stringify(r));
 if(w===1100||w===390)await pg.screenshot({path:`v2/_review/nav-${w}.jpg`,type:'jpeg',clip:{x:0,y:0,width:w,height:140}})}
// crawl
const seen=new Set(),q=[base],bad=[];
while(q.length){const u=q.shift();if(seen.has(u))continue;seen.add(u);const res=await pg.goto(u,{waitUntil:'domcontentloaded'});if(res.status()>=400){bad.push(res.status()+' '+u);continue}
 const l=await pg.evaluate(()=>[...document.querySelectorAll('a[href],img[src],link[href],script[src]')].map(e=>e.href||e.src));
 for(const x of l){if(!x.startsWith(base))continue;const c=x.split('#')[0];if(/\.html$|\/$/.test(c)){q.push(c)}else if(!seen.has(c)){seen.add(c);const r=await pg.goto(c).catch(()=>null);if(!r||r.status()>=400)bad.push('asset '+c)}}}
console.log('crawled',[...seen].filter(x=>/\/$|html$/.test(x)).length,'bad',JSON.stringify(bad));await b.close()})();
