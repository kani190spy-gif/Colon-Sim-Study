import asyncio, os
from playwright.async_api import async_playwright
DBG="()=>{const G=window.__colony.G,B=G.burial; if(!B) return 0; const a=window.__colony.AG.get(B.dig); const b=G.bodies.find(x=>x.id===B.bid); return JSON.stringify([Math.round(a.x),a.l,a.pose,a.path,b&&Math.round(b.x),b&&b.l])}"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1600,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'ERR_TUNNEL' not in m.text else None)
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    await pg.click('[data-a=bigview]')
    await pg.evaluate("()=>{const C=window.__colony,G=C.G; G.settlers.forEach(s=>s.s.S=10); C.startFight();}")
    for i in range(40):
      await pg.wait_for_timeout(1000)
      if not await pg.evaluate("()=>!!window.__colony.FIGHT"): break
    print(await pg.evaluate("()=>JSON.stringify(window.__colony.G.bodies.map(b=>[b.kind,Math.round(b.x),b.loot]))"))
    print(await pg.evaluate("()=>window.__colony.G.log[0].m"))
    await pg.wait_for_timeout(500); await pg.screenshot(path='bd1.png')
    caps0=await pg.evaluate("()=>window.__colony.G.res.caps")
    await pg.evaluate("()=>{const C=window.__colony,G=C.G; const b=G.bodies.find(x=>x.kind==='raider'); if(b) C.lootRaider(b);}")
    print('caps +', await pg.evaluate("()=>window.__colony.G.res.caps")-caps0, await pg.evaluate("()=>document.getElementById('toast').textContent"))
    # a settler dies in the vault, then is buried
    await pg.evaluate("()=>{const C=window.__colony,G=C.G; const v=G.settlers.find(s=>s.bd==null&&!s.partner&&s.room); C.removeSettler(v,'Old age'); const b=G.bodies.find(x=>x.kind==='settler'); C.UI.modal={t:'body',id:b.id}; C.renderUI();}")
    await pg.wait_for_timeout(500); await pg.locator('.dlg').screenshot(path='bd2.png')
    await pg.evaluate("()=>document.querySelector('[data-a=bury]').click()")
    for i in range(60):
      await pg.wait_for_timeout(1000)
      st=await pg.evaluate("()=>JSON.stringify(window.__colony.G.burial)")
      if i%5==0: print(st, await pg.evaluate(DBG))
      if i in (4,12): await pg.screenshot(path=f'bd3_{i}.png')
      if st=='null': break
    print('burial done after',i, await pg.evaluate("()=>JSON.stringify(window.__colony.G.graves)"))
    await pg.wait_for_timeout(500); await pg.screenshot(path='bd4.png')
    # expedition death carried home
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const team=G.settlers.filter(s=>s.bd==null&&!s.preg&&s.health>=50).slice(0,2); const e=C.startExpedition(team.map(s=>s.id),'live','UWorld',0); team[0].health=1; C.expAnswer(e,false); C.expAnswer(e,false); C.expAnswer(e,false); C.expAnswer(e,false); C.expAnswer(e,false); return JSON.stringify({deaths:e.deaths,bodies:e.bodies&&e.bodies.length,team:e.team.length}); }"""))
    print(errs); await b.close()
asyncio.run(main())
