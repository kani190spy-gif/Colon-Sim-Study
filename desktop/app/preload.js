const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('desktop', {
  isDesktop: true,
  load: () => ipcRenderer.sendSync('load'),
  save: (json) => ipcRenderer.sendSync('save', json),
  loadSlot: (n) => ipcRenderer.sendSync('loadSlot', n),
  saveSlot: (n, json) => ipcRenderer.sendSync('saveSlot', n, json),
  delSlot: (n) => ipcRenderer.sendSync('delSlot', n)
});
