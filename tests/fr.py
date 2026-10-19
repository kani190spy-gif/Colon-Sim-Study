import asyncio, os, json, base64, gzip, time, sys
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud2/data/users/me/c0.json')); d=d.get('data',d); gs=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--enable-gpu-rasterization']); pg=await b.new_page(viewport={'width':1400,'height':1000},device_scale_factor=int(sys.argv[1]) if len(sys.argv)>1 else 1)
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(gs)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(1500)
    print(await pg.evaluate("""()=>{ const C=window.__colony; const cv=document.querySelector('canvas'); let s=performance.now(); for(let i=0;i<60;i++) C.drawScene(s+i*16.7); const dt=(performance.now()-s)/60; return 'canvas '+cv.width+'x'+cv.height+' drawScene '+dt.toFixed(1)+'ms'; }"""))
    await b.close()
asyncio.run(main())
