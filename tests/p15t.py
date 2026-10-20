import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1300})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const W=G.settlers.filter(s=>s.room&&s.ec0!=null); const st=W.map(s=>[s.ec0,s.idn0]);
      const at=d=>{ for(let i=0;i<d;i++){ G.day++; C.jobDriftDay(); } return W.map((s,i)=>Math.hypot(s.ec0-st[i][0],s.idn0-st[i][1])); };
      const q=a=>{ const x=a.slice().sort((p,q)=>p-q); return [.25,.5,.75,.95].map(f=>x[Math.floor(f*(x.length-1))].toFixed(2)).join('/'); };
      const a1=at(36), a2=at(72), a3=at(180); return 'n '+W.length+' | moved after 2y '+q(a1)+' | 6y '+q(a2)+' | 16y '+q(a3); }"""))
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const o=G.settlers.find(s=>s.pol==='officer'); if(!o) return 'no officer'; o.waiting=true; o.intake=null; C.UI.modal={t:'settler',id:o.id}; C.renderUI(); const b=document.querySelector('[data-a=polPatrol]'); if(!b) return 'no button'; b.click(); return 'after click waiting '+o.waiting+' room '+o.room+' | '+G.log[0].m; }"""))
    print(errs[:5]); await b.close()
asyncio.run(main())
