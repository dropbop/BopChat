document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    // Function to add a message to the chat
    function addMessage(text, isUser = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
        messageElement.textContent = text;
        
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Placeholder function for sending messages
    // Will be replaced with actual API call later
    async function sendMessage(text) {
        // Add user message to chat
        addMessage(text, true);
        
        // Clear input
        userInput.value = '';
        
        // For now, just echo the message
        // This will be replaced with LLM API call
        setTimeout(() => {
            addMessage(`You said: ${text}`);
        }, 500);
    }
    
    // Handle send button click
    sendButton.addEventListener('click', () => {
        const text = userInput.value.trim();
        if (text) {
            sendMessage(text);
        }
    });
    
    // Handle enter key
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            const text = userInput.value.trim();
            if (text) {
                sendMessage(text);
            }
        }
    });
});