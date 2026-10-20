import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.inst.gov=Math.max(G.inst.gov,3); C.partyDay(); C.chairsDay(); const L=G.settlers.find(s=>s.id===G.leader); const out=['odds '+C.postponeOdds(L).toFixed(2)];
      L.doc={sec:.8,open:-.5,prag:.3,tech:false}; G.approval=40; out.push('hawk odds '+C.postponeOdds(L).toFixed(2));
      let post=0, held=0; for(let i=0;i<10;i++){ G.nextElection=G.day; const p0=G.postponed||0; const LL=G.settlers.find(s=>s.id===G.leader); out.push(C.postponeOdds(LL).toFixed(2)+'/'+G.approval.toFixed(0)+'/'+JSON.stringify(LL.doc).slice(0,20)); C.electionDue(); if((G.postponed||0)>p0) post++; else held++; }
      out.push('10 tries: postponed '+post+' held '+held+' next '+(G.nextElection-G.day));
      return out.join(' | ')+' | '+G.log.slice(0,2).map(l=>l.m).join(' || ')}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.tab='council'; C.renderUI();}"); await pg.wait_for_timeout(400)
    await pg.locator('#tab .box:has(h4:text-is("Leader"))').screenshot(path='elect.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
