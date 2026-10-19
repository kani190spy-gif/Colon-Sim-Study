import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1300,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+' '+(e.stack or '')[:400]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    for _ in range(3):
      if await pg.locator('[data-a=close]').count(): await pg.locator('[data-a=close]').first.click(); await pg.wait_for_timeout(300)
    async def click(a,v=None):
      await pg.evaluate("([a,v])=>{const el=document.createElement('button');el.dataset.a=a;if(v!=null)el.dataset.v=v;document.body.appendChild(el);el.click();el.remove();window.__colony.renderUI();}",[a,v]); await pg.wait_for_timeout(150)
    await click('obOpen','list'); await pg.locator('#modal .dlg').screenshot(path='ob_list.png')
    await click('obGo','pph'); await pg.fill('#obAns','4 Ts, oxytocin, type and cross'); await pg.click('[data-a=obRev]'); await pg.wait_for_timeout(200)
    await pg.locator('#modal .dlg').screenshot(path='ob_rev.png')
    await pg.locator('#modal .dlg').screenshot(path='ob_rev.png')
    await click('obAll'); await click('obNext')
    for i in range(4):
      await click('obRev'); await click('obAll'); await click('obNext')
    caps0=await pg.evaluate("window.__colony.G.res.caps")
    # last stage: tick only some
    await pg.evaluate("()=>{}")
    await click('obRev'); await click('obChk','5_0'); await click('obEnd')
    await pg.locator('#modal .dlg').screenshot(path='ob_done.png')
    print(await pg.evaluate("()=>{const G=window.__colony.G;return JSON.stringify(G.ob)+' | '+G.log.slice(0,2).map(l=>l.m).join(' || ')}"))
    # critical-miss case
    await click('obGo','ectopic')
    for i in range(5): await click('obRev'); await click('obNext')
    await click('obRev'); await click('obEnd')
    await pg.locator('#modal .dlg').screenshot(path='ob_bad.png')
    print(await pg.evaluate("()=>window.__colony.G.log.slice(0,1).map(l=>l.m).join('')"))
    await click('obOpen','rf'); await click('obRf','0'); await pg.locator('#modal .dlg').screenshot(path='ob_rf.png')
    await click('obOpen','guide'); await click('obG','5'); await pg.locator('#modal .dlg').screenshot(path='ob_guide.png')
    await click('close'); await pg.evaluate("()=>{window.__colony.UI.tab='study';window.__colony.renderUI()}"); await pg.wait_for_timeout(300)
    await pg.screenshot(path='ob_tab.png')
    print('births', await pg.evaluate("()=>{const C=window.__colony,G=C.G;const m=G.settlers.find(s=>s.sex==='F');let n=0;for(let i=0;i<2000;i++){const h=m.health;C.birthRisk(m);m.health=h;} return G.ob.buff+' day '+G.day}"))
    print(errs); await b.close()
asyncio.run(main())
