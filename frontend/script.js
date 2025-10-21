
const API_URL = 'http://localhost:5001/api';
let currentMode = 'formal';
let isProcessing = false;

const chatContainer = document.getElementById('chat-container');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const modeSwitch = document.getElementById('mode-switch');
const clearBtn = document.getElementById('clear-chat');

document.addEventListener('DOMContentLoaded', () => {
    const savedMode = localStorage.getItem('chatMode');
    if (savedMode === 'funny') {
        modeSwitch.checked = true;
        currentMode = 'funny';
    }
    loadChatHistory();
    chatForm.addEventListener('submit', handleSubmit);
    modeSwitch.addEventListener('change', handleModeChange);
    clearBtn.addEventListener('click', handleClearChat);
    messageInput.addEventListener('input', handleInput);
    checkBackendConnection();
});

async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_URL}/health`);
    } catch (error) {
        console.log('Backend offline');
    }
}

// handling form submissions
async function handleSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message || isProcessing) return;

    // adding user message
    addMessage(message, 'user');
    messageInput.value = '';
    const typingId = showTypingIndicator();
    isProcessing = true;
    sendBtn.disabled = true;

    try {
        // server call to backend
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                mode: currentMode
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        removeTypingIndicator(typingId);

        // adding bot response
        addMessage(data.reply, 'bot', data.classification);

    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator(typingId);
        
        addMessage(
            "Sorry, I'm having trouble connecting. Please make sure the backend server is running.",
            'bot',
            'irrelevant'
        );
    } finally {
        isProcessing = false;
        sendBtn.disabled = false;
        messageInput.focus();
    }
}

function addMessage(text, sender, classification = 'safe') {
    const welcomeMsg = chatContainer.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    if (sender === 'bot' && classification !== 'safe') {
        messageDiv.classList.add(classification);
    }

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = text;

    messageDiv.appendChild(bubbleDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    saveChatHistory();
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot';
    typingDiv.id = 'typing-indicator';
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble typing-indicator';
    bubbleDiv.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;
    
    typingDiv.appendChild(bubbleDiv);
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return 'typing-indicator';
}

function removeTypingIndicator(id) {
    const typingDiv = document.getElementById(id);
    if (typingDiv) {
        typingDiv.remove();
    }
}

// handling mode change
function handleModeChange(e) {
    currentMode = e.target.checked ? 'funny' : 'formal';
    localStorage.setItem('chatMode', currentMode);
}

function handleClearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        chatContainer.innerHTML = `
            <div class="welcome-message">
                <h2>👋 Welcome!</h2>
                <p>I'm here to help answer your questions in a safe and respectful way.</p>
                <p>Try asking me anything! I'll keep our conversation appropriate.</p>
            </div>
        `;
        localStorage.removeItem('chatHistory');
    }
}

function handleInput(e) {
    // input handling if needed
}

function saveChatHistory() {
    const messages = [];
    chatContainer.querySelectorAll('.message').forEach(msg => {
        const bubble = msg.querySelector('.message-bubble');
        if (bubble && !bubble.classList.contains('typing-indicator')) {
            messages.push({
                text: bubble.textContent,
                sender: msg.classList.contains('user') ? 'user' : 'bot',
                classification: msg.classList.contains('offensive') ? 'offensive' : 
                               msg.classList.contains('irrelevant') ? 'irrelevant' : 'safe'
            });
        }
    });
    localStorage.setItem('chatHistory', JSON.stringify(messages));
}

function loadChatHistory() {
    const history = localStorage.getItem('chatHistory');
    if (history) {
        try {
            const messages = JSON.parse(history);
            if (messages.length > 0) {
                const welcomeMsg = chatContainer.querySelector('.welcome-message');
                if (welcomeMsg) {
                    welcomeMsg.remove();
                }
                messages.forEach(msg => {
                    addMessageWithoutSaving(msg.text, msg.sender, msg.classification);
                });
            }
        } catch (e) {
            console.error('Error loading chat history:', e);
        }
    }
}

function addMessageWithoutSaving(text, sender, classification = 'safe') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    if (sender === 'bot' && classification !== 'safe') {
        messageDiv.classList.add(classification);
    }

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = text;

    messageDiv.appendChild(bubbleDiv);
    chatContainer.appendChild(messageDiv);
}
