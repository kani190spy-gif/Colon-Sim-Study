import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(1000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; C.build('quarters',1,3); const v=C.mkVisitor(); G.gate.push(v); const b=document.createElement('button'); b.dataset.a='accept'; b.dataset.i=G.gate.length-1; document.body.appendChild(b); b.click(); const s=G.settlers[G.settlers.length-1]; window.__s=s; return s.first+' intake '+(s.intake-Date.now()); }"""))
    for k in range(8):
      await pg.wait_for_timeout(6000)
      print(await pg.evaluate("""()=>{const C=window.__colony,s=window.__s,a=C.AG.get(s.id); return [Math.round(a.x),a.l,a.pose,s.intake?Math.round((s.intake-Date.now())/1000):null,s.room].join(' '); }"""))
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const j=G.rooms.find(r=>r.type==='jail'); return 'rehab test: '+JSON.stringify((G.captives||[]).map(q=>q.rehab)); }"""))
    print(errs); await b.close()
asyncio.run(main())
