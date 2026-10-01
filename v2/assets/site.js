const nav=document.querySelector('.nav');if(!nav.dataset.solid){}
const onS=()=>nav.classList.toggle('is-scrolled',scrollY>40);addEventListener('scroll',onS,{passive:true});onS();
const menu=document.getElementById('menu');
document.querySelectorAll('.nav__menu').forEach(b=>b.addEventListener('click',()=>{const open=!b.hasAttribute('data-close');menu.classList.toggle('is-open',open);menu.setAttribute('aria-hidden',!open);document.body.style.overflow=open?'hidden':''}));
menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('is-open');document.body.style.overflow=''}));
if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver' in window){
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.reveal').forEach((el,i)=>{el.style.transitionDelay=((i%3)*60)+'ms';io.observe(el)});
}else{document.querySelectorAll('.reveal').forEach(el=>el.classList.add('is-in'))}
