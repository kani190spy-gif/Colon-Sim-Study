#!/usr/bin/env python3
"""Build desktop/app/index.html from src/index.html: full HTML document plus a boot screen."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parents[1]
game = (root / 'src' / 'index.html').read_text()
title = re.search(r'<title>.*?</title>', game).group(0)
body = game.replace(title, '')
boot = r'''
<style>
#boot{position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;
  background:radial-gradient(ellipse at 50% 40%,#2a2119 0%,#14110f 70%);color:#f1e9dc;font-family:Archivo,system-ui,sans-serif;transition:opacity .7s ease}
#boot.out{opacity:0;pointer-events:none}
#boot .door{width:190px;height:190px;filter:drop-shadow(0 10px 30px rgba(0,0,0,.6))}
#boot .gear{transform-origin:100px 100px;animation:bootspin 3.2s cubic-bezier(.6,.05,.3,1) infinite}
#boot .t{font-family:Bungee,Impact,sans-serif;font-size:38px;letter-spacing:.08em;color:#f2b83b;text-shadow:0 3px 0 #5a3f12}
#boot .v{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:13px;letter-spacing:.2em;color:#a59a8c;text-transform:uppercase}
#boot .bar{width:280px;height:6px;border-radius:4px;background:#2b241f;overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,.6)}
#boot .bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#d9a63a,#f2b83b);animation:bootbar 1.9s ease-out forwards}
#boot .tip{max-width:460px;text-align:center;font-size:14px;color:#cfc3b2;min-height:40px}
@keyframes bootspin{0%{transform:rotate(0)}60%{transform:rotate(300deg)}100%{transform:rotate(360deg)}}
@keyframes bootbar{to{width:100%}}
</style>
<div id="boot">
  <svg class="door" viewBox="0 0 200 200" aria-hidden="true">
    <circle cx="100" cy="100" r="96" fill="#3a3f44" stroke="#15110d" stroke-width="4"/>
    <g class="gear">
      <circle cx="100" cy="100" r="78" fill="#c9a23a" stroke="#15110d" stroke-width="4"/>
      <g fill="#15110d">''' + ''.join(f'<rect x="94" y="14" width="12" height="20" rx="2" transform="rotate({a} 100 100)"/>' for a in range(0,360,30)) + r'''</g>
      <circle cx="100" cy="100" r="54" fill="#6f7a83" stroke="#15110d" stroke-width="4"/>
      <circle cx="100" cy="100" r="40" fill="#8d98a2" stroke="#15110d" stroke-width="3"/>
    </g>
    <text x="100" y="114" text-anchor="middle" font-family="Bungee,Impact,sans-serif" font-size="38" fill="#f2b83b" stroke="#15110d" stroke-width="1.5">07</text>
  </svg>
  <div class="t">COLONY SIM</div>
  <div class="v" id="bootName">Opening the vault door…</div>
  <div class="bar"><i></i></div>
  <div class="tip" id="bootTip"></div>
</div>
<script>
(function(){ const tips=['Every correct answer on an expedition can turn up loot.','Soldiers guard the Armory and the Entrance; police run patrols from HQ.','Leaders govern by their own style: hawks, doves, populists and technocrats.','Approval is checked twice a game day. Long terms wear on any leader.','Rehabilitated raiders can earn citizenship after 18 days on probation.','Away for 45 minutes or more? Politics stays calm until you are back.','Children learn faster in school than adults do in training rooms.','The Memory Book keeps every life, family tree and leader on record.'];
  const el=document.getElementById('bootTip'); el.textContent=tips[Math.floor(Math.random()*tips.length)];
  try{ const r=window.desktop&&window.desktop.load(); if(r){ const m=r.match(/"name":"([^"]{1,40})"/); if(m) document.getElementById('bootName').textContent=m[1]+' · opening the vault door…'; } }catch(e){}
  const t0=performance.now();
  window.addEventListener('load',()=>{ const wait=Math.max(0,1900-(performance.now()-t0)); setTimeout(()=>{ const b=document.getElementById('boot'); b.classList.add('out'); setTimeout(()=>b.remove(),800); },wait); });
})();
</script>
'''
html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + title + \
  '<style>[hidden]{display:none!important}html,body{margin:0;background:#14110f}</style></head><body>\n' + boot + body + '\n</body></html>\n'
out = root / 'desktop' / 'app' / 'index.html'
out.write_text(html)
print('wrote', out, len(html))
