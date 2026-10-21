import asyncio, os, json
from playwright.async_api import async_playwright
async def main():
  g=open('/mnt/user-data/uploads/Applications/ColonySim/saves/current.json').read()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:400]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const off=G.settlers.filter(s=>s.pol==='officer'), aux=G.settlers.filter(s=>s.pol==='aux');
      const civ=G.settlers.filter(s=>!s.pol&&!s.mil&&s.ec0!=null&&s.id!==G.leader).slice(0,8); for(const s of civ){ s.pol='officer'; s.polXP=30+Math.random()*60; }
      const all=G.settlers.filter(s=>s.pol==='officer'&&s.id!==G.leader); all.forEach((s,i)=>s.rank_p=[0,0,0,0,0,0,0,0,0,0,0,0][i]||0); for(const k of ['o_policesgt','o_policesgt']) C.addItem(k); C.polVacancyDay(); if(aux[0]) aux[0].rank_p=2;
      C.vacancyDay(); C.UI.modal={t:'pol'}; C.renderUI(); return 'officers '+all.length+' aux '+aux.length+' posts '+JSON.stringify(C.polOpenPosts().map(o=>[o.r,o.n,o.cap,o.c.map(x=>x.s.first+(x.why?'*':''))]))+' vac btns '+document.querySelectorAll('#modal [data-a=polPromo]').length; }"""))
    await pg.evaluate("()=>document.querySelector('[data-a=polTree]').click()"); await pg.wait_for_timeout(1200)
    await pg.locator('#modal .dlg').screenshot(path='poltree.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
