import asyncio, os, json
from playwright.async_api import async_playwright
async def main():
  g=open('/mnt/user-data/uploads/Applications/ColonySim/saves/current.json').read()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:400])); pg.on('console',lambda m: errs.append('console:'+m.text[:300]) if m.type=='error' and 'net::' not in m.text else None)
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps+=9000; G.graceUntil=0; let r=G.rooms.find(x=>x.type==='execc'); let ok=!!r; if(!r){ ok=C.build('execc',6,0); r=G.rooms.find(x=>x.type==='execc'); }
      for(let d=0;d<3;d++){ G.day++; C.cabinetDay(); } r.design='marble'; G.flag={lay:'h3',c:['#1f3f8a','#f2efe6','#1f3f8a'],em:'lily',ec:'#d9b14a'}; G.flagHist=[{}];
      const where=['execc','office','command','precinct'].map(t=>{const q=G.rooms.find(x=>x.type===t); return q?t+':'+q.floor+','+q.col:t+':none'}).join(' ');
      C.UI.modal=null; G.gate=[]; C.renderUI(); window.dispatchEvent(new Event('resize')); return 'exec '+ok+' workers '+r.workers.length+' | '+where;}"""))
    await pg.wait_for_timeout(45000)
    await pg.locator('canvas').first.screenshot(path='v109.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
