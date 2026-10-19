import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const s=G.settlers[3]; const out=[];
      for(const [lab,w,o] of [['unarmed, no armor',null,null],['armed+armored',1,1]]){ const g0=s.gear; s.gear={}; if(w){ const it={id:9e6,k:'magnum'}; G.items.push(it); s.gear.w=it.id; } if(o){ const it={id:9e6+1,k:'o_colonel'}; G.items.push(it); s.gear.o=it.id; }
        for(const tier of [0,1,2]){ let tot=0,mx=0; for(let i=0;i<5000;i++){ const d=raidHit(s,{dmg:[2.2,3.6,5.4][tier],tier}); tot+=d; mx=Math.max(mx,d);} out.push(lab+' tier'+tier+' avg '+(tot/5000).toFixed(1)+' max '+mx.toFixed(1)); } s.gear=g0; G.items=G.items.filter(i=>i.id<9e6); }
      return out.join('\\n'); }""".replace('raidHit(','C.raidHit(')))
    await pg.evaluate("()=>{const C=window.__colony,G=C.G; C.startFight();}")
    for i in range(40):
      await pg.wait_for_timeout(1000)
      if not await pg.evaluate("()=>!!window.__colony.FIGHT"): break
    print(await pg.evaluate("()=>window.__colony.G.log.slice(0,3).map(l=>l.m).join(' // ')"))
    print(errs); await b.close()
asyncio.run(main())
