import asyncio, os
from playwright.async_api import async_playwright
src=open('colony/index.html').read()
open('wrapped.html','w').write('<!doctype html><html><head><meta charset="utf-8"><style>[hidden]{display:none!important}body{margin:0}</style></head><body>'+src+'</body></html>')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'TUNNEL' not in m.text else None)
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(1000)
    r=await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps=1e6; const o=[];
      o.push('unconnected B3c3 '+C.build('jail',2,3)); o.push('B3c0 '+C.build('jail',2,0)); o.push('B3c1 '+C.build('jail',2,1));
      o.push('class merge: '+C.build('classroom',1,3)+' '+C.build('classroom',1,4)+' '+C.build('classroom',1,5)); o.push(G.rooms.filter(r=>r.type==='classroom').map(r=>r.col+'w'+r.w).join(','));
      const j=G.rooms.find(r=>r.type==='jail'); const g=G.settlers.find(s=>!s.room); if(g) C.assign(g,j); return o;}""")
    print(r)
    await pg.click('#sessBtn'); await pg.evaluate("()=>window.__colony.startFight()")
    await pg.wait_for_timeout(30000)
    print(await pg.evaluate("()=>window.__colony.G.log.slice(0,3).map(l=>l.m).join(' // ')"))
    print(await pg.evaluate("()=>JSON.stringify((window.__colony.G.captives||[]).map(q=>q.s.first+' '+q.room))"))
    await pg.evaluate("()=>{ const C=window.__colony,G=C.G; const q=(G.captives||[])[0]; if(q){ q.war='mladic'; } G.inst.gov=1; }")
    if await pg.evaluate("()=>(window.__colony.G.captives||[]).length>0"):
      await pg.evaluate("()=>{ const q=window.__colony.G.captives[0]; const b=document.createElement('button'); b.dataset.a='trial'; b.dataset.id=q.id; document.body.appendChild(b); b.click(); const c=window.__colony.G.captives[1]; if(c){ const r=document.createElement('button'); r.dataset.a='release'; r.dataset.id=c.id; document.body.appendChild(r); r.click(); } }")
    await pg.evaluate("()=>{ const C=window.__colony; C.UI.modal={t:'book',v:'pris'}; C.renderUI(); }"); await pg.wait_for_timeout(1200); await pg.screenshot(path='pris.png')
    print(await pg.evaluate("()=>JSON.stringify((window.__colony.G.prisonRec||[]).map(r=>[r.name,r.sent,r.how]))"))
    await pg.evaluate("()=>{ const C=window.__colony; C.UI.modal=null; C.renderUI(); }")
    await pg.click('[data-a=bigview]'); await pg.wait_for_timeout(600)
    await pg.evaluate("()=>{const w=document.getElementById('sceneWrap'); w.scrollTop=9999;}"); await pg.wait_for_timeout(2500)
    await pg.locator('#sceneWrap').screenshot(path='j1.png')
    print(errs); await b.close()
asyncio.run(main())
