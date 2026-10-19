import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1300,'height':1300})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.inst.gov=1; const ad=G.settlers.filter(s=>s.bd==null); G.leader=ad[0].id; ad.forEach((s,i)=>{ if(i%3==1){ s.s.C=7; s.happy=5; s.grief=40; } if(i%3==2){ s.happy=10; s.grief=30; } }); C.enlist(ad[4],'soldier'); C.enlist(ad[7],'soldier'); ad[7].s.C=7; ad[7].happy=10; ad[4].happy=10; ad[7].grief=30;
      for(let d=0;d<8;d++) C.polDay(); return JSON.stringify((G.pfac||[]).map(f=>[f.name,f.b,f.n,f.hos,f.lvl]))+' leans '+JSON.stringify(G.settlers.filter(s=>s.lean).map(s=>s.lean[0]+Math.round(s.loy)).join(',')); }"""))
    await pg.evaluate("()=>{ const C=window.__colony; C.UI.tab='council'; C.renderUI(); }"); await pg.wait_for_timeout(600)
    await pg.locator('#tab').screenshot(path='pol.png')
    print(errs); await b.close()
asyncio.run(main())
