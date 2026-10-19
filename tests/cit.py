import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    for _ in range(3):
      if await pg.locator('[data-a=close]').count(): await pg.locator('[data-a=close]').first.click(); await pg.wait_for_timeout(300)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const out=[]; out.push('citizens '+G.settlers.filter(C.isCitizen).length+'/'+G.settlers.length);
      const ad=G.settlers.filter(s=>s.bd==null&&!s.mil&&!s.pol&&s.id!==G.leader);
      const a=ad[0], b=ad[1], c=ad[2]; C.makeResident(a); C.makeResident(b); C.makeResident(c,'probation'); b.loy=30;
      out.push('enlist resident: '+C.enlist(a,'soldier'));
      G.day+=7; C.citDay(); out.push('after 7d: a='+a.cit+' b='+b.cit+'/'+b.citState+' c='+c.citState);
      out.push('rec b '+JSON.stringify(C.citRec(b)));
      for(let i=0;i<12;i++){ G.day++; C.citDay(); } out.push('b grievance '+Math.round(b.citGr)+' threat '+b.leaveThreat+' detained '+!!b.detained);
      out.push('free cells: '+(G.rooms.filter(r=>r.type==='jail').length));
      return out.join('\\n')+'\\n'+G.log.slice(0,5).map(l=>l.m).join('\\n'); }"""))
    await pg.evaluate("()=>{ const el=document.createElement('button'); el.dataset.a='citOpen'; el.id='xx'; document.body.appendChild(el); }")
    await pg.click('#xx'); await pg.wait_for_timeout(600)
    await pg.locator('#modal').screenshot(path='citm.png')
    print(errs); await b.close()
asyncio.run(main())
