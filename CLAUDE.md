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
