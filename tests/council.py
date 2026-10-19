import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1300,'height':1600})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.inst.gov=2; G.inst.health=2; const ad=G.settlers.filter(s=>s.bd==null); G.leader=ad[0].id; const o=[];
      for(let d=0;d<10;d++){ G.day++; C.polDay(); C.councilDay(); }
      o.push('council '+G.council.length+' policies '+G.policies.join(','));
      // make council furious
      for(const id of G.council){ const s=G.settlers.find(x=>x.id===id); s.happy=0; s.grief=60; }
      for(let d=0;d<8;d++){ G.day++; C.polDay(); C.councilDay(); }
      o.push('after vote leader '+G.leader+' interreg '+JSON.stringify(G.interreg)); for(let d=0;d<6;d++){ G.day++; C.polDay(); C.councilDay(); } o.push('leader now '+(G.settlers.find(s=>s.id===G.leader)||{}).first);
      return o.join(' | ')+' // '+(G.polNews||[]).slice(0,7).map(n=>n.m).join(' / '); }"""))
    await pg.evaluate("()=>{ const C=window.__colony; C.UI.tab='council'; C.renderUI(); }"); await pg.wait_for_timeout(600)
    await pg.locator('#tab').screenshot(path='council.png')
    print(errs); await b.close()
asyncio.run(main())
