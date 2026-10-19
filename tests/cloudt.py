import asyncio, os, json
src=open('colony/index.html').read()
open('wrapped.html','w').write('<!doctype html><html><head><meta charset="utf-8"><style>[hidden]{display:none!important}body{margin:0}</style></head><body>'+src+'</body></html>')
MOCK="""window.__store=JSON.parse(window.name&&window.name.startsWith('{')?window.name:'{}');
window.claude={use:async n=>{ await new Promise(r=>setTimeout(r,300)); if(n==='db') return {doc:p=>({get:async()=>({exists:p in __store,data:()=>__store[p]}),set:async d=>{__store[p]=JSON.parse(JSON.stringify(d));}})}; if(n==='user') return {id:async()=>'u1'}; return null; }};"""
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    errs=[]
    # device A
    ca=await b.new_context(); await ca.add_init_script(MOCK); pa=await ca.new_page(); pa.on('pageerror',lambda e: errs.append('A '+str(e)))
    await pa.goto('file://'+os.path.abspath('wrapped.html')); await pa.wait_for_timeout(1500)
    print('A status', await pa.evaluate("()=>document.getElementById('cloudSt').textContent"))
    await pa.evaluate("()=>{const G=window.__colony.G; G.name='Haven Test'; G.res.caps=4242; }")
    await pa.evaluate("()=>{ document.dispatchEvent(new Event('visibilitychange')); }")  # not hidden -> pull; force push via save path:
    await pa.evaluate("()=>{ window.dispatchEvent(new Event('pagehide')); }"); await pa.wait_for_timeout(1500)
    print(await pa.evaluate("()=>[window.__colony.G.name,window.__colony.G.res.caps,window.__colony.G.savedAt]"))
    store=await pa.evaluate("()=>JSON.stringify(window.__store)")
    meta=json.loads(store).get('data/users/u1/save'); print('A pushed meta', meta and {k:meta[k] for k in ('n','z','name','pop')}, 'bytes', len(store))
    # device B (fresh, different localStorage) seeded with the store
    cb=await b.new_context(); await cb.add_init_script("window.name="+json.dumps(store)+";"+MOCK); pb=await cb.new_page(); pb.on('pageerror',lambda e: errs.append('B '+str(e)))
    await pb.goto('file://'+os.path.abspath('wrapped.html')); await pb.wait_for_timeout(2500)
    print('B', await pb.evaluate("()=>[window.__colony.G.name, window.__colony.G.res.caps, document.getElementById('cloudSt').textContent, document.getElementById('toast').textContent]"))
    print(errs); await b.close()
asyncio.run(main())
