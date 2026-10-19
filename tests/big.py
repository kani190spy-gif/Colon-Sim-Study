import asyncio, os, json, base64, gzip, sys
from playwright.async_api import async_playwright
N=int(sys.argv[1])
async def main():
  d=json.load(open('cloud2/data/users/me/c0.json')); d=d.get('data',d); g=json.loads(gzip.decompress(base64.b64decode(d['s'])).decode())
  base=[s for s in g['settlers']]; nid=max(s['id'] for s in base)+1
  rooms=[r['id'] for r in g['rooms'] if r['type'] not in ('office','entrance','jail','precinct')]
  i=0
  while len(g['settlers'])<N:
    s=json.loads(json.dumps(base[i%len(base)])); s['id']=nid; nid+=1; s['partner']=None; s['children']=[]; s['parents']=[]; s['room']=None; s['mil']=None; s['pol']=None; s['exp']=None; s['waiting']=False; g['settlers'].append(s); i+=1
  g['nextId']=nid+10
  gs=json.dumps(g)
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(gs)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(3000)
    print(N, await pg.evaluate("""()=>{ const C=window.__colony; const n=C.G.settlers.length; let s=performance.now(); for(let i=0;i<30;i++) C.drawScene(s+i*16.7); const dt=(performance.now()-s)/30; 
      let t2=performance.now(); for(let i=0;i<20;i++) C.runSpan(60000,false); const sim=(performance.now()-t2)/20; return 'n='+n+' drawScene '+dt.toFixed(1)+'ms; sim 1 real min '+sim.toFixed(1)+'ms'; }"""))
    print(errs[:2]); await b.close()
asyncio.run(main())
