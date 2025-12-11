const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('api', {
  // These functions will call the Python Flask API
  speak: async (text) => {
    const response = await fetch('http://localhost:5000/speak', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    return await response.json();
  },
  
  listen: async () => {
    const response = await fetch('http://localhost:5000/listen', {
      method: 'POST'
    });
    return await response.json();
  },
  
  startListening: async () => {
    const response = await fetch('http://localhost:5000/start', {
      method: 'POST'
    });
    return await response.json();
  },
  
  stopListening: async () => {
    const response = await fetch('http://localhost:5000/stop', {
      method: 'POST'
    });
    return await response.json();
  },
  
  checkStatus: async () => {
    const response = await fetch('http://localhost:5000/status');
    return await response.json();
  }
});