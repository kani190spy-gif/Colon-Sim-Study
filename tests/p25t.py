import asyncio, os, json
from playwright.async_api import async_playwright
async def main():
  g=open('/mnt/user-data/uploads/Applications/ColonySim/saves/current.json').read()
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:400])); pg.on('console',lambda m: errs.append('console:'+m.text[:300]) if m.type=='error' and 'net::' not in m.text else None)
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps+=9000; G.floors=Math.max(G.floors,9); const out=[]; const spots=[[6,0],[6,2],[6,4],[7,0],[7,2]];
      for(const [f,c] of spots){ G.inst.gov=3; const ok=C.build('phall',f,c); out.push(ok); } const H=G.rooms.filter(r=>r.type==='phall'); H.forEach((r,i)=>r.design=[4,1,2,3][i]); C.UI.modal=null; G.gate=[]; C.renderUI(); window.dispatchEvent(new Event('resize')); return out.join(',')+' halls '+H.length;}"""))
    await pg.wait_for_timeout(2500)
    await pg.locator('canvas').first.screenshot(path='halls2.png')
    await pg.dispatch_event('#musBtn','click'); await pg.wait_for_timeout(300)
    await pg.evaluate("()=>{const M=window.__colony.MUS; const an=M.ctx.createAnalyser(); M.master.connect(an); window._an=an;}")
    for sid in []:
      await pg.evaluate("id=>{const C=window.__colony,M=C.MUS; M.anthem=null; M.song=null; M.step=0; C.musPlay(id);}", sid)
      vals=[]
      for i in range(4):
        await pg.wait_for_timeout(1000); vals.append(await pg.evaluate("()=>{const a=window._an,d=new Float32Array(a.fftSize); a.getFloatTimeDomainData(d); let s=0,m=0; for(const x of d){s+=x*x;m=Math.max(m,Math.abs(x));} return Math.sqrt(s/d.length).toFixed(3)+'/'+m.toFixed(2)}"))
      print(sid, await pg.evaluate("()=>JSON.stringify(window.__colony.MUS.song)"), vals)
    print(errs[:6]); await b.close()
asyncio.run(main())
