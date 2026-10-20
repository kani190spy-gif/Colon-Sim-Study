import asyncio, os, json, base64, gzip, sys
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  mode=sys.argv[1]
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    for _ in range(3):
      if await pg.locator('[data-a=close]').count(): await pg.locator('[data-a=close]').first.click(); await pg.wait_for_timeout(300)
    print(await pg.evaluate("""(mode)=>{const C=window.__colony,G=C.G; G.graceUntil=0; G.inst.gov=Math.max(3,G.inst.gov); G.res.caps+=3000; C.partyDay(); C.chairsDay(); const L=G.settlers.find(s=>s.id===G.leader);
      const k=['com','mkt','nat','civ'].filter(x=>x!==L.party).sort((a,b)=>C.partyMembers?0:0)[0];
      let ok=false; for(let f=0;f<G.floors+2&&!ok;f++){ if(f>=G.floors) G.floors++; for(let c=0;c<5&&!ok;c++){ if(!C.roomAt(f,c)&&!C.roomAt(f,c+1)) ok=C.build('phall',f,c); } }
      const h=G.rooms.find(r=>r.type==='phall'); h.party=k; G.pChair=G.pChair||{}; C.chairsDay(); C.startUprising(k); const U=G.uprising; if(!U) return 'no uprising';
      if(mode==='raid') C.uprDecide('raid',true); else if(mode==='talk') C.uprDecide('negotiate',true); else { C.uprDecide('wait',true); U.goAt=0; }
      return 'uprising '+k+' rebels '+(U?U.ids.length:0)+' defenders '+G.settlers.filter(s=>(s.mil==='soldier'||s.pol)&&!s.rebel).length+' stage '+(G.uprising&&G.uprising.stage)}""",mode))
    for i in range(30):
      await pg.wait_for_timeout(4000)
      st=await pg.evaluate("()=>{const U=window.__colony.G.uprising; const G=window.__colony.G; return U?U.stage+' clock '+Math.round(U.clock)+' deaths '+U.deaths+' R '+U.ids.map(id=>G.settlers.find(s=>s.id===id)).filter(s=>s&&s.rebel&&s.health>15).length+' D '+G.settlers.filter(s=>!s.rebel&&!s.exp&&!s.detained&&s.health>20&&(s.mil==='soldier'||s.pol)).length:'over'}")
      if i==3: await pg.screenshot(path='upr.png')
      print(st)
      if st=='over': break
    print(st)
    print(await pg.evaluate("()=>window.__colony.G.log.slice(0,6).map(l=>l.m).join('\\n')"))
    print(errs[:5]); await b.close()
asyncio.run(main())
