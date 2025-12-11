const listenBtn = document.getElementById('listenBtn');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const speakBtn = document.getElementById('speakBtn');
const statusText = document.getElementById('statusText');
const statusDot = document.getElementById('statusDot');
const outputDiv = document.getElementById('output');
const micAnimation = document.getElementById('micAnimation');

let messages = [];
let isListening = false;

// Check server status on load
async function checkServerStatus() {
  try {
    const result = await window.api.checkStatus();
    if (result.status === 'online') {
      statusText.textContent = 'Ready';
      statusDot.classList.add('active');
      listenBtn.disabled = false;
      startBtn.disabled = false;
    }
  } catch (error) {
    statusText.textContent = 'Server offline - Please wait...';
    setTimeout(checkServerStatus, 2000);
  }
}

checkServerStatus();

// Add message to chat
function addMessage(text, type = 'user') {
  messages.push({ text, type, time: new Date().toLocaleTimeString() });
  updateOutput();
}

function updateOutput() {
  if (messages.length === 0) {
    outputDiv.innerHTML = '<div class="loading">Waiting for commands...</div>';
    return;
  }
  
  let html = '';
  messages.forEach(msg => {
    const label = msg.type === 'user' ? 'You' : msg.type === 'jarvis' ? 'Jarvis' : 'System';
    html += `
      <div class="message ${msg.type}">
        <div class="message-label">${label} • ${msg.time}</div>
        <div>${msg.text}</div>
      </div>
    `;
  });
  
  outputDiv.innerHTML = html;
  outputDiv.scrollTop = outputDiv.scrollHeight;
}

// Listen once
listenBtn.addEventListener('click', async () => {
  listenBtn.disabled = true;
  statusText.textContent = '🎧 Listening...';
  micAnimation.classList.add('active');
  
  try {
    const result = await window.api.listen();
    
    if (result.status === 'success') {
      addMessage(result.text, 'user');
      statusText.textContent = 'Ready';
      
      // Check for wake word
      if (result.text.toLowerCase().includes('jarvis')) {
        await window.api.speak('Bola sir');
        addMessage('Bola sir', 'jarvis');
      }
    } else {
      addMessage(result.message, 'error');
      statusText.textContent = 'Error - Try again';
    }
  } catch (error) {
    addMessage('Failed to connect to voice server', 'error');
    statusText.textContent = 'Connection error';
  }
  
  micAnimation.classList.remove('active');
  listenBtn.disabled = false;
});

// Start continuous listening
startBtn.addEventListener('click', async () => {
  try {
    await window.api.startListening();
    isListening = true;
    statusText.textContent = '🎧 Continuous listening active';
    startBtn.disabled = true;
    stopBtn.disabled = false;
    listenBtn.disabled = true;
    micAnimation.classList.add('active');
    addMessage('Continuous listening started', 'jarvis');
  } catch (error) {
    addMessage('Failed to start listening', 'error');
  }
});

// Stop continuous listening
stopBtn.addEventListener('click', async () => {
  try {
    await window.api.stopListening();
    isListening = false;
    statusText.textContent = 'Ready';
    startBtn.disabled = false;
    stopBtn.disabled = true;
    listenBtn.disabled = false;
    micAnimation.classList.remove('active');
    addMessage('Continuous listening stopped', 'jarvis');
  } catch (error) {
    addMessage('Failed to stop listening', 'error');
  }
});

// Test speech
speakBtn.addEventListener('click', async () => {
  try {
    await window.api.speak('Hello, I am Jarvis. Your personal assistant.');
    addMessage('Hello, I am Jarvis. Your personal assistant.', 'jarvis');
  } catch (error) {
    addMessage('Speech test failed', 'error');
  }
});
