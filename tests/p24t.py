import asyncio, os, json
from playwright.async_api import async_playwright
async def main():
  g=open('/mnt/user-data/uploads/Applications/ColonySim/saves/current.json').read()
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:400])); pg.on('console',lambda m: errs.append('console:'+m.text[:300]) if m.type=='error' and 'net::' not in m.text else None)
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps+=9000; const out=[]; const spots=[[6,0],[6,2],[6,4],[5,0]]; 
      for(const [f,c] of spots){ out.push('hall '+C.build('phall',f,c)); } const H=G.rooms.filter(r=>r.type==='phall'); out.push('parties '+H.map(r=>r.party).join(','));
      const h=H[0]; const non=G.settlers.find(s=>s.party&&s.party!==h.party&&!s.mil&&s.ec0!=null); out.push('non-member assign '+C.assign(non,h)); const mem=G.settlers.find(s=>s.party===h.party&&!s.mil&&!s.pol&&s.id!==G.leader); out.push('member assign '+C.assign(mem,h));
      mem.party=non.party; C.lifeStepTest&&0; return out.join(' | ');}"""))
    await pg.wait_for_timeout(1500)
    print(await pg.evaluate("()=>{const G=window.__colony.G; const h=G.rooms.find(r=>r.type==='phall'); return 'workers after leaving party '+h.workers.length+' | '+G.log.slice(0,2).map(l=>l.m).join(' || ')}"))
    await pg.evaluate("()=>{const C=window.__colony,G=C.G; G.gate=[]; C.UI.modal={t:'assign',id:G.rooms.find(r=>r.type==='phall').id}; C.renderUI();}"); await pg.wait_for_timeout(600)
    await pg.locator('#modal .dlg').screenshot(path='hallpanel.png')
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const j=G.rooms.find(r=>r.type==='jail'); j.holds='out'; const s=G.settlers.find(x=>x.ec0!=null&&!x.detained&&x.id!==G.leader); s.detained={why:'test',until:G.day+2,sent:2,day:G.day}; 
      const j2=G.rooms.filter(r=>r.type==='jail'); return 'jails '+j2.length+' holds '+j2.map(r=>r.holds||'both');}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal=null; C.renderUI(); window.dispatchEvent(new Event('resize'))}"); await pg.wait_for_timeout(2500)
    await pg.locator('canvas').first.screenshot(path='v104.png')
    await pg.dispatch_event('#musBtn','click'); await pg.wait_for_timeout(300)
    print(await pg.evaluate("()=>{const M=window.__colony.MUS; const an=M.ctx.createAnalyser(); M.master.connect(an); window._an=an; return 'music on '+M.on}"))
    lv=[]
    for i in range(6):
      await pg.wait_for_timeout(1000); lv.append(await pg.evaluate("()=>{const a=window._an,d=new Float32Array(a.fftSize); a.getFloatTimeDomainData(d); let s=0; for(const x of d) s+=x*x; return Math.sqrt(s/d.length).toFixed(3)}"))
    print('waves rms',lv)
    await pg.evaluate("()=>window.__colony.musAnthem()"); await pg.wait_for_timeout(3000)
    print(await pg.evaluate("()=>JSON.stringify(window.__colony.MUS.anthem)"))
    print(errs[:6]); await b.close()
asyncio.run(main())
