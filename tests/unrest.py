import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100},device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.inst.gov=1; const ad=G.settlers.filter(s=>s.bd==null); G.leader=ad[0].id; C.leaderSync();
      ad.forEach((s,i)=>{ if(i>=1&&i<=6){ s.happy=0; s.grief=80; if(i===1) s.s.C=8; } }); for(let d=0;d<4;d++){ G.day++; C.polDay(); }
      const F=G.pfac&&G.pfac.find(f=>!f.gone&&f.b==='reform'); if(!F) return 'no faction '+JSON.stringify(G.pfac);
      // force protest
      F.protCool=0; let tries=0; while(!G.protest&&tries<40){ C.unrestDay(); tries++; }
      const o=['faction '+F.name+' lvl '+F.lvl+' protest '+(!!G.protest)];
      window.__F=F; return o.join(' | '); }"""))
    await pg.wait_for_timeout(16000)
    box=await pg.evaluate("""()=>{ const cv=document.querySelector('canvas'); const R=cv.getBoundingClientRect(); return [R.left,R.top,R.width,R.height]; }""")
    x0,y0,w,h=box
    await pg.screenshot(path='protest.png',clip={'x':x0+w*0.3,'y':y0+h*0.22,'width':w*0.45,'height':h*0.28})
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; C.protestChoice('meet',true); G.dayFrac+=.2; C.protestStep();
      // plot
      const F=window.__F; F.lvl=3; F.hostDays=5; let t=0; while(!G.plot&&t<40){ C.unrestDay(); t++; } const P=G.plot; if(!P) return 'no plot';
      const real=P.by; G.day++; C.unrestDay(); const wrong=P.suspects.find(x=>x!==real); if(wrong) C.arrest(wrong); C.arrest(real);
      return 'plot handled; plot now '+JSON.stringify(G.plot)+' detained '+G.settlers.filter(s=>s.detained).map(s=>s.first+':'+s.detained.why).join(','); }"""))
    await pg.evaluate("()=>{ const C=window.__colony; C.UI.modal={t:'book',v:'hist'}; C.renderUI(); }"); await pg.wait_for_timeout(800)
    await pg.screenshot(path='hist.png')
    print(errs); await b.close()
asyncio.run(main())
