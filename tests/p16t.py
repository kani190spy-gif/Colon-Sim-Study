import asyncio, os, json, base64, gzip
from playwright.async_api import async_playwright
async def main():
  d=json.load(open('cloud3/data/users/me/c0.json')); d=d.get('data',d); g=gzip.decompress(base64.b64decode(d['s'])).decode()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1300})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:300]))
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.graceUntil=0; G.inst.gov=3; G.res.caps+=5000; C.partyDay(); C.chairsDay();
      if(!G.rooms.some(r=>r.type==='assembly')){ let ok=false; for(let f=0;f<G.floors+2&&!ok;f++){ if(f>=G.floors) G.floors++; for(let c=0;c<5&&!ok;c++){ if(!C.roomAt(f,c)&&!C.roomAt(f,c+1)) ok=C.build('assembly',f,c); } } }
      const p=C.pollNow(); const ok=C.startVoting(); const V=G.vote; return 'cparty '+(V&&V.cparty)+' names '+(V&&V.cands.map(id=>G.settlers.find(s=>s.id===id).first))+' poll '+JSON.stringify(p.L.map(x=>[x.name,x.share.toFixed(2)]))+' council '+JSON.stringify(p.C.map(x=>[x.k,x.share.toFixed(2)]))+' | start '+ok+' party '+(V&&V.party)+' elig '+(V&&V.elig)+' will '+(V&&V.will.length)+' T '+(V&&V.T.toFixed(2))+' dur '+(V&&V.dur);}"""))
    await pg.evaluate("()=>{const C=window.__colony; C.UI.modal=null; C.G.gate=[]; C.UI.tab='elect'; C.renderUI();}")
    # advance game time by moving dayFrac forward in steps and stepping
    for i in range(12):
      await pg.evaluate("()=>{const C=window.__colony,G=C.G; if(!G.vote) return; G.dayFrac+=0.08; if(G.dayFrac>=1){G.dayFrac-=1; G.day++;} C.voteStep(); C.renderUI();}")
      await pg.wait_for_timeout(250)
      if i==3:
        await pg.wait_for_timeout(6000); cv=pg.locator('canvas').first; await cv.screenshot(path='elect_canvas.png'); print(await pg.evaluate("()=>{const V=window.__colony.G.vote; return V?Object.keys(V.going).join(','):'x'}"))
      if i==5:
        el=pg.locator('#tab'); await el.screenshot(path='elect_live.png')
        print(await pg.evaluate("()=>{const V=window.__colony.G.vote; return V?('cast '+V.cast+' going '+Object.keys(V.going).length+' L '+V.L+' C '+JSON.stringify(V.C)):'closed'}"))
    print(await pg.evaluate("()=>{const C=window.__colony,G=C.G; for(let i=0;i<40&&G.vote;i++){ G.dayFrac+=0.1; if(G.dayFrac>=1){G.dayFrac-=1;G.day++;} C.voteStep(); } const E=G.lastElection; return G.vote?'still open':JSON.stringify(E.turnout)+' '+E.results.map(r=>r.name+' '+r.votes).join(', ')+' council '+JSON.stringify(E.council)+' || '+G.log.slice(0,3).map(l=>l.m).join(' || ')}"))
    await pg.evaluate("()=>{const C=window.__colony; C.renderUI();}"); await pg.wait_for_timeout(300)
    await pg.locator('#tab').screenshot(path='elect_after.png')
    print(errs[:5]); await b.close()
asyncio.run(main())
