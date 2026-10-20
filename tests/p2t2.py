import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    snap=await pg.evaluate("()=>JSON.stringify(window.__colony.G)")
    for sev in [0,1,2]:
      for quar in [False,True]:
        r=await pg.evaluate("""([snap,sev,quar])=>{const C=window.__colony; let res=[]; for(let k=0;k<6;k++){ const G=JSON.parse(snap); Object.assign(C.G,G); C.G.settlers=G.settlers; C.startPlague(sev); C.G.plague.quar=quar; C.G.plague.treat=quar; let days=0; while(C.G.plague&&days<40){ C.G.day++; C.plagueDay(); days++; } const L=C.G.plagueLog&&C.G.plagueLog[0]; res.push(L?L.total+'/'+L.dead+'/'+days+'d':'ongoing'); } return res.join(' ')}""",[snap,sev,quar])
        print('sev',sev,'measures',quar,':',r)
    print(errs[:3]); await b.close()
asyncio.run(main())
