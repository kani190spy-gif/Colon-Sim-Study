import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    for _ in range(3):
      if await pg.locator('[data-a=close]').count(): await pg.locator('[data-a=close]').first.click(); await pg.wait_for_timeout(300)
    # live boss fight
    await pg.evaluate("()=>{window.__forceBoss=true; window.__colony.G.lastBoss=null; window.__colony.startFight(); window.__forceBoss=false;}")
    print(await pg.evaluate("()=>{const F=window.__colony.FIGHT; return F?F.name+' foes '+F.foes.length+' bossHP '+Math.round(F.foes[0].hp)+' def '+F.def.length:'none'}"))
    for i in range(12):
      await pg.wait_for_timeout(5000)
      st=await pg.evaluate("()=>{const F=window.__colony.FIGHT; return F?('alive '+F.foes.filter(f=>!f.dead).length+' boss '+Math.round(F.foes[0].hp)+' def '+F.def.length):'over'}")
      if i==4: await pg.screenshot(path='boss_fight.png')
      if st=='over': break
    print(st)
    print(await pg.evaluate("()=>window.__colony.G.log.slice(0,6).map(l=>l.m).join('\\n')"))
    await pg.screenshot(path='boss_after.png')
    # offline boss loss forced: weaken defense
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.lastBoss=null; const d=window.defense; C.bossAftermath('Mother Rust',false); return 'hostages '+JSON.stringify(G.hostages)+' dmgRooms '+G.rooms.filter(r=>r.dmgUntil>G.day).length}"""))
    # plague
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; C.startPlague(2); const out=[]; for(let i=0;i<25&&G.plague;i++){ C.plagueDay(); out.push(G.settlers.filter(s=>s.sick).length); } return 'sick per day '+out.join(',')+' | '+G.log.slice(0,3).map(l=>l.m).join(' || ')+' | plagueLog '+JSON.stringify(G.plagueLog)}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.startPlague(0); C.UI.tab='study'; C.renderUI();}"); await pg.wait_for_timeout(400)
    await pg.locator('#tab').screenshot(path='plague_box.png')
    # rescue
    print(await pg.evaluate("()=>{const C=window.__colony,G=C.G; const h=(G.hostages||[])[0]; if(!h) return 'no hostage'; C.hostageRescue(h.sid); return G.log.slice(0,2).map(l=>l.m).join(' || ')}"))
    for i in range(3): await pg.evaluate("()=>window.__colony.dayStep()")
    print(errs[:5]); await b.close()
asyncio.run(main())
