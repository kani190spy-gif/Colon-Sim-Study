import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1300})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.graceUntil=0; G.inst.health=Math.max(1,G.inst.health); G.res.caps+=5000; G.floors++; const f=G.floors-1;
      const out=[]; for(const [t,col] of [['farm',0],['farm',1],['cannery',2],['cistern',3],['purifier',4]]) out.push(t+':'+C.build(t,f,col));
      out.push('farm w '+G.rooms.find(r=>r.type==='farm').w);
      const free=G.settlers.filter(s=>s.ec0!=null&&!s.exp&&!s.mil&&!s.pol&&s.id!==G.leader).slice(0,10); let i=0; for(const r of G.rooms.filter(r=>['farm','cannery','cistern','purifier'].includes(r.type))) for(let k=0;k<2;k++) C.assign(free[i++],r);
      out.push('boost '+C.farmBoost()+' purify '+C.purifyQ().toFixed(2)+' caps rc '+C.rationCap()+' tc '+C.tankCap());
      G.res.food=900; G.res.water=900; C.reservesDay(); out.push('rations '+Math.round(G.rations)+' tank '+Math.round(G.tank)+' food '+Math.round(G.res.food)+' water '+Math.round(G.res.water));
      G.res.food=-5; G.res.water=-3; const r0=G.rations,t0=G.tank; C.reservesDraw(); out.push('draw: rations '+(r0-G.rations).toFixed(2)+' tank '+(t0-G.tank).toFixed(2)+' flags '+G.flags.food+'/'+G.flags.water);
      const s=free[0]; const e0=s.ec0; for(let d=0;d<200;d++){ G.day++; C.jobDriftDay(); } out.push('grumbles '+G.log.filter(l=>/transfer/.test(l.m)).length); out.push('drift '+s.first+' '+e0.toFixed(2)+'→'+s.ec0.toFixed(2)+' fit '+s.jobFit);
      return out.join(' | ')+' || '+G.log.slice(0,3).map(l=>l.m).join(' || ')}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal=null; C.G.gate=[]; C.renderUI(); window.dispatchEvent(new Event('resize'))}"); await pg.wait_for_timeout(800)
    cv=pg.locator('canvas').first; await cv.scroll_into_view_if_needed(); await pg.wait_for_timeout(500); await cv.screenshot(path='v93.png')
    print(await pg.evaluate("()=>{const C=window.__colony; if(!C.dayStep) return 'no dayStep'; for(let i=0;i<40;i++) C.dayStep(); return 'days ok '+C.G.settlers.length+' rations '+Math.round(C.G.rations)+' tank '+Math.round(C.G.tank);}")); await pg.wait_for_timeout(5000)
    print(errs[:5]); await b.close()
asyncio.run(main())
