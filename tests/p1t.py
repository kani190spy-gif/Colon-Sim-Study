import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1300,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    for _ in range(3):
      if await pg.locator('[data-a=close]').count(): await pg.locator('[data-a=close]').first.click(); await pg.wait_for_timeout(300)
    async def click(a,v=None,id=None,i=None):
      await pg.evaluate("([a,v,id,i])=>{const el=document.createElement('button');el.dataset.a=a;if(v!=null)el.dataset.v=v;if(id!=null)el.dataset.id=id;if(i!=null)el.dataset.i=i;document.body.appendChild(el);el.click();el.remove();window.__colony.renderUI();}",[a,v,id,i]); await pg.wait_for_timeout(150)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const nc=G.settlers.filter(s=>s.cit&&s.cit!=='citizen'); return 'noncit tracks: '+nc.map(s=>s.first+':'+s.cit+'/'+s.citTrack).join(', ')+' | gate '+G.gate.length}"""))
    # make a gate visitor and accept with review
    await pg.evaluate("()=>{const C=window.__colony,G=C.G; if(!G.gate.length) G.gate.push(C.mkVisitor()); }")
    await click('accept','review',None,'0')
    print(await pg.evaluate("()=>{const G=window.__colony.G; const s=G.settlers[G.settlers.length-1]; return s.first+' '+s.cit+' track='+s.citTrack}"))
    # sprint
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal=null; C.UI.tab='study'; C.renderUI();}")
    await click('sprintGo','20'); await pg.evaluate("()=>{window.__colony.G.sprint.t0-=150000}"); await pg.wait_for_timeout(1200)
    await pg.locator('#tab').screenshot(path='sp1.png')
    await click('sprintDone'); print(await pg.evaluate("()=>window.__colony.G.log.slice(0,1).map(l=>l.m).join('')"))
    # wear
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const s=G.settlers.find(x=>x.mil==='soldier'); if(!s) return 'no soldier'; for(let i=0;i<60;i++){ C.dayStep(); } C.addWear(s,20,'Raid injuries'); C.UI.modal={t:'settler',id:s.id}; C.renderUI(); return s.first+' wear '+Math.round(s.wear)+' src '+JSON.stringify(s.wearSrc)}"""))
    await pg.wait_for_timeout(300); await pg.locator('#modal .dlg').screenshot(path='wear.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
