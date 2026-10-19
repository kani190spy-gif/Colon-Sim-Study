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
    await click('obOpen','list'); await shot('y_list.png')
    # practice heg
    await click('obPr','heg')
    # pick 3 key + 1 junk in hx
    ids=await pg.evaluate("()=>{const s=window.__colony.G.ob.run.st[0]; return [s.ids.filter(x=>x[0]=='k').slice(0,3), s.ids.filter(x=>x[0]=='j').slice(0,1)].flat()}")
    for i in ids: await click('obAns',i)
    await shot('y_hx_mid.png'); await click('obEnough'); await shot('y_hx_rev.png'); await click('obNext')
    # run through rest: pick all keys then enough; sb pick best
    for i in range(40):
      t=await pg.evaluate("""()=>{const R=window.__colony.G.ob.run; if(!R) return 'none'; const s=R.st[R.si]; return s.type+(s.done?'D':'')+(s.pushed==='ask'?'P':'')}""")
      if t=='none': break
      if t.endswith('D'): await click('obNext'); continue
      if t=='sbP': await click('obStand'); continue
      if t.startswith('list'):
        ks=await pg.evaluate("()=>{const s=window.__colony.G.ob.run.st[window.__colony.G.ob.run.si]; return s.ids.filter(x=>x[0]=='k'&&!s.picked.includes(x))}")
        for k in ks[:-1]: await click('obAns',k)
        await click('obEnough')
      elif t.startswith('sb'):
        bi=await pg.evaluate("()=>{const s=window.__colony.G.ob.run.st[window.__colony.G.ob.run.si]; return s.opts.findIndex(o=>o.g==='b')}")
        await click('obAns',str(bi))
        if i==4: await shot('y_sb.png')
      elif t.startswith('ord'):
        n=await pg.evaluate("()=>{const s=window.__colony.G.ob.run.st[window.__colony.G.ob.run.si]; return s.items.length}")
        for k in range(n): await click('obAns',str(k))
    await shot('y_done_pr.png')
    # mock exam with settler
    await click('obMockGo'); await shot('y_mockpick.png')
    sid=await pg.evaluate("()=>{const G=window.__colony.G;return G.settlers.find(s=>!s.exp&&!s.preg&&s.health>=50&&s.id!==G.leader&&s.bd==null&&!s.waiting&&!s.detained).id}")
    await click('obSend',None,sid)
    await shot('y_mock0.png')
    for i in range(80):
      t=await pg.evaluate("""()=>{const R=window.__colony.G.ob.run; if(!R) return 'none'; const s=R.st[R.si]; return s.type+(s.done?'D':'')+(s.pushed==='ask'?'P':'')}""")
      if t=='none': break
      if t.endswith('D'): await click('obNext'); continue
      if t=='sbP': await click('obRethink'); continue
      if t.startswith('list'):
        ks=await pg.evaluate("()=>{const s=window.__colony.G.ob.run.st[window.__colony.G.ob.run.si]; const k=s.ids.filter(x=>x[0]=='k'); return k.slice(0,Math.ceil(k.length*.6)).concat(s.ids.filter(x=>x[0]=='j').slice(0,1))}")
        for k in ks: await click('obAns',k)
        await click('obEnough')
      elif t.startswith('sb'): await click('obAns','0')
      elif t.startswith('ord'):
        n=await pg.evaluate("()=>{const s=window.__colony.G.ob.run.st[window.__colony.G.ob.run.si]; return s.items.length}")
        for k in range(n): await click('obAns',str(k))
    await shot('y_done_mock.png')
    print(await pg.evaluate("()=>window.__colony.G.log.slice(0,1).map(l=>l.m).join('')"))
    print(errs[:5]); await b.close()
asyncio.run(main())
