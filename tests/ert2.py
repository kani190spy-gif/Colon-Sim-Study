import asyncio, os
from PIL import Image
src=open('colony/index.html').read()
open('wrapped.html','w').write('<!doctype html><html><head><meta charset="utf-8"><style>[hidden]{display:none!important}body{margin:0}</style></head><body>'+src+'</body></html>')
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1600,'height':1100},device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(1000)
    await pg.click('[data-a=bigview]'); await pg.wait_for_timeout(400)
    await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps=1e6; G.inst.health=2; C.build('clinic',0,3);
      const ad=G.settlers.filter(s=>!s.preg&&s.bd==null); G.ert=[ad[0].id,ad[1].id]; const pat=ad.find(s=>s.room&&!G.ert.includes(s.id)&&G.rooms.find(r=>r.id===s.room).floor===1); pat.health=30; C.callEmergency(pat,'injury',true); window._e=G.emerg[0]; window._p=pat.id;}""")
    shots=[]; t=0; done=False
    for i in range(60):
      await pg.wait_for_timeout(1000); t+=1
      st=await pg.evaluate("()=>{const G=window.__colony.G; return (G.emerg[0]||{stage:'none'}).stage}")
      if i in (2,5,8,12,16) or (st=='none' and not done):
        await pg.screenshot(path=f'f{i}.png'); shots.append((i,st))
        if st=='none': done=True; await pg.wait_for_timeout(1500); await pg.screenshot(path='fbed.png'); break
    print(shots)
    print(await pg.evaluate("()=>window.__colony.G.log.slice(0,3).map(l=>l.m).join(' // ')"))
    print(errs); await b.close()
asyncio.run(main())
