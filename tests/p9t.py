import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.graceUntil=0; C.partyDay(); C.chairsDay(); const L=G.settlers.find(s=>s.id===G.leader); const k=['com','mkt','nat','civ'].find(x=>x!==L.party&&C.partyApproval(x)!=null);
      const res=[];
      for(let t=0;t<6;t++){ G.plot=null; G.inquiry=null; C.startPartyPlot(k); const P=G.plot; P.directed=t%2===0; const before=G.settlers.filter(s=>s.party===k).length;
        if(t<4){ C.arrest(P.by); } else { P.stage=3; P.at=0; C.plotStrike(); }
        const ev=G.inquiry?Math.round(G.inquiry.ev*100):'none'; G.day+=3; C.inquiryDay(); const after=G.settlers.filter(s=>s.party===k).length;
        res.push(`${t<4?'caught':'struck'} directed=${P.directed} ev=${ev} susp=${G.pSusp&&G.pSusp[k]>G.day?G.pSusp[k]-G.day:0} members ${before}->${after}`); if(G.pSusp) G.pSusp[k]=0; for(const s of G.settlers) if(s.detained) s.detained=null; }
      return res.join('\\n')+'\\n'+G.log.slice(0,4).map(l=>l.m).join('\\n')}"""))
    await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const L=G.settlers.find(s=>s.id===G.leader); const k=['com','mkt','nat','civ'].find(x=>x!==L.party); C.suspendParty(k,15,'test'); C.UI.tab='council'; C.renderUI();}"""); await pg.wait_for_timeout(400)
    await pg.locator('#tab .box:has(h4:text("Party leadership"))').screenshot(path='susp.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
