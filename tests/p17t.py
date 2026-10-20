import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const sol=G.settlers.filter(s=>s.mil==='soldier'), res=G.settlers.filter(s=>s.mil==='reserve');
      return 'soldiers '+sol.length+' reserve '+res.length+' ranks '+sol.map(s=>s.first+':'+(s.rank_m||0)).join(',')+' | res '+res.map(s=>s.first+':'+(s.rank_m||0)).join(',')+' leader mil '+(G.settlers.find(s=>s.id===G.leader)||{}).mil}"""))
    print(await pg.evaluate('''()=>{const C=window.__colony,G=C.G; G.inst.def=Math.max(2,G.inst.def); G.res.caps+=9000; let ok=G.rooms.some(r=>r.type==='command'); for(let f=0;f<G.floors+2&&!ok;f++){ if(f>=G.floors) G.floors++; for(let c=0;c<5&&!ok;c++){ if(!C.roomAt(f,c)&&!C.roomAt(f,c+1)) ok=C.build('command',f,c); } }
      const civ=G.settlers.filter(s=>!s.mil&&s.ec0!=null&&!s.pol&&s.id!==G.leader).slice(0,10); for(const s of civ){ s.mil='soldier'; }
      const sol=G.settlers.filter(s=>s.mil==='soldier'&&s.id!==G.leader); const rk=[7,6,5,5,4,4,3,3,3,2,2,1,1,0,0]; sol.forEach((s,i)=>s.rank_m=rk[i]??0);
      const L=G.settlers.find(s=>s.id===G.leader); L.rank_m=5; L.milLeave='office'; const r0=G.settlers.find(s=>s.mil==='reserve'); r0.rank_m=5;
      return 'built '+ok+' sol '+sol.length+' rankOf reserve '+C.rankOf?.(r0);}'''))
    await pg.evaluate("()=>{const C=window.__colony; C.G.gate=[]; C.UI.modal={t:'miltree'}; C.renderUI();}"); await pg.wait_for_timeout(1200)
    await pg.locator('#modal .dlg').screenshot(path='miltree.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
