import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1000},device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    print('new game:',await pg.evaluate("""()=>{const G=window.__colony.G; return JSON.stringify(G.rooms.map(r=>[r.type,r.floor,r.col,r.w]));}"""))
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps=1e5;
      // recreate the old layout: generator B1/1, water B1/2, rest of B1 full
      G.rooms=G.rooms.filter(r=>r.type!=='entrance'); const g=G.rooms.find(r=>r.type==='generator'), w=G.rooms.find(r=>r.type==='water'), d=G.rooms.find(r=>r.type==='diner');
      g.col=0; w.col=1; d.col=2; g.level=2; for(let c=3;c<6;c++) C.build('trade',0,c);
      const before=JSON.stringify({g:[g.floor,g.col,g.level,g.workers.length],w:[w.floor,w.col,w.workers.length]});
      C.ensureEntrance(); const e=C.entRoom();
      return before+' -> '+JSON.stringify({g:[g.floor,g.col,g.level,g.workers.length],w:[w.floor,w.col,w.workers.length],e:e&&[e.floor,e.col,e.w]})+' overlap:'+G.rooms.some(a=>G.rooms.some(b=>a!==b&&a.floor===b.floor&&a.col<b.col+(b.w||1)&&b.col<a.col+(a.w||1)))+' | '+G.log.slice(0,3).map(l=>l.t||l.m||l.msg||JSON.stringify(l).slice(0,90)).join(' // '); }"""))
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G,e=C.entRoom(); const d0=C.defense(); const ad=G.settlers.filter(s=>s.bd==null&&!s.preg); C.assign(ad[5],e); C.assign(ad[6],e); C.assign(ad[7],e);
      const d1=C.defense(); ad[3].intake=Date.now()+30000; ad[4].intake=Date.now()+30000; C.startFight(); const F=C.FIGHT; return 'guards '+e.workers.length+' def '+d0.toFixed(1)+'->'+d1.toFixed(1)+' defenders first: '+(F&&F.def.slice(0,2).every(id=>e.workers.includes(id))); }"""))
    await pg.wait_for_timeout(500)
    await pg.evaluate("()=>{ const C=window.__colony; C.FIGHT&&(C.FIGHT.foes.forEach(f=>{f.dead=true;})); }")
    await pg.wait_for_timeout(14000)
    box=await pg.evaluate("""()=>{ const cv=document.querySelector('canvas'); const R=cv.getBoundingClientRect(); return [R.left,R.top,R.width,R.height]; }""")
    x0,y0,w,h=box
    await pg.screenshot(path='ent.png',clip={'x':x0,'y':y0+h*0.22,'width':w*0.4,'height':h*0.3})
    print(errs); await b.close()
asyncio.run(main())
