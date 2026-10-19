import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'TUNNEL' not in m.text else None)
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(1000)
    r=await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps=1e6; G.boost=3000; const out=[];
      // fill B1 for lift2
      ['trade','quarters','training'].forEach((t,i)=>{ if(!C.roomAt(0,3+i)) out.push('b'+C.build(t,0,3+i)); });
      const tr=G.rooms.find(r=>r.type==='training'); 
      const ad=G.settlers.filter(s=>!s.room); if(ad[0]) C.assign(ad[0].id,tr.id);
      const t0=G.lastReal; const step=m=>{ G.lastReal-=m*60000; C.advance(m*60000); };
      const preg=()=>G.settlers.filter(s=>s.preg).map(s=>s.first+':'+Math.round((s.preg.due-(G.day+G.dayFrac))*G.dayLen)+'m');
      for(let i=0;i<6;i++){ step(20); out.push('t+'+(i+1)*20+' preg '+preg().join(',')+' n='+G.settlers.length); }
      const kids=()=>G.settlers.filter(s=>s.bd!=null).map(s=>s.first+' age '+(Math.round(((G.day+G.dayFrac-s.bd)/s.kd*16)*10)/10)+' '+s.track+s.s[s.track]+' learn'+Math.round(s.learn||0));
      for(let i=0;i<5;i++){ step(30); out.push('k '+kids().join(' | ')); }
      out.push('train '+(ad[0]?ad[0].first+' '+tr.train+ad[0].s[tr.train]+' prog '+Math.round(ad[0].train):''));
      out.push(G.log.slice(0,8).map(l=>l.m).join(' // '));
      return out;}""")
    print('\n'.join(r))
    await pg.wait_for_timeout(1500)
    await pg.screenshot(path='l1.png')
    await pg.click('#sessBtn'); await pg.evaluate("()=>window.__colony.startFight()"); await pg.wait_for_timeout(1000)
    await pg.click('[data-a=bigview]'); await pg.wait_for_timeout(500)
    await pg.click('[data-a=watchFight]'); await pg.wait_for_timeout(12000)
    await pg.screenshot(path='l2.png')
    print(errs); await b.close()
asyncio.run(main())
