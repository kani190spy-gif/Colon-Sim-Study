# Project rules
- Every published update bumps the version label next to the vault name by +0.1 (e.g. `>v6.9</span>` → `>v7.0</span>`) and the reply states the new version.
- The player is "above politics": the leader acts on their own style; the player can intervene and must be kept informed.
- Deaths in political crises are capped (principals + 1–3 others).
- Never break existing saves: add migrations in `migrate(g)` guarded by a version flag.
- Publish target: https://claude.ai/artifact/Mqf667qLwLYRzLjXYzjqp2 (same URL keeps cloud saves).

# Desktop app (primary platform)
- IMPORTANT: game files + saves live in ~/Applications/ColonySim/{app,saves} (macOS privacy blocks Electron from reading ~/Desktop). Update ~/Applications/ColonySim/app/index.html. The launcher `Colony Sim.app` and the runtime (`Install Runtime/Electron.app`) stay in ~/Desktop/ColonySim.
- Lives on the player's Mac at ~/Desktop/ColonySim: `Colony Sim.app` (launcher script) → `Electron.app` runtime (player unzipped `Install Runtime.zip`, so it sits in `Install Runtime/Electron.app`; the launcher also checks `./Electron.app`) → `app/` (main.js, preload.js, index.html, icon.png).
- Saves: `saves/current.json` (+ `saves/backups/`, one every 15 min, 40 kept). The game uses `window.desktop.load/save` when present.
- Build: `python3 tools/build_desktop.py` wraps `src/index.html` with a document shell and the boot screen into `desktop/app/index.html`; copy it to the Mac's `app/index.html` to update.
- The artifact build (src/index.html) is still published to the artifact link and keeps working on its own.

# Idea board (not built yet)
- Political parties (Communist / Capitalist / Nationalist / Civic) layered over factions; faith designation (M/C/O/X) feeds mild voting tendencies.
- Plagues/pandemics (1–7 deaths by severity and preparedness).
- Rarer Legendary/Mythic MVP spawns.
- Occasional boss raids that badly damage defense.
- Career health: frontline injuries shorten lifespan / slow healing / can kill.
- Timed Anki mode (start button; 10/20/50-card sprints).
- Intelligence agency: small corps of agents (smaller than police/military), surveillance, plot detection, counter-coup, can be abused by leaders.

# Temporary
- OB/GYN Oral Boards (v7.5) + "Operation Delivery Room" expansion (v7.6) live between `/* ===== OB/GYN ORAL BOARDS` and `END OB/GYN ORAL BOARDS ===== */` in src/index.html. Hooks outside the block: session button + obBox (study tab), `m.t==='ob'` modal, ob* click cases, gearHead OBM_DRAW/OBH_DRAW hooks, hijab/surgcap in COVERS_HAIR + gearHeadBack, mask accessory slot `gear.a` (holderOf/equip/gearItems/bonusOf/lookOf/slotTile/pickerHTML/aitem canvas/storage filter), `lootKeys()` (excludes `ITEMS[k].ob` from all other loot), removeSettler cause 'Died in the ruined hospital'. Each case = expedition (s.exp='ob', back 2 min after finishing). Exclusive loot (ob_/obm_/obw_) stays in saves even after removing the mode — keep the item/look/mask/hat defs if the mode is removed.
