import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.inst.gov=2; const ad=G.settlers.filter(s=>s.bd==null); G.leader=ad[0].id; G.apBoost=0; G.apHit=0;
      const out=[]; for(const c of [30,45,52,57,62,67,80]){ G.opsDay=null; const b0=G.apBoost, h0=G.apHit; const ids=ad.slice(1,3).filter(s=>!s.exp).map(s=>s.id); ad.slice(1,3).forEach(s=>{s.health=100; s.exp=null;});
        C.reportExpedition(ad.slice(1,3).map(s=>s.id),'UWorld',0,20,Math.round(c/5)); out.push(c+'%: +'+(G.apBoost-b0).toFixed(1)+' -'+(G.apHit-h0).toFixed(1)); G.exps.forEach(e=>{e.backAt=0;}); G.exps=[]; ad.forEach(s=>s.exp=null); }
      return out.join(' | ')+'\\n'+G.log.slice(0,3).map(l=>l.m||l.t).join('\\n')+'\\n'+C.lifeBox(ad[1]).match(/Took part[^<]*/)[0]; }"""))
    print(errs); await b.close()
asyncio.run(main())
