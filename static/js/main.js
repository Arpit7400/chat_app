document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect();

    socket.on('connect', () => {
        console.log('Socket connected');
    });

    socket.on('message', data => {
        console.log('Received message:', data);

        displayMessage(data.sender_contact, data.sender_username, data.message);
    });

    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const connectForm = document.getElementById('connect-form');
    const connectedUsernameElement = document.getElementById('connected-username');
    
    connectForm.addEventListener('submit', event => {
        event.preventDefault();
        const receiverContact = document.getElementById('receiver_contact').value.trim();
        
        if (receiverContact !== '') {
            connectedUsernameElement.textContent = receiverContact;
            fetch(`/get_chat_history?receiver_contact=${receiverContact}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        clearChatMessages();
                        data.messages.forEach(message => {
                            displayMessage(message.sender_contact, message.sender_username, message.message);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error fetching chat history:', error);
                });
        }
    });

    sendButton.addEventListener('click', () => {
        const receiverContact = connectedUsernameElement.textContent;
        const message = messageInput.value.trim();

        if (message !== '') {
            sendMessage('{{ contact }}', receiverContact, '{{ username }}', message);
            messageInput.value = '';
        }
    });

    function sendMessage(senderContact, receiverContact, senderUsername, message) {
        const data = {
            sender_contact: senderContact,
            receiver_contact: receiverContact,
            sender_username: senderUsername,
            message: message
        };

        socket.emit('message', data); // Send the message to the server
        displayMessage(senderContact, senderUsername, message);
    }

    function displayMessage(contact, username, message) {
        const messagesDiv = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        
        const senderLabel = contact === '{{ contact }}' ? 'You' : username;
        messageDiv.innerHTML = `<strong>${senderLabel}: </strong>${message}`;
        
        messagesDiv.appendChild(messageDiv);
    }

    function clearChatMessages() {
        const messagesDiv = document.getElementById('chat-messages');
        messagesDiv.innerHTML = '';
    }
});
