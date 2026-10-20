import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    for _ in range(3):
      if await pg.locator('[data-a=close]').count(): await pg.locator('[data-a=close]').first.click(); await pg.wait_for_timeout(300)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; C.partyDay(); C.chairsDay(); const ch=Object.entries(G.pChair||{}).map(([k,id])=>k+':'+(id?G.settlers.find(s=>s.id===id).first:'-')).join(' '); const ap=['com','mkt','nat','civ'].map(k=>k+' '+C.partyApproval(k)).join(', ');
      const gov=G.inst.gov; G.inst.gov=Math.max(gov,3); const r=[]; for(let i=0;i<5;i++){ C.election(); r.push(G.lastElection.results.map(x=>x.name.split(' ')[0]+'('+x.party+') '+Math.round(x.share*100)).join(' / ')); } G.inst.gov=gov; return 'chairs '+ch+' | approval '+ap+' | elections: '+r.join(' || ')}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.tab='council'; C.renderUI();}"); await pg.wait_for_timeout(500)
    await pg.locator('#tab .box:has(h4:text("Party leadership"))').screenshot(path='party2.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
