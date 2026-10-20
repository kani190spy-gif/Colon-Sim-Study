import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.graceUntil=0; C.partyDay(); C.chairsDay(); const snap=JSON.stringify(G); const out=[];
      out.push('commanders: '+C.topCommander().map(([s,k])=>s.first+'/'+k).join(', '));
      for(const choice of ['back','oppose','out','out']){ const G2=JSON.parse(snap); for(const k in G2) C.G[k]=G2[k];
        for(const s of C.G.settlers) if(s.mil||s.pol) s.loy=10; const cs=C.topCommander(); if(!cs.length){ out.push('no commander'); break; } const [by,kind]=cs[0]; C.startCoup(by,kind); const Cp=C.G.coup; C.G.day=Cp.next; Cp.purgeTried=true; C.coupStep(); C.G.coup.choice=choice; const F=C.coupForces(by,kind);
        const ldr0=C.G.leader; C.coupStep(); out.push(choice+': coup '+F.coup.length+' vs loyal '+F.loyal.length+' -> leader '+(C.G.leader===ldr0?'kept':'changed')+' emergency '+!!C.G.emergency); }
      return out.join('\\n')+'\\n'+C.G.log.slice(0,3).map(l=>l.m).join('\\n')}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.tab='council'; C.renderUI();}"); await pg.wait_for_timeout(300)
    print(errs[:5]); await b.close()
asyncio.run(main())
