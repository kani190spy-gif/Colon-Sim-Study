import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1300,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    for _ in range(3):
      if await pg.locator('[data-a=close]').count(): await pg.locator('[data-a=close]').first.click(); await pg.wait_for_timeout(300)
    async def click(a,v=None,id=None):
      await pg.evaluate("([a,v,id])=>{const el=document.createElement('button');el.dataset.a=a;if(v!=null)el.dataset.v=v;if(id!=null)el.dataset.id=id;document.body.appendChild(el);el.click();el.remove();window.__colony.renderUI();}",[a,v,id]); await pg.wait_for_timeout(100)
    shot=lambda n: pg.locator('#modal .dlg').screenshot(path=n)
    # bad run, no stims, many deaths stats
    res=await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const out={}; const ss=G.settlers.filter(s=>s.bd==null&&!s.preg);
      for(const q of [0,1]){ const s=ss[q]; for(let k=0;k<200;k++){ const c=C.OB_CASES[k%29]; const B=C.obBuild(c,'mc',-1); const hz=[]; for(const st of B.st){ if(st.type==='sel'){ st.opts.forEach((o,i)=>{ if(rndv()) st.pick[i]=true; }); } if(st.type==='sb') st.pick=0; if(st.type==='ord') st.seq=st.items.map((_,i)=>i); hz.push(...C.obGrade(st).hz); }
        const D=C.obDanger({hz,stims:q},s); out[q+D.fate]=(out[q+D.fate]||0)+1; } }
      function rndv(){ return Math.random()<.5; } return JSON.stringify(out); }""")
    print('random answering, 0 vs 1 stims (two settlers):',res)
    # mixed mode run through UI
    await pg.evaluate("()=>{window.__colony.G.ob.mcDone.pec=1}")
    await click('obPick','pec'); await click('obMode','mx')
    sid=await pg.evaluate("()=>{const G=window.__colony.G;return G.settlers.find(s=>s.sex==='M'&&!s.exp&&s.health>=50&&s.id!==G.leader&&s.bd==null&&!s.waiting).id}")
    await click('obSend',None,sid); await pg.fill('#obAns','headache, vision, RUQ pain'); await pg.click('[data-a=obSubmit]'); await pg.wait_for_timeout(150)
    await click('obChk','0'); await click('obChk','1'); await shot('x_free.png'); await click('obSubmit'); await click('obNext')
    for i in range(30):
      st=await pg.evaluate("""()=>{const R=window.__colony.G.ob.run; if(!R) return 'none'; const s=R.st[R.si]; if(s.type==='sb') s.pick=1; if(s.type==='ord') s.seq=s.items.map((_,i)=>i).reverse(); return s.type}""")
      if st=='none': break
      if st=='free':
        await click('obSubmit'); await click('obSubmit')
      else:
        await click('obSubmit')
        if st=='sb': await shot('x_sb.png')
      await click('obNext')
    await shot('x_done2.png')
    await pg.evaluate("()=>{const G=window.__colony.G; G.ob.trips.forEach(t=>t.back=0); window.__colony.obTick(); window.__colony.renderUI();}")
    print(await pg.evaluate("()=>window.__colony.G.log.slice(0,2).map(l=>l.m).join(' || ')"))
    # practice
    await click('obPr','vv'); await shot('x_pr.png')
    await click('obQuit')
    await click('obOpen','loot'); await shot('x_loot.png')
    await click('obOpen','guide'); await click('obG','5'); await shot('x_guide.png')
    # profile with mask slot
    await pg.evaluate("()=>{const C=window.__colony,G=C.G; const s=G.settlers.find(s=>s.sex==='F'&&s.bd==null&&!s.exp); const it=C.addItem('obm_venetian'); C.equip(s,'a',it.id); C.UI.modal={t:'settler',id:s.id}; C.renderUI();}")
    await pg.wait_for_timeout(400); await shot('x_prof.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
