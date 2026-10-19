import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':1000},device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(1200)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const a=G.settlers.find(s=>s.first==='Amir'); C.removeSettler(a,'Heart attack'); const b=G.bodies.find(x=>x.kind==='settler'); C.startBurial(b); return JSON.stringify(G.burial)+' '+G.log[0].m; }"""))
    shot=False
    for k in range(70):
      await pg.wait_for_timeout(2000)
      st=await pg.evaluate("()=>{const B=window.__colony.G.burial; return B?B.stage+' '+Math.round(B.t)+' svc '+(B.svc||0).toFixed(1):'done'}")
      if st.startswith('dig') and 'svc 0.0' not in st and not shot:
        box=await pg.evaluate("""()=>{ const cv=document.querySelector('canvas'); const R=cv.getBoundingClientRect(); return [R.left,R.top,R.width,R.height]; }""")
        x0,y0,w,h=box
        await pg.screenshot(path='fun.png',clip={'x':x0+w*0.78,'y':y0+h*0.12,'width':w*0.22,'height':h*0.2}); shot=True
      if st=='done': break
    print('final', st, k, await pg.evaluate("()=>window.__colony.G.log.slice(0,2).map(l=>l.m).join(' // ')"))
    print(errs); await b.close()
asyncio.run(main())
