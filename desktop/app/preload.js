const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('desktop', {
  isDesktop: true,
  load: () => ipcRenderer.sendSync('load'),
  save: (json) => ipcRenderer.sendSync('save', json)
});
