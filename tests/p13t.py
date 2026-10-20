import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.graceUntil=0; G.inst.gov=3; G.res.caps+=5000;
      let ok=false; for(let f=0;f<G.floors+2&&!ok;f++){ if(f>=G.floors) G.floors++; for(let c=0;c<6&&!ok;c++){ if(!C.roomAt(f,c)) ok=C.build('execc',f,c); } }
      const r=G.rooms.find(x=>x.type==='execc'); const out=['built '+ok+' w '+(r&&r.w)+' workersMax '+(r&&r.level)];
      for(let i=0;i<4;i++){ G.day++; C.cabinetDay(); }
      out.push(Object.entries(G.cab).map(([k,v])=>k+':'+(v?C.secOf(k).first+'('+C.secB(k).toFixed(1)+')':'-')).join(' '));
      out.push('desks '+r.workers.length+' intel '+(G.rooms.find(x=>x.type==='intel')?C.secB('sdb'):'n/a'));
      const old=G.leader; const L2=G.settlers.find(s=>C.isCitizen(s)&&s.id!==old&&!Object.values(G.cab).includes(s.id)); G.leader=L2.id; G.day++; C.cabinetDay(); out.push('after new leader '+Object.values(G.cab).filter(Boolean).length+' atdesk '+Object.values(G.cab).filter(id=>id&&C.G.settlers.find(s=>s.id===id).room===r.id).length);
      return out.join(' | ')+' || '+G.log.slice(0,6).map(l=>l.m).join(' || ')}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.tab='cab'; C.renderUI();}"); await pg.wait_for_timeout(400)
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal=null; C.renderUI();}"); await pg.wait_for_timeout(300)
    await pg.evaluate("()=>{const C=window.__colony; C.G.gate=[]; C.renderUI();}"); el=pg.locator('h3:has-text("Executive Council")').first; await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(200); await el.evaluate('e=>e.parentElement.scrollIntoView()')
    await pg.screenshot(path='cab.png')
    cv=pg.locator('canvas').first; await pg.set_viewport_size({'width':1400,'height':1300}); await pg.evaluate('()=>window.dispatchEvent(new Event("resize"))'); await pg.wait_for_timeout(800); await cv.scroll_into_view_if_needed(); await pg.wait_for_timeout(500); await pg.evaluate("()=>{document.querySelectorAll('.modal-bg,.backdrop,.ov,.overlay').forEach(e=>e.remove())}"); await cv.screenshot(path='cab_room.png'); print(await pg.evaluate("()=>{const r=window.__colony.G.rooms.find(x=>x.type==='execc'); return [r.floor,r.col,r.w, document.querySelector('canvas').width]}"))
    await pg.evaluate("()=>{const C=window.__colony,G=C.G; const r=G.rooms.find(x=>x.type==='execc'); C.UI.camY=C.floorTop?C.floorTop(r.floor)-200:0;}")
    print(await pg.evaluate('''()=>{const C=window.__colony,G=C.G; G.cab.eco=null; for(const c of (G.council||[]).map(id=>G.settlers.find(s=>s.id===id)).filter(Boolean)) c.loy=5; G.approval=70; const a0=G.apBoost||0; G.day++; C.cabinetDay(); const r1='pop: boost '+((G.apBoost||0)-a0)+' eco '+G.cab.eco+' hold '+JSON.stringify(G.cabHold);
      G.approval=30; G.cab.hea=null; const h0=G.apHit||0; G.day++; C.cabinetDay(); return r1+' | unpop: hit '+((G.apHit||0)-h0)+' || '+G.log.slice(0,3).map(l=>l.m).join(' || ')}'''))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.tab='cab'; C.renderUI();}")
    v=await pg.evaluate("()=>{const o=document.querySelector('#secPick_eco option:nth-child(2)'); return o&&o.value}")
    await pg.select_option('#secPick_eco', v); await pg.dispatch_event('button[data-a=secSet][data-v=eco]','click'); await pg.wait_for_timeout(200)
    await pg.dispatch_event('button[data-a=secFire][data-v=def]','click'); await pg.wait_for_timeout(200)
    print(await pg.evaluate("()=>{const G=window.__colony.G; return 'eco '+G.cab.eco+' want '+%s+' def '+G.cab.def+' | '+G.log.slice(0,2).map(l=>l.m).join(' || ')}"%v))
    print(errs[:5]); await b.close()
asyncio.run(main())
