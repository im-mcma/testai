document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('message-input');
    const button = document.getElementById('send-button');
    const chatArea = document.getElementById('chat-messages');

    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        messageDiv.textContent = content;
        chatArea.appendChild(messageDiv);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    async function sendMessage() {
        const message = input.value.trim();
        if (!message) return;
        
        addMessage('user', message);
        input.value = '';
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            if (data.reply) {
                addMessage('bot', data.reply);
            } else {
                addMessage('bot', 'خطا در دریافت پاسخ: ' + (data.error || 'ناشناخته'));
            }
        } catch (error) {
            addMessage('bot', 'خطا در ارتباط با سرور');
        }
    }

    button.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
