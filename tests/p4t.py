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
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; C.partyDay(); const cnt=()=>{const o={}; for(const s of G.settlers) if(s.party) o[s.party]=(o[s.party]||0)+1; return JSON.stringify(o)}; const avg=()=>{const A=G.settlers.filter(s=>s.ec!=null); return (A.reduce((x,s)=>x+s.ec,0)/A.length).toFixed(2)}; const a=cnt()+" ec "+avg();
      G.flags.food=true; for(let i=0;i<20;i++){ G.day++; C.partyDay(); } const b=cnt()+" ec "+avg()+" D "+JSON.stringify(G.pDrift); G.flags.food=false; for(let i=0;i<40;i++){ G.day++; C.partyDay(); } return 'start '+a+' after shortage '+b+' later '+cnt()+' switches '+(G.pSwitch||[]).length}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.tab='council'; C.renderUI();}"); await pg.wait_for_timeout(500)
    el=pg.locator('#tab .box:has(h4:text("Parties"))'); await el.screenshot(path='parties.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
