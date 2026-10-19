import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1300,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+' '+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    for _ in range(3):
      if await pg.locator('[data-a=close]').count(): await pg.locator('[data-a=close]').first.click(); await pg.wait_for_timeout(300)
    async def click(a,v=None,id=None):
      await pg.evaluate("([a,v,id])=>{const el=document.createElement('button');el.dataset.a=a;if(v!=null)el.dataset.v=v;if(id!=null)el.dataset.id=id;document.body.appendChild(el);el.click();el.remove();window.__colony.renderUI();}",[a,v,id]); await pg.wait_for_timeout(120)
    shot=lambda n: pg.locator('#modal .dlg').screenshot(path=n)
    await click('obOpen','list'); await shot('x_list.png')
    await click('obPick','pph'); await click('obStims','1'); await shot('x_pick.png')
    sid=await pg.evaluate("()=>{const C=window.__colony,G=C.G;const s=G.settlers.find(s=>s.sex==='F'&&!s.exp&&!s.preg&&s.health>=50&&s.id!==G.leader&&s.bd==null&&!s.waiting&&!s.detained&&(Date.now()-0)); return s.id}")
    await click('obSend',None,sid)
    await shot('x_run0.png')
    # answer perfectly: pick all c/o, sb best, ord correct
    for i in range(30):
      st=await pg.evaluate("""()=>{const R=window.__colony.G.ob.run; if(!R) return 'none'; const s=R.st[R.si];
        if(s.type==='sel') s.opts.forEach((o,i)=>{ if(o.g==='c'||o.g==='o'||(o.g==='h'&&R.si===3)) s.pick[i]=true; });
        if(s.type==='sb') s.pick=s.opts.findIndex(o=>o.g==='b');
        if(s.type==='ord') s.seq=s.items.map((_,i)=>i);
        return s.type+':'+R.si+'/'+R.st.length}""")
      if st=='none': break
      await click('obSubmit')
      if i==3: await shot('x_rev.png')
      await click('obNext')
    await shot('x_done.png')
    print(await pg.evaluate("()=>JSON.stringify(window.__colony.G.ob.trips.map(t=>({fate:t.out.fate,hp:t.out.hp,loot:t.out.loot,lost:t.out.lost,ev:t.out.ev.length})))"))
    await pg.evaluate("()=>{const G=window.__colony.G; G.ob.trips.forEach(t=>t.back=0); window.__colony.obTick(); window.__colony.renderUI();}")
    await pg.wait_for_timeout(300); await shot('x_back.png')
    print(await pg.evaluate("()=>window.__colony.G.log.slice(0,3).map(l=>l.m).join(' || ')"))
    # mixed + practice builds for all cases and variants
    print(await pg.evaluate("""()=>{const C=window.__colony; let n=0, bad=[]; for(const c of C.OB_CASES){ const X=C.OB_X[c.id]||{}; for(let vi=-1; vi<(X.v?X.v.length:0); vi++){ for(const m of ['mc','mx','pr']){ const B=C.obBuild(c,m,vi); n+=B.st.length; for(const s of B.st){ if(s.type==='sel'&&!s.opts.some(o=>o.g==='c'||o.g==='o')) bad.push(c.id+vi+s.k); } } }
      // check variant del prefixes matched something
      if(X.v) X.v.forEach((v,vi)=>{ if(v.del) for(const k in v.del) for(const pfx of v.del[k]){ const st=c.st.find(s=>s.k===k); if(!st||!st.pts.some(p=>(p[0]==='!'?p.slice(1):p).startsWith(pfx))) bad.push('DEL '+c.id+' '+pfx); } }); }
      return n+' stages; bad: '+bad.join(', ')}"""))
    # equip all OB outfits on a woman & render sheet
    await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const ks=Object.keys(C.ITEMS||{}); }""")
    await click('close')
    print(errs[:5]); await b.close()
asyncio.run(main())
