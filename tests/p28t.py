import asyncio, os, json
from playwright.async_api import async_playwright
async def main():
  g=open('/mnt/user-data/uploads/Applications/ColonySim/saves/current.json').read()
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1100})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)+(e.stack or '')[:400])); pg.on('console',lambda m: errs.append('console:'+m.text[:300]) if m.type=='error' and 'net::' not in m.text else None)
    await pg.add_init_script("localStorage.setItem('colony-sim-live',"+json.dumps(g)+");")
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(2500)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.graceUntil=0; G.ref=null; C.partyDay(); C.chairsDay(); const out=[];
      for(let i=0;i<8;i++){ G.day+=6; G.nextElection=G.day+5; C.pollDay(); const pl=C.pollNow(); out.push(JSON.stringify(G.campaign&&{run:G.campaign.run,end:G.campaign.endorse})+' poll '+pl.L.map(x=>x.party+':'+x.share.toFixed(2)).join(',')); }
      G.vote=null; C.startVoting(); out.push('vote cands '+G.vote.cparty+' endorse '+JSON.stringify(G.vote.endorse));
      for(let i=0;i<60&&G.vote;i++){ G.dayFrac+=.05; if(G.dayFrac>=1){G.dayFrac-=1;G.day++;} C.voteStep(); }
      out.push('result '+G.lastElection.results.map(r=>r.party+':'+r.votes).join(','));
      return out.join('\\n')+'\\n'+G.log.filter(l=>/endorses|back in the race/.test(l.m)).slice(0,4).map(l=>l.m).join('\\n');}"""))
    await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps+=5000; G.inst.econ=Math.max(1,G.inst.econ); let r=G.rooms.find(x=>x.type==='tailor'); if(!r){ for(const [f,c] of [[6,0],[6,1],[5,0],[0,4]]){ if(C.build('tailor',f,c)) break; } r=G.rooms.find(x=>x.type==='tailor'); } window._tl=r?[r.floor,r.col]:null;
      const free=G.settlers.filter(s=>s.ec0!=null&&!s.mil&&!s.pol&&s.id!==G.leader&&s.room).slice(0,4); for(const s of free) C.assign(s,r); C.UI.modal=null; G.gate=[]; C.renderUI(); window.dispatchEvent(new Event('resize'));}""")
    await pg.wait_for_timeout(30000); await pg.evaluate("()=>{window.__colony.G.dayFrac=.5;}"); await pg.wait_for_timeout(800)
    await pg.locator('canvas').first.screenshot(path='tailor.png'); print(await pg.evaluate('()=>JSON.stringify(window._tl)'))
    print(errs[:5]); await b.close()
asyncio.run(main())
