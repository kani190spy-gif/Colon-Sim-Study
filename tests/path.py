import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(800)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; G.res.caps=1e5; G.inst.health=3;
      for(let c=0;c<6;c++) if(!C.roomAt(0,c)) C.build('generator',0,c);
      const out=[]; const a={l:1,x:C.roomX(0)+60,y:0}; 
      out.push(JSON.stringify(G.rooms.filter(r=>r.floor===1).map(r=>[r.col,r.w])));
      // B2 left room -> B2 right edge col 5 (unbuilt?)
      return out.join(' | '); }"""))
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const R=(al,ax,tl,tx)=>JSON.stringify(C.routeVia(al,ax,0,tl,tx,0).map(p=>[Math.round(p.x),p.l]));
      return [R(1,C.roomX(0)+60,0,C.roomX(5)+60), R(0,C.roomX(5)+60,1,C.roomX(1)+60), R(0,C.roomX(5)+60,0,C.roomX(0)+60), 'ert '+C.G.settlers.length].join('\\n'); }"""))
    print(errs); await b.close()
asyncio.run(main())
