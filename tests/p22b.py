import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:400]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.inst.def=2; G.res.caps+=9000; let ok=false,where=null; for(let f=0;f<G.floors&&!ok;f++) for(let c=0;c<5&&!ok;c++){ if(!C.roomAt(f,c)&&!C.roomAt(f,c+1)){ ok=C.build('command',f,c); where=[f,c]; } }
      const r=G.rooms.find(x=>x.type==='command'); const sol=G.settlers.filter(s=>s.mil==='soldier'&&s.id!==G.leader); for(const s of sol.slice(0,3)) C.assign(s,r);
      for(const s of sol.slice(0,3)) if(!s.gear||!s.gear.w){ const it=G.items.find(i=>ITEMS_W(i)); } 
      C.UI.modal=null; G.gate=[]; C.renderUI(); return 'built '+ok+' at '+JSON.stringify([r.floor,r.col])+' workers '+r.workers.length+' fight '+!!C.FIGHT;}""".replace("const it=G.items.find(i=>ITEMS_W(i));","")))
    await pg.wait_for_timeout(40000)
    cv=pg.locator('canvas').first; await cv.screenshot(path='cmd.png')
    print(await pg.evaluate("()=>{const C=window.__colony,G=C.G; const r=G.rooms.find(x=>x.type==='command'); return [r.floor,r.col]}"))
    print(errs[:5]); await b.close()
asyncio.run(main())
