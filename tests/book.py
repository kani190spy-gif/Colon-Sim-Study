import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1300,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps=1e5; G.res.food=1e5; G.res.water=1e5; G.res.power=1e5; C.build('quarters',1,3);
      const q2=G.rooms.find(r=>r.type==='quarters'&&r.col===3); const ad=G.settlers.filter(s=>s.bd==null&&!s.partner&&s.sex==='M'), af=G.settlers.filter(s=>s.bd==null&&!s.partner&&s.sex==='F');
      C.assign(ad[0],q2); C.assign(af[0],q2);
      for(let i=0;i<40;i++){ G.lastReal-=60*60000; C.advance(60*60000); G.res.food=1e5; G.res.water=1e5; G.res.power=1e5; }
      const d=G.settlers.find(s=>s.first==='Desmond'); if(d) C.removeSettler(d,'Heart attack');
      return 'pop '+G.settlers.length+' dead '+G.dead.length+' kids '+G.settlers.filter(s=>s.bd!=null).length; }"""))
    await pg.evaluate("()=>{ const C=window.__colony; C.UI.modal={t:'book',v:'trees'}; C.renderUI(); }")
    await pg.wait_for_timeout(1500); await pg.screenshot(path='book1.png')
    await pg.evaluate("()=>{ const C=window.__colony; const d=C.G.dead[0]; C.UI.modal={t:'settler',id:d.id,from:'book'}; C.renderUI(); }")
    await pg.wait_for_timeout(1200); await pg.screenshot(path='book2.png',full_page=True)
    await pg.evaluate("()=>{ const C=window.__colony; C.UI.modal={t:'book',v:'all'}; C.renderUI(); }")
    await pg.wait_for_timeout(1200); await pg.screenshot(path='book3.png')
    print(errs); await b.close()
asyncio.run(main())
