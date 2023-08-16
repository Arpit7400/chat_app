const socket = io.connect();

socket.on('connect', () => {
    console.log('Socket connected');
});

// socket.on('message', (data) => {
//     console.log('Received message:', data);
//     const messagesDiv = document.getElementById('chat-messages');
//     const newMessage = document.createElement('div');
//     newMessage.className = data.sender_username === '{{ username }}' ? 'my-message' : 'other-message';
//     newMessage.innerHTML = `<strong>${data.sender_username}: </strong>${data.message}`;
//     messagesDiv.appendChild(newMessage);
// });
socket.on('message', (data) => {
    console.log('Received message:', data);

    // Update the chat messages in the UI
    const messagesDiv = document.getElementById('chat-messages');
    // messagesDiv.innerHTML = ''; // Clear existing messages
    
    data.messages.forEach(message => {
        const messageDiv = document.createElement('div');
        const senderLabel = message.sender_contact === '{{ contact }}' ? 'You' : message.sender_username;
        messageDiv.innerHTML = `<strong>${senderLabel}: </strong>${message.message}`;
        messagesDiv.appendChild(messageDiv);
    });
});


// Event listener for sending messages when the form is submitted
document.getElementById('message-form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    console.log('Sending message...');
    const receiverContact = document.getElementById('connected-username').textContent;
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (message !== '') {
        socket.emit('message', {
            sender_contact: '{{ contact }}',
            receiver_contact: receiverContact,
            message: message
        });
            // Fetch and display updated chat history after sending a message
            fetch(`/get_chat_history?receiver_contact=${receiverContact}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const chatMessagesDiv = document.getElementById('chat-messages');
                    chatMessagesDiv.innerHTML = ''; // Clear existing messages

                    data.messages.forEach(message => {
                        const messageDiv = document.createElement('div');
                        const senderLabel = message.sender_contact === '{{ contact }}' ? 'You' : message.sender_username;
                        messageDiv.innerHTML = `<strong>${senderLabel}: </strong>${message.message}`;
                        chatMessagesDiv.appendChild(messageDiv);
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching chat history:', error);
            });
        messageInput.value = '';
    }
});

document.getElementById('connect-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const connectContactInput = document.getElementById('receiver_contact');
    const connectContact = connectContactInput.value.trim();

    if (connectContact !== '') {
        // Fetch the connected user's username from the server
        fetch(`/user_exists?contact=${connectContact}`)
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    const connectedUsername = data.username;
                    const connectedUsernameElement = document.getElementById('connected-username');
                    connectedUsernameElement.textContent = connectedUsername;

                    // Set the receiver_contact for sending messages
                    const sendButton = document.getElementById('send-button');
                    sendButton.setAttribute('data-receiver-contact', connectContact);

                    // Fetch and display chat history for the connected user
                    fetch(`/get_chat_history?receiver_contact=${connectContact}`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                const chatMessagesDiv = document.getElementById('chat-messages');
                                chatMessagesDiv.innerHTML = ''; // Clear existing messages

                                data.messages.forEach(message => {
                                    const messageDiv = document.createElement('div');
                                    const senderLabel = message.sender_contact === '{{ contact }}' ? 'You' : message.sender_username;
                                    messageDiv.innerHTML = `<strong>${senderLabel}: </strong>${message.message}`;
                                    chatMessagesDiv.appendChild(messageDiv);
                                });
                            }
                        })
                        .catch(error => {
                            console.error('Error fetching chat history:', error);
                        });
                } else {
                    console.log('User not found');
                }
            })
            .catch(error => {
                console.error('Error fetching username:', error);
            });
    }
});
