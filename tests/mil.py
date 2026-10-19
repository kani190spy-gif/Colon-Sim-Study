import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1300,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(1000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps=5000; C.build('armory',1,3); const arm=G.rooms.find(r=>r.type==='armory'), ent=C.entRoom(), gen=G.rooms.find(r=>r.type==='generator');
      const ad=G.settlers.filter(s=>s.bd==null&&!s.preg&&s.first!=='Desmond'); const o=[];
      o.push('civ->armory '+C.assign(ad[0],arm));
      C.enlist(ad[0],'soldier'); o.push('sol->armory '+C.assign(ad[0],arm)+' '+ad[0].room);
      o.push('sol->gen '+C.assign(ad[0],gen));
      C.enlist(ad[1],'soldier'); o.push('sol->entrance '+C.assign(ad[1],ent));
      C.enlist(ad[2],'reserve'); o.push('res job kept '+ad[2].room);
      C.enlist(ad[3],'soldier'); o.push('unposted sol room '+ad[3].room);
      const d=C.defense(); const c0=G.res.caps, f0=G.res.food; C.milUpkeep(); o.push('def '+d.toFixed(1)+' upkeep caps '+(c0-G.res.caps)+' food '+(f0-G.res.food));
      C.startFight(); const F=C.FIGHT; o.push('defenders '+F.def.map(id=>{const s=G.settlers.find(x=>x.id===id); return s.first+':'+(s.mil||'civ');}).join(','));
      // migration of old save
      const g=JSON.parse(JSON.stringify(G)); delete g.milV; const w=g.settlers.find(s=>s.id===ad[1].id); w.mil=null; C.migrate(g); o.push('migrated entrance guard -> '+g.settlers.find(s=>s.id===ad[1].id).mil);
      return o.join(' | '); }"""))
    await pg.evaluate("()=>{ const C=window.__colony; C.UI.modal={t:'mil'}; C.renderUI(); }"); await pg.wait_for_timeout(700); await pg.screenshot(path='mil.png')
    print(errs); await b.close()
asyncio.run(main())
