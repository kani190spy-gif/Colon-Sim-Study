import asyncio, os
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':1000})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'TUNNEL' not in m.text else None)
    await pg.goto('file://'+os.path.abspath('wrapped.html')); await pg.wait_for_timeout(1000)
    print(await pg.evaluate("""()=>{const C=window.__colony,G=C.G; const vs=[]; for(let i=0;i<3;i++){ const v=C.mkVisitor(); if(i==0){v.gear={w:'pump',o:'leather'}; v.s.look.ghoul=true; v.s.look.scar='eye';} if(i==1){v.gear={w:'revolver'}; v.s.look.scar='cheek';} G.gate.push(v);} G.rooms.find(r=>r.type==='quarters').level=3; C.renderUI(); return G.gate.length;}"""))
    await pg.wait_for_timeout(800)
    await pg.click('[data-a=zoom][data-v="+"]'); await pg.click('[data-a=zoom][data-v="+"]'); await pg.evaluate("()=>{const w=document.getElementById('sceneWrap'); w.scrollTop=0; w.scrollLeft=0;}"); await pg.wait_for_timeout(600); await pg.locator('#sceneWrap').screenshot(path='gt1.png')
    await pg.locator('[data-a=accept]').first.click(); await pg.wait_for_timeout(800)
    await pg.screenshot(path='gt2.png')
    print(await pg.evaluate("()=>{const G=window.__colony.G; const s=G.settlers[G.settlers.length-1]; return JSON.stringify(s.gear)+' items '+G.items.length;}"))
    print(errs); await b.close()
asyncio.run(main())
