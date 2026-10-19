(function(){
  const THEME_KEY='ailab-theme-v1';
  const GREEN_KEY='ailab-green-v1';
  const themeEl=document.getElementById('theme');
  const saved=localStorage.getItem(THEME_KEY)||'aurora';
  document.documentElement.setAttribute('data-theme',saved);
  themeEl.value=saved;
  themeEl.addEventListener('change',()=>{
    document.documentElement.setAttribute('data-theme',themeEl.value);
    localStorage.setItem(THEME_KEY,themeEl.value);
  });

  const items=[
    'I ran labs 01–03',
    'I opened at least one labs/artifacts/*.json',
    'I opened labs/reports/golden10-report.md',
    'I can explain Run without notes',
    'I can explain Trace without notes',
    'I can explain Metric without notes',
    'I can explain Artifact without notes',
    'I can state a falsifier for "model is smart enough"',
    'I know mock vs Ollama honesty',
    'I know why tool schema beats invented math',
    'I know what never goes in git',
    'I can map LICC → RTMA in one sentence',
    'I will not delete the UC free pack for this project'
    ,'I ran the RAG ablation and inspected the wrong-neighbor risk'
    ,'I saw the bounded agent fail, correct, verify, and stop'
    ,'I can isolate voice STT, model/tools, TTS, and transport latency'
    ,'I scheduled reviews at 1h, 24h, 7d, 30d, and 90d'
  ];
  const box=document.getElementById('checks');
  let state={};
  try{state=JSON.parse(localStorage.getItem(GREEN_KEY)||'{}')}catch(e){state={}}
  function render(){
    box.innerHTML='';
    let on=0;
    items.forEach((t,i)=>{
      const id='g'+i;
      const checked=!!state[id];
      if(checked) on++;
      const row=document.createElement('div');
      row.className='check';
      row.innerHTML=`<input type="checkbox" id="${id}" ${checked?'checked':''}/><label for="${id}">${t}</label>`;
      box.appendChild(row);
      row.querySelector('input').addEventListener('change',e=>{
        state[id]=e.target.checked;
        localStorage.setItem(GREEN_KEY,JSON.stringify(state));
        render();
      });
    });
    document.getElementById('greenCount').textContent=on+' / '+items.length;
    document.getElementById('greenBar').style.width=((on/items.length)*100)+'%';
  }
  render();
  document.getElementById('btnResetGreen').onclick=()=>{state={};localStorage.removeItem(GREEN_KEY);render()};

  // search
  const q=document.getElementById('q');
  function applySearch(){
    const term=(q.value||'').trim().toLowerCase();
    document.querySelectorAll('[data-search], .q-item, .section, .hero').forEach(el=>{
      if(!term){el.classList.remove('hidden');return;}
      const hay=((el.getAttribute('data-search')||'')+' '+el.textContent).toLowerCase();
      el.classList.toggle('hidden',!hay.includes(term));
    });
  }
  q.addEventListener('input',applySearch);
  document.addEventListener('keydown',e=>{
    if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();q.focus();q.select()}
  });

  const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches; document.documentElement.setAttribute('data-motion', reduceMotion?'reduce':'full'); document.getElementById('btnTop').onclick=()=>window.scrollTo({top:0,behavior:reduceMotion?'auto':'smooth'});
  let focus=false;
  document.getElementById('btnFocus').onclick=()=>{
    focus=!focus;
    document.getElementById('side').style.display=focus?'none':'';
    document.querySelector('.layout').style.gridTemplateColumns=focus?'1fr':'var(--side) 1fr';
  };

  // active nav
  const navs=[...document.querySelectorAll('.side a.nav[href^="#"]')];
  const map=navs.map(a=>({a,id:a.getAttribute('href').slice(1)}));
  function syncNav(){
    let cur='home';
    map.forEach(({id})=>{
      const el=document.getElementById(id);
      if(el && el.getBoundingClientRect().top<120) cur=id;
    });
    navs.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+cur));
  }
  window.addEventListener('scroll',syncNav,{passive:true});
  syncNav();
})();
