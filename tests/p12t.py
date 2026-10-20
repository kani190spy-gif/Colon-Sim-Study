import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.graceUntil=0; G.inst.gov=Math.max(2,G.inst.gov); G.res.caps+=3000; C.partyDay(); C.chairsDay();
      let ok=false; for(let f=0;f<G.floors+2&&!ok;f++){ if(f>=G.floors) G.floors++; for(let c=0;c<6&&!ok;c++){ if(!C.roomAt(f,c)) ok=C.build('intel',f,c); } }
      const r=G.rooms.find(x=>x.type==='intel'); const cand=G.settlers.filter(s=>!s.room&&!s.exp&&C.isCitizen(s)).slice(0,2); const pool=cand.length>=2?cand:G.settlers.filter(s=>!s.exp&&!s.mil&&s.id!==G.leader).slice(0,2); for(const s of pool){ C.assign(s,r); }
      const out=['built '+ok+' agents '+C.agents().length+' power '+C.intelPower().toFixed(2)];
      const L=G.settlers.find(s=>s.id===G.leader); const k=['com','mkt','nat','civ'].find(x=>x!==L.party);
      C.startPartyPlot(k); for(let i=0;i<10&&!G.plot.exposed;i++) C.intelDay(); out.push('plot exposed '+G.plot.exposed+' suspects '+G.plot.suspects.length);
      G.plot=null; L.doc={sec:.9,open:-.6,prag:.3,tech:false}; G.approval=35; let n=0; for(let i=0;i<60;i++){ G.day++; C.intelDay(); } out.push('abuse events '+JSON.stringify(G.intelAbuse||[]));
      return out.join(' | ')+' | '+G.log.slice(0,3).map(l=>l.m).join(' || ')}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.tab='council'; C.renderUI();}"); await pg.wait_for_timeout(300)
    print(errs[:5]); await b.close()
asyncio.run(main())
