import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps=1e5;
      const t=G.rooms.find(r=>r.type==='trade'); const j=Object.assign(JSON.parse(JSON.stringify(t)),{id:8888,col:3,type:'jail'}); G.rooms.push(j);
      const LK=G.settlers[0].look; const mk=(i)=>({id:7000+i,s:{first:'Pris'+i,last:'X',sex:'M',born:G.day-400,s:{S:5,P:5,E:5,C:5,I:5,A:5,L:5},look:LK},tier:1,day:G.day,room:8888,from:'Rust Jackals'});
      G.settlers.filter(s=>s.bd==null).slice(0,2).forEach(s=>s.room=8888); const res={held:0,broke:0}; const n0=G.settlers.length;
      for(let k=0;k<60;k++){ G.captives=[mk(1),mk(2),mk(3),mk(4)]; G.settlers.forEach(s=>s.health=100); const r=C.escapeTry(j,true); res[r]++; }
      return JSON.stringify(res)+' settlers '+n0+'->'+G.settlers.length+' apHit '+Math.round(G.apHit||0)+' logs: '+G.log.slice(0,3).map(l=>l.m||l.t||JSON.stringify(l)).join(' || ').slice(0,1200); }"""))
    print(errs); await b.close()
asyncio.run(main())
