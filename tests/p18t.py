import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1300})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.graceUntil=0; G.inst.econ=Math.max(1,G.inst.econ); G.res.caps+=9000; G.floors++; const f=G.floors-1; const out=[];
      out.push('mine upper:'+C.build('mine',0,5)); for(const [t,col] of [['salvage',0],['coop',1],['generator',2],['bank',3],['bazaar',4],['refinery',5]]) out.push(t+':'+C.build(t,f,col)); G.floors++; out.push('mine:'+C.build('mine',G.floors-1,0));
      const free=G.settlers.filter(s=>s.ec0!=null&&!s.mil&&!s.pol&&s.id!==G.leader).slice(0,16); let i=0; for(const r of G.rooms.filter(r=>['salvage','coop','generator','bank','bazaar','refinery','mine'].includes(r.type)&&r.floor>=f)) for(let k=0;k<2;k++) C.assign(free[i++],r);
      const m0=JSON.stringify(G.mats), c0=G.res.caps; for(let d=0;d<10;d++){ G.day++; C.econDay(); }
      out.push('mats before '+m0+' after '+JSON.stringify(G.mats)+' caps +'+Math.round(G.res.caps-c0));
      const gen=G.rooms.find(r=>r.type==='generator'&&r.floor===f); out.push('coopNear gen '+C.coopNear(gen)); const mn=G.rooms.find(r=>r.type==='mine'); out.push('mine workers '+mn.workers.length+' acc '+JSON.stringify(mn._acc)+' bank '+JSON.stringify(G.rooms.find(r=>r.type==='bank')._acc));
      return out.join(' | ')+' || '+G.log.slice(0,2).map(l=>l.m).join(' || ')}"""))
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const bz=G.rooms.find(r=>r.type==='bazaar'); C.UI.modal={t:'assign',id:bz.id}; C.renderUI(); const b=document.querySelector('[data-a=bzBuy]'); if(!b) return 'no stall btn'; const k=b.dataset.v, n0=G.mats[k]||0; b.click(); return 'bought '+k+' '+n0+'→'+G.mats[k]; }"""))
    await pg.locator('#modal .dlg').screenshot(path='bazaar.png')
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const ws=G.rooms.find(r=>r.type==='workshop'); if(!ws) return 'no workshop'; ws.craft=null; G.mats.oil=20; const k=(G.bps||[]).find(k=>ITEMS[k]&&ITEMS[k].t==='w'); for(const m of Object.keys(G.mats)) G.mats[m]+=50; const ok=C.startCraft?C.startCraft(ws,k):'nf'; return 'craft '+ok+' fast '+(ws.craft&&ws.craft.fast)+' oil '+G.mats.oil; }"""))
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.inst.def=2; let ok=false; for(let f=0;f<G.floors&&!ok;f++) for(let c=0;c<5&&!ok;c++){ if(!C.roomAt(f,c)&&!C.roomAt(f,c+1)) ok=C.build('command',f,c); }
      const sol=G.settlers.filter(s=>s.mil==='soldier'&&s.id!==G.leader); sol.forEach((s,i)=>{ s.milXP=40+i*30; s.rank_m=2; }); for(const k of ['o_infsgt','o_infsgt']) C.addItem(k); C.vacancyDay(); C.UI.modal={t:'mil'}; C.renderUI(); return 'cmd '+ok+' log: '+G.log[0].m+' | btns '+document.querySelectorAll('[data-a=milPromo]').length+' | '+JSON.stringify(C.openPosts().map(o=>[o.r,o.n,o.cap,o.c.map(x=>x.s.first+(x.why?'*':''))]))}""")); await pg.locator('#modal .dlg').screenshot(path='vac.png')
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal=null; C.G.gate=[]; C.renderUI(); window.dispatchEvent(new Event('resize'))}"); await pg.wait_for_timeout(800)
    cv=pg.locator('canvas').first; await cv.scroll_into_view_if_needed(); await pg.wait_for_timeout(500); await cv.screenshot(path='v98.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
