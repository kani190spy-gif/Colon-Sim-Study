import asyncio, os, json
from playwright.async_api import async_playwright
async def main():
  g=open('/mnt/user-data/uploads/Applications/ColonySim/saves/current.json').read()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:400])); pg.on('console',lambda m: errs.append('console:'+m.text[:300]) if m.type=='error' and 'net::' not in m.text else None)
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps+=9000; G.graceUntil=0; const out=[]; out.push('pur '+C.build('purifier',6,0)+' '+C.build('purifier',6,1)+' exec '+C.build('execc',6,2));
      const r=G.rooms.find(x=>x.type==='purifier'); out.push('w '+r.w); const free=G.settlers.filter(s=>s.ec0!=null&&!s.mil&&!s.pol&&s.id!==G.leader&&s.room&&!['phall','office'].includes(C.roomAt?'':'' )).slice(0,4); for(const s of free) C.assign(s,r);
      out.push('workers '+r.workers.length); C.UI.modal=null; G.gate=[]; C.renderUI(); window.dispatchEvent(new Event('resize'));
      const L=G.settlers.find(s=>s.id===G.leader); out.push('leader party '+L.party+' likes current '+C.flagLike(L.party,G.flag||null).toFixed(2));
      out.push('likes nat tpl '+['com','mkt','nat','civ'].map(k=>k+':'+C.flagLike(k,C.FL_TPL.nat[0]).toFixed(2)).join(' '));
      return out.join(' | ');}"""))
    await pg.wait_for_timeout(12000)
    await pg.locator('canvas').first.screenshot(path='pur.png')
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal=null; C.renderUI(); document.querySelector('[data-a=flagEdit]')||0; C.UI.tab='council'; C.renderUI();}")
    await pg.evaluate("()=>document.querySelector('[data-a=flagEdit]').click()"); await pg.wait_for_timeout(300)
    for sel in ["[data-a=flLay][data-v=canton]","[data-a=flCol][data-i='0'][data-v='#2e7a4a']","[data-a=flEm][data-v=dove]","[data-a=flEc][data-v='#f2efe6']"]:
      await pg.evaluate("s=>{document.querySelector(s).click(); window.__colony.renderUI();}", sel); await pg.wait_for_timeout(150)
    await pg.locator('#modal .dlg').screenshot(path='flagmodal.png')
    await pg.evaluate("()=>{document.querySelector('[data-a=flRef]').click();}")
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const R=G.ref; if(!R) return 'no ref'; for(let i=0;i<60&&G.ref;i++){ G.dayFrac+=.03; if(G.dayFrac>=1){G.dayFrac-=1;G.day++;} C.refStep(); } return 'ref done '+JSON.stringify(G.refHist&&G.refHist.slice(-1)[0]&&{yes:G.refHist.slice(-1)[0].yes,no:G.refHist.slice(-1)[0].no,pass:G.refHist.slice(-1)[0].pass})+' || '+G.log.slice(0,2).map(l=>l.m).join(' || ');}"""))
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const L=G.settlers.find(s=>s.id===G.leader); G.flag={lay:'h2',c:['#6a3a8a','#d97a2a'],em:'ring',ec:'#f2efe6'}; const lk=C.flagLike(L.party,G.flag); let n=0; for(let i=0;i<80&&n===0;i++){ G.day++; const before=JSON.stringify(G.flag); C.flagLeaderDay(); if(JSON.stringify(G.flag)!==before||G.ref) n=i+1; } return 'like '+lk.toFixed(2)+' leader acted after '+n+' days ref '+!!G.ref+' | '+G.log.slice(0,2).map(l=>l.m).join(' || ');}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal=null; C.UI.tab='council'; C.renderUI();}"); await pg.wait_for_timeout(300)
    await pg.locator('#tab').screenshot(path='flagbox.png')
    print(errs[:6]); await b.close()
asyncio.run(main())
