// Siti in JavaScript dei promotori rimasti su Facebook: home e fino a due pagine eventi aperte con Chromium,
// testo visibile salvato nello scratch. robots.txt rispettato (User-agent * e il nostro), un host alla volta per pagina.
const {chromium}=require('playwright'); const fs=require('fs'); const zlib=require('zlib');
const S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad';
const UA='QuartieriNews-fonti/1.0 (+https://github.com/quartierinews/qn; contatto: redazione)';
const hosts=JSON.parse(fs.readFileSync(S+'/canali/dinamici.json'));
const roots=JSON.parse(fs.readFileSync(S+'/canali/dinamici_root.json'));
const KW=/event|calendar|agenda|programm|appuntament|cartellon|stagion|spettacol|concert|mostre|rassegn|news|notizi|attivit|iniziativ/i;
async function robots(origin){
  try{const r=await fetch(origin+'/robots.txt',{headers:{'User-Agent':UA}});
    if(r.status===401||r.status===403) return ()=>false;
    if(!r.ok) return ()=>true;
    const t=await r.text(); let on=false; const dis=[];
    for(const raw of t.split(/\r?\n/)){const l=raw.replace(/#.*/,'').trim(); const m=l.match(/^([A-Za-z-]+)\s*:\s*(.*)$/); if(!m) continue;
      const k=m[1].toLowerCase(), v=m[2].trim();
      if(k==='user-agent') on=(v==='*'||/quartierinews/i.test(v)); else if(on&&k==='disallow'&&v) dis.push(v);}
    return u=>{const p=new URL(u).pathname; return !dis.some(d=>p.startsWith(d.replace(/\*.*$/,'')));};
  }catch(e){return ()=>true;}
}
(async()=>{
  const b=await chromium.launch(); const out=[];
  const ctx=await b.newContext({userAgent:UA});
  let i=0;
  async function one(h){
    const root=roots[h]; const res={host:h,docs:[],errori:[],robots_vieta:0,giro:'browser'};
    const ok=await robots(new URL(root).origin);
    await new Promise(r=>setTimeout(r,1000));   // una richiesta al secondo per sito, anche fra robots.txt e la prima pagina
    const page=await ctx.newPage(); let rifiuto=false;
    async function open(u,kind){
      if(rifiuto) return null;
      if(!ok(u)){res.robots_vieta++; return null;}
      let resp=null;
      try{resp=await page.goto(u,{waitUntil:'networkidle',timeout:30000});}catch(e){try{await page.waitForTimeout(3000);}catch(_){}}
      const st=resp?resp.status():0;
      if(st===401||st===403){rifiuto=true; res.errori.push([kind,u,'HTTP '+st+': rifiuto, non si aggira']); return null;}   // niente testo, niente link, niente altre pagine
      try{const t=await page.evaluate(()=>document.body?document.body.innerText:''); 
          const ld=await page.evaluate(()=>[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>s.textContent));
          const links=await page.evaluate(()=>[...document.querySelectorAll('a[href]')].map(a=>[a.href,(a.innerText||'').slice(0,60)]));
          res.docs.push({kind,url:u,testo:t.replace(/\s+/g,' ').slice(0,150000),ld}); await new Promise(r=>setTimeout(r,1000)); return links;}
      catch(e){res.errori.push([kind,u,String(e).slice(0,80)]); return null;}
    }
    const links=await open(root,'home');
    if(links){
      const host=new URL(root).host; const cand=[...new Set(links.filter(([u,t])=>{try{return new URL(u).host===host&&(KW.test(new URL(u).pathname)||KW.test(t))&&u.split('#')[0].replace(/\/$/,'')!==root.replace(/\/$/,'');}catch(e){return false;}}).map(x=>x[0].split('#')[0]))];
      for(const u of cand.slice(0,2)) await open(u,'pagina');
    }
    await page.close(); out.push(JSON.stringify(res));
  }
  const queue=[...hosts]; const workers=Array.from({length:4},async()=>{while(queue.length){const h=queue.shift(); try{await one(h);}catch(e){out.push(JSON.stringify({host:h,docs:[],errori:[['crash','',String(e).slice(0,100)]],robots_vieta:0,giro:'browser'}));} if(++i%10===0) console.log(i,'host');}});
  await Promise.all(workers); await b.close();
  fs.writeFileSync(S+'/canali/pagine3.jsonl.gz',zlib.gzipSync(out.join('\n')+'\n')); console.log('fine',out.length);
})();
