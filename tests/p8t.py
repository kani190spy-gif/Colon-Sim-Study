import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.graceUntil=0; C.partyDay(); C.chairsDay(); const L=G.settlers.find(s=>s.id===G.leader); const rival=['com','mkt','nat','civ'].find(k=>k!==L.party);
      for(const s of G.settlers) if(s.party===rival) s.loy=5; const out=['rival '+rival+' approval '+C.partyApproval(rival)];
      let n=0; for(let i=0;i<30&&!G.plot;i++){ G.day++; C.partyPlotDay(); n++; } out.push('plot after '+n+' days: '+JSON.stringify(G.plot&&{party:G.plot.party,directed:G.plot.directed,slow:G.plot.slow,sus:G.plot.suspects.length}));
      if(G.plot){ G.day=G.plot.next; C.plotDay(); G.day=G.plot.next; C.plotDay(); out.push('stage '+G.plot.stage); }
      return out.join(' | ')+' | '+G.log.slice(0,3).map(l=>l.m).join(' || ')}"""))
    print(errs[:5]); await b.close()
asyncio.run(main())
