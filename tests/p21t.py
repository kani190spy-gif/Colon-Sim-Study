import asyncio, os, json
from playwright.async_api import async_playwright
async def main():
  g=open('/mnt/user-data/uploads/Applications/ColonySim/saves/current.json').read()
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']); pg=await b.new_page(viewport={'width':1400,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:400])); pg.on('console',lambda m: errs.append('console:'+m.text[:300]) if m.type=='error' and 'net::' not in m.text else None)
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal=null; C.renderUI();}")
    await pg.dispatch_event('#musBtn','click'); await pg.wait_for_timeout(500)
    print(await pg.evaluate("""()=>{const M=window.__colony.MUS; const an=M.ctx.createAnalyser(); an.fftSize=2048; M.master.connect(an); window._an=an; return 'on '+M.on+' mood '+M.mood+' state '+M.ctx.state;}"""))
    rms=[]
    for i in range(8):
      await pg.wait_for_timeout(500)
      rms.append(await pg.evaluate("()=>{const a=window._an,d=new Float32Array(a.fftSize); a.getFloatTimeDomainData(d); let s=0,m=0; for(const x of d){s+=x*x; m=Math.max(m,Math.abs(x));} return [Math.sqrt(s/d.length).toFixed(3),m.toFixed(2)]}"))
    print('rms/peak', rms)
    await pg.evaluate("()=>window.__colony.musAnthem()"); await pg.wait_for_timeout(4000)
    print(await pg.evaluate("()=>{const M=window.__colony.MUS; return 'anthem '+JSON.stringify(M.anthem)+' bar '+M.bar}"))
    for mood in ['folk','night','tense','focus','somber']:
      await pg.evaluate("m=>{const M=window.__colony.MUS; M.anthem=null; M.mood=m; M.phrase=null; M.lastAnthem=Date.now();}", mood); await pg.wait_for_timeout(1500)
      print(mood, await pg.evaluate("()=>{const a=window._an,d=new Float32Array(a.fftSize); a.getFloatTimeDomainData(d); let s=0,m=0; for(const x of d){s+=x*x; m=Math.max(m,Math.abs(x));} return [Math.sqrt(s/d.length).toFixed(3),m.toFixed(2), window.__colony.MUS.mood]}"))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal={t:'menu'}; C.renderUI();}"); await pg.wait_for_timeout(400)
    await pg.locator('#modal .dlg').screenshot(path='music_menu.png')
    await pg.locator('header.top').screenshot(path='music_top.png')
    print(errs[:6]); await b.close()
asyncio.run(main())
