import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    for _ in range(3):
      if await pg.locator('[data-a=close]').count(): await pg.locator('[data-a=close]').first.click(); await pg.wait_for_timeout(300)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.inst.gov=Math.max(G.inst.gov,3); G.res.caps+=5000; C.partyDay(); C.chairsDay();
      // find free 2-wide slot
      let ok=false; for(let f=0;f<G.floors+2&&!ok;f++){ if(f>=G.floors){ G.floors++; } for(let c=0;c<5&&!ok;c++){ if(!C.roomAt(f,c)&&!C.roomAt(f,c+1)) ok=C.build('phall',f,c); } }
      const h=G.rooms.find(r=>r.type==='phall'); return 'built '+ok+' party '+(h&&h.party)+' floor '+(h&&h.floor)}"""))
    r=await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const h=G.rooms.find(r=>r.type==='phall'); C.startAssembly(h.party,'rally'); return JSON.stringify(G.assembly)}""")
    print(r)
    await pg.evaluate("()=>{const C=window.__colony,G=C.G; const h=G.rooms.find(r=>r.type==='phall'); C.UI.modal=null; C.UI.follow=G.assembly.ids[0]; }")
    await pg.wait_for_timeout(9000)
    await pg.screenshot(path='hall_rally.png')
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.assembly.end=0; C.assemblyStep(); const h=G.rooms.find(r=>r.type==='phall'); C.startAssembly(h.party,'march'); G.assembly.end=0; C.assemblyStep(); return G.log.slice(0,4).map(l=>l.m).join(' || ')+' protest '+!!G.protest}"""))
    print(errs[:5]); await b.close()
asyncio.run(main())
