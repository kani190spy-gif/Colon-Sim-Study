import asyncio, os, json
from playwright.async_api import async_playwright
async def main():
  g=open('/mnt/user-data/uploads/Applications/ColonySim/saves/current.json').read()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:400])); pg.on('console',lambda m: errs.append('console:'+m.text[:300]) if m.type=='error' and 'net::' not in m.text else None)
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.graceUntil=0; G.res.caps+=3000; const out=[]; out.push('intel '+C.build('intel',5,0)+' distill '+C.build('distill',6,0));
      const r=G.rooms.find(x=>x.type==='distill'); const w=G.settlers.filter(s=>s.ec0!=null&&!s.mil&&!s.pol&&s.id!==G.leader).slice(0,2); for(const s of w) C.assign(s,r);
      for(let d=0;d<6;d++){ G.day++; C.drinkDay(); } const A=G.settlers.filter(s=>s.drink!=null); out.push('drink dist '+[0,1,2,3].map(k=>A.filter(s=>s.drink===k).length).join('/')+' rakija '+Math.round(G.rakija)+' caps sold '+G._rakSold);
      const sess=G.settlers.filter(s=>s.drinkAt!=null); out.push('sessions '+sess.length); for(const s of sess) s.drinkAt=C.nowD()-.07; C.drinkStep(); out.push('drunk now '+G.settlers.filter(C.isDrunk).length);
      const ab=G.settlers.find(s=>s.drink>=1); C.drunkDisorder(ab); out.push('held '+JSON.stringify(ab.detained));
      for(let i=0;i<4;i++) G.drinkInc.push(G.day); C.distClose(8,'leader','Test closure.'); out.push('open? '+C.distOpen());
      return out.join(' | ')+' || '+G.log.slice(0,3).map(l=>l.m).join(' || ')}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal=null; C.G.gate=[]; C.G.distClosed=null; for(const s of C.G.settlers) if(s.drink>=1) s.drunkUntil=C.nowD()+.2; C.renderUI(); window.dispatchEvent(new Event('resize'))}"); await pg.wait_for_timeout(3000)
    cv=pg.locator('canvas').first; await cv.scroll_into_view_if_needed(); await pg.wait_for_timeout(800); await cv.screenshot(path='v100.png')
    print(errs[:6]); await b.close()
asyncio.run(main())
