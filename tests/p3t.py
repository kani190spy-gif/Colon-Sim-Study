import asyncio, os, json, base64, gzip, sys
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    for _ in range(3):
      if await pg.locator('[data-a=close]').count(): await pg.locator('[data-a=close]').first.click(); await pg.wait_for_timeout(300)
    weak=sys.argv[1] if len(sys.argv)>1 else '0'
    await pg.evaluate("""(weak)=>{const C=window.__colony,G=C.G; window.__forceBoss=true; G.lastBoss=null; C.startFight(); window.__forceBoss=false; const F=C.FIGHT; if(weak==='1'){ F.foes.forEach(f=>{f.hp*=2;f.max*=2;}); } if(weak==='2'){ F.resp=[]; F.foes.forEach(f=>{f.hp*=1.5;f.max*=1.5;}); } }""",weak)
    print(await pg.evaluate("()=>{const F=window.__colony.FIGHT; return F.name+' def '+F.def.length+' resp '+F.resp.length}"))
    shots=0
    for i in range(40):
      await pg.wait_for_timeout(4000)
      st=await pg.evaluate("()=>{const F=window.__colony.FIGHT; if(!F) return 'over'; const b=F.foes.find(f=>f.boss); return F.stage+' alive '+F.foes.filter(f=>!f.dead).length+' boss '+Math.round(b.hp)+'/'+Math.round(b.max)+' front '+(F.front?window.__colony.G.rooms.find(r=>r.id===F.front).type:'-')+' fl '+(b.a.l)}")
      print(i,st)
      if st.startswith('breach') and shots<2:
        await pg.screenshot(path=f'breach{shots}.png'); shots+=1
      if st=='over': break
    print(await pg.evaluate("()=>window.__colony.G.log.slice(0,8).map(l=>l.m).join('\\n')"))
    print(errs[:5]); await b.close()
asyncio.run(main())
