import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps=1e4; C.build('quarters',1,3); const q=G.rooms.find(r=>r.type==='quarters'&&r.col===3), ent=C.entRoom();
      const m=G.settlers.find(s=>s.sex==='M'&&!s.partner&&s.bd==null&&s.first!=='Desmond'), f=G.settlers.find(s=>s.sex==='F'&&!s.partner&&s.bd==null&&C.G.settlers.indexOf(s)>2);
      C.enlist(m,'soldier'); C.assign(m,ent); C.enlist(f,'soldier'); C.assign(f,ent);
      const o=['m to quarters '+C.assign(m,q)+' leave '+m.leavePost, 'f to quarters '+C.assign(f,q)];
      for(let i=0;i<60&&!f.preg;i++) C.lifeStepT(5);
      o.push('preg '+!!f.preg+' | m room '+(G.rooms.find(r=>r.id===m.room)||{}).type+' | f room '+(G.rooms.find(r=>r.id===f.room)||{}).type);
      return o.join(' | ')+' // '+G.log.slice(0,2).map(l=>l.m).join(' / '); }"""))
    print(errs); await b.close()
asyncio.run(main())
