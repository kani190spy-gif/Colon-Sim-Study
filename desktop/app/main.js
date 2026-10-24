// Colony Sim desktop shell: one window, saves written to ../saves next to the app.
const { app, BrowserWindow, ipcMain, shell, Menu } = require('electron');
const path = require('path'), fs = require('fs');
app.setName('Colony Sim');
app.commandLine.appendSwitch('ignore-gpu-blocklist');
app.commandLine.appendSwitch('enable-gpu-rasterization');
const ROOT = path.join(__dirname, '..');
const SAVES = path.join(ROOT, 'saves'), BACK = path.join(SAVES, 'backups'), CUR = path.join(SAVES, 'current.json');
fs.mkdirSync(BACK, { recursive: true });
let lastBackup = 0;
ipcMain.on('load', e => { try { e.returnValue = fs.readFileSync(CUR, 'utf8'); } catch (err) { e.returnValue = null; } });
ipcMain.on('save', (e, data) => {
  try {
    if (typeof data !== 'string' || data.length < 100) { e.returnValue = false; return; }
    fs.writeFileSync(CUR + '.tmp', data); fs.renameSync(CUR + '.tmp', CUR);
    const now = Date.now();
    if (now - lastBackup > 15 * 60000) {
      lastBackup = now; const d = new Date(now), p = n => String(n).padStart(2, '0');
      fs.writeFileSync(path.join(BACK, `save-${d.getFullYear()}${p(d.getMonth()+1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}.json`), data);
      const all = fs.readdirSync(BACK).filter(f => f.endsWith('.json')).sort();
      for (const f of all.slice(0, Math.max(0, all.length - 40))) { try { fs.unlinkSync(path.join(BACK, f)); } catch (x) {} }
    }
    e.returnValue = true;
  } catch (err) { e.returnValue = false; }
});
// v12.4: extra vault slots 1 and 2 (slot 0 stays current.json)
const slotFile = n => path.join(SAVES, `slot${n}.json`);
const okSlot = n => n === 1 || n === 2;
let lastSlotBackup = {};
ipcMain.on('loadSlot', (e, n) => { try { e.returnValue = okSlot(n) ? fs.readFileSync(slotFile(n), 'utf8') : null; } catch (err) { e.returnValue = null; } });
ipcMain.on('saveSlot', (e, n, data) => {
  try {
    if (!okSlot(n) || typeof data !== 'string' || data.length < 100) { e.returnValue = false; return; }
    const f = slotFile(n); fs.writeFileSync(f + '.tmp', data); fs.renameSync(f + '.tmp', f);
    const now = Date.now();
    if (now - (lastSlotBackup[n] || 0) > 15 * 60000) {
      lastSlotBackup[n] = now; const d = new Date(now), p = x => String(x).padStart(2, '0');
      fs.writeFileSync(path.join(BACK, `slot${n}-${d.getFullYear()}${p(d.getMonth()+1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}.json`), data);
      const all = fs.readdirSync(BACK).filter(x => x.startsWith(`slot${n}-`)).sort();
      for (const x of all.slice(0, Math.max(0, all.length - 20))) { try { fs.unlinkSync(path.join(BACK, x)); } catch (y) {} }
    }
    e.returnValue = true;
  } catch (err) { e.returnValue = false; }
});
ipcMain.on('delSlot', (e, n) => { try { if (okSlot(n) && fs.existsSync(slotFile(n))) fs.renameSync(slotFile(n), path.join(BACK, `slot${n}-deleted-${Date.now()}.json`)); e.returnValue = true; } catch (err) { e.returnValue = false; } });
function create() {
  const win = new BrowserWindow({
    width: 1560, height: 980, minWidth: 900, minHeight: 600, backgroundColor: '#14110f', title: 'Colony Sim', show: false,
    webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, backgroundThrottling: false }
  });
  win.once('ready-to-show', () => win.show());
  win.webContents.setWindowOpenHandler(({ url }) => { shell.openExternal(url); return { action: 'deny' }; });
  win.loadFile(path.join(__dirname, 'index.html'));
  try { app.dock && app.dock.setIcon(path.join(__dirname, 'icon.png')); } catch (e) {}
}
Menu.setApplicationMenu(Menu.buildFromTemplate([
  { label: 'Colony Sim', submenu: [{ role: 'about' }, { type: 'separator' }, { role: 'hide' }, { role: 'hideOthers' }, { type: 'separator' }, { role: 'quit' }] },
  { label: 'Edit', submenu: [{ role: 'undo' }, { role: 'redo' }, { type: 'separator' }, { role: 'cut' }, { role: 'copy' }, { role: 'paste' }, { role: 'selectAll' }] },
  { label: 'View', submenu: [{ role: 'reload' }, { role: 'togglefullscreen' }, { type: 'separator' }, { role: 'resetZoom' }, { role: 'zoomIn' }, { role: 'zoomOut' }, { type: 'separator' }, { role: 'toggleDevTools' }] },
  { label: 'Window', submenu: [{ role: 'minimize' }, { role: 'zoom' }, { role: 'close' }] }
]));
app.whenReady().then(create);
app.on('window-all-closed', () => app.quit());
