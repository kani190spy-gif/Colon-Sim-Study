import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1300})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G,ITEMS=C.ITEMS; G.graceUntil=0; G.inst.def=Math.max(1,G.inst.def); G.res.caps+=9000; const out=[];
      let ws=G.rooms.find(r=>r.type==='workshop'); if(!ws){ let ok=false; for(let f=0;f<G.floors+2&&!ok;f++){ if(f>=G.floors) G.floors++; for(let c=0;c<5&&!ok;c++){ if(!C.roomAt(f,c)&&!C.roomAt(f,c+1)) ok=C.build('workshop',f,c); } } ws=G.rooms.find(r=>r.type==='workshop'); }
      out.push('ws workers before '+ws.workers.map(id=>G.settlers.find(s=>s.id===id)?.mil||'civ').join(','));
      const civ=G.settlers.find(s=>!s.mil&&s.ec0!=null); out.push('civ assign '+C.assign(civ,ws));
      const sol=G.settlers.filter(s=>s.mil==='soldier'&&s.id!==G.leader).slice(0,3); for(const s of sol) C.assign(s,ws); out.push('crew3 speed '+C.wfSpeed(ws).toFixed(2));
      const more=G.settlers.filter(s=>!s.mil&&!s.pol&&s.ec0!=null&&s.id!==G.leader).slice(0,2); for(const s of more){ s.mil='soldier'; C.assign(s,ws); } out.push('crew '+ws.workers.length+' cap '+(ws.level)+' speed '+C.wfSpeed(ws).toFixed(2));
      const ks=Object.keys(ITEMS).filter(k=>ITEMS[k].t==='w'); const byT=[0,1,2,3,4,5].map(t=>ks.find(k=>ITEMS[k].tier===t)); out.push('hours '+byT.map(k=>k?Math.round(C.craftNeed(k)/60):'-').join('/'));
      const myth=ks.filter(k=>ITEMS[k].tier===5).map(k=>Math.round(C.craftNeed(k)/60)); out.push('mythic range '+Math.min(...myth)+'-'+Math.max(...myth));
      ws.craft=null; G.ammo=0; G.boost=1; C.ammoStep(180); out.push('ammo after 3h '+G.ammo);
      return out.join(' | ')}"""))
    # rescue
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const v=G.settlers.find(s=>!s.mil&&s.ec0!=null&&s.id!==G.leader); v.exp='hostage'; G.hostages=[{sid:v.id,boss:'The Iron Hounds',until:G.day+5,ransom:500}];
      C.UI.modal=null; C.UI.tab='study'; C.renderUI(); document.querySelector('[data-a=hostRescue]').click(); C.renderUI(); for(let i=0;i<3;i++){ document.querySelector('#modal .pick [data-a=rescPick]').click(); C.renderUI(); }
      const m=C.UI.modal; const odds=C.rescOdds(m.team.map(id=>G.settlers.find(s=>s.id===id))); document.querySelector('[data-a=rescGo]').click(); const h=G.hostages[0]; const team=h.rescue.ids.map(id=>G.settlers.find(s=>s.id===id)); 
      const r1='team '+team.map(s=>s.first+':'+s.exp).join(',')+' odds '+odds.toFixed(2); h.rescue.at=Date.now()-1; C.rescueStep(); return r1+' | after: hostages '+G.hostages.length+' | '+G.log.slice(0,2).map(l=>l.m).join(' || ');}"""))
    await pg.wait_for_timeout(500)
    print(errs[:5]); await b.close()
asyncio.run(main())
