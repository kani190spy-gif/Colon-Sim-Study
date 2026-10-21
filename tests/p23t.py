import asyncio, os, json
from playwright.async_api import async_playwright
async def main():
  g=open('/mnt/user-data/uploads/Applications/ColonySim/saves/current.json').read()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:400]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const u=G.settlers.find(s=>s.first==='Una'&&s.last.startsWith('Mahm')); const gr=G.rooms.find(r=>r.type==='gameroom');
      const r0='edu '+JSON.stringify(u.edu)+' track '+u.track; C.assign(u,gr); u.track='L'; C.UI.modal={t:'settler',id:u.id}; C.renderUI();
      const tags=[...document.querySelectorAll('#modal .tag.g')].map(t=>t.textContent).filter(t=>/education/.test(t));
      return r0+' | after game room: track '+u.track+' edu '+JSON.stringify(u.edu)+' tags '+JSON.stringify(tags);}"""))
    print(errs[:5]); await b.close()
asyncio.run(main())
