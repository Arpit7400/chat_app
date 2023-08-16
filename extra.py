# <!DOCTYPE html>
# <html lang="en">

# <head>
#   <!-- Include necessary meta tags, stylesheets, and title -->
# </head>

# <body>
#   <h2>Welcome to the Chat Room, {{ username }}</h2>
  
#   <!-- Include your chat interface here -->
  
#   <div id="chat-container">
#     <ul id="chat-messages"></ul>
#     <div class="d-flex">
#       <input type="text" id="message-input" class="form-control mr-2" placeholder="Type a message...">
#       <button id="send-button" class="btn btn-primary">Send</button>
#     </div>
#   </div>

#   <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.1.2/socket.io.js"></script>
#   <script>
#     const socket = io.connect();

#     const chatMessages = document.getElementById('chat-messages');
#     const messageInput = document.getElementById('message-input');
#     const sendButton = document.getElementById('send-button');

#     sendButton.addEventListener('click', () => {
#       const message = messageInput.value;
#       const senderContact = "{{ contact }}"; // Get the user's contact from Flask
#       const receiverContact = "receiver_contact"; // Define the receiver's contact here
#       const senderUsername = "{{ username }}"; 
#       socket.emit('message', {
#         sender_contact: senderContact,
#         receiver_contact: receiverContact,
#         message: message,
#         sender_username: senderUsername 
#       });
#       messageInput.value = '';  // Clear the input field
#     });

#     socket.on('message', (data) => {
#       const listItem = document.createElement('li');
#       listItem.textContent = `${data.sender_username}: ${data.message}`;
#       chatMessages.appendChild(listItem);
#     });
#   </script>
# </body>

# </html>



#### chat.html



# <!DOCTYPE html>
# <html lang="en">

# <head>
#   <!-- Include necessary meta tags, stylesheets, and title -->
# </head>

# <body>
#   <h2>Welcome to the Chat Room, {{ username }}</h2>
#   <div id="chat-messages">
#     {% for message in messages %}
#     <div>{{ message.sender_username }}: {{ message.message }}</div>
#   {% endfor %}

#   </div>
#   <div>
#     <input type="text" id="message-input" placeholder="Type a message...">
#     <button id="send-button">Send</button>
#   </div>
#   <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.1.2/socket.io.js"></script>
#   <script>
#     const socket = io.connect();

#     const chatMessages = document.getElementById('chat-messages');
#     const messageInput = document.getElementById('message-input');
#     const sendButton = document.getElementById('send-button');

#     sendButton.addEventListener('click', () => {
#       const message = messageInput.value;
#       if (message.trim() !== '') {
#         socket.emit('message', {
#           'sender_contact': '{{ contact }}', // Your sender contact
#           'receiver_contact': '{{ receiver_contact }}', // Other user's contact
#           'message': message
#         });
#         messageInput.value = ''; // Clear the input field
#       }
#     });

#     socket.on('message', (data) => {
#       const messageElement = document.createElement('div');
#       messageElement.textContent = `${data.sender_username}: ${data.message}`;
#       chatMessages.appendChild(messageElement);
#     });
#   </script>
# </body>

# </html>






    
# @socketio.on('message')
# def handle_message(data):
#     sender_contact = data['sender_contact']
#     receiver_contact = data['receiver_contact']
#     room = f'{sender_contact}_{receiver_contact}'
    
#     sender = users_collection.find_one({'contact': sender_contact})
#     if sender:
#         sender_username = sender.get('username')
#     else:
#         sender_username = 'Unknown User'

#     message_data = {
#         'sender_contact': sender_contact,
#         'receiver_contact': receiver_contact,
#         'sender_username': sender_username,
#         'message': data['message'],
#         'timestamp': datetime.datetime.now()
#     }
    
#     messages_collection.insert_one(message_data)

#     emit('message', {
#         'message': data['message'],
#         'sender_username': sender_username
#     }, room=room)




# @app.route('/chat')
# def chat():
#     contact = session.get('contact')
#     user = users_collection.find_one({'contact': contact})
    
#     if user:
#         username = user.get('username')
#         messages = list(messages_collection.find({
#             '$or': [
#                 {'sender_contact': contact},
#                 {'receiver_contact': contact}
#             ]
#         }).sort('timestamp'))
#         return render_template('chat.html', username=username, contact=contact, receiver_contact='other_user_contact', messages=messages)
#     else:
#         return redirect(url_for('login'))

# @app.route('/chat', methods=['GET', 'POST'])
# def chat():
#     contact = session.get('contact')
#     user = users_collection.find_one({'contact': contact})

#     if user:
#         username = user.get('username')

#         if request.method == 'POST':
#             receiver_contact = request.form.get('receiver_contact')
#             return redirect(url_for('chat', contact=receiver_contact))

#         receiver_contact = request.args.get('contact')  # Extract receiver's contact from query parameter
        
#         messages = list(messages_collection.find({
#             '$or': [
#                 {'sender_contact': contact, 'receiver_contact': receiver_contact},
#                 {'sender_contact': receiver_contact, 'receiver_contact': contact}
#             ]
#         }).sort('timestamp'))

#         return render_template('chat.html', username=username, contact=contact, receiver_contact=receiver_contact, messages=messages)
#     else:
#         return redirect(url_for('login'))


# having same connect and send button

# <!DOCTYPE html>
# <html lang="en">

# <head>
#     <!-- Include necessary meta tags, stylesheets, and title -->
# </head>

# <body>
#     <div class="container">
#         <h2>Welcome to the Chat Room, {{ username }}</h2>
#         <div id="chat-messages">
#             {% for message in messages %}
#             {% if message.sender_contact == contact %}
#             <div class="my-message">
#                 <strong>You: </strong>{{ message.message }}
#             </div>
#             {% else %}
#             <div class="other-message">
#                 <strong>{{ message.sender_username }}: </strong>{{ message.message }}
#             </div>
#             {% endif %}
#             {% endfor %}
#         </div>
#         <form id="message-form" class="form-inline">
#             <div class="form-group">
#                 <input type="text" class="form-control" id="message-input" placeholder="Type your message...">
#             </div>
#             <button type="button" class="btn btn-primary" id="send-button">Send</button>
#         </form>

#         <!-- New form to connect with other user -->
#         <form id="connect-form" class="form-inline mt-3" method="post" action="/chat">
#             <div class="form-group">
#                 <label for="receiver_contact">Connect with:</label>
#                 <input type="text" class="form-control" id="receiver_contact" name="receiver_contact"
#                        placeholder="Enter contact/user ID">
#             </div>
#             <button type="submit" class="btn btn-success" id="connect-button">Connect</button>
#         </form>
#     </div>
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.1.2/socket.io.js"></script>
#     <script>
#         const socket = io.connect();

#         socket.on('message', (data) => {
#             const messagesDiv = document.getElementById('chat-messages');
#             const newMessage = document.createElement('div');
#             newMessage.className = data.sender_username === '{{ username }}' ? 'my-message' : 'other-message';
#             newMessage.innerHTML = `<strong>${data.sender_username}: </strong>${data.message}`;
#             messagesDiv.appendChild(newMessage);
#         });

#         document.getElementById('message-form').addEventListener('submit', function (event) {
#             event.preventDefault();

#             const messageInput = document.getElementById('message-input');
#             const message = messageInput.value.trim();

#             if (message !== '') {
#                 socket.emit('message', {
#                     sender_contact: '{{ contact }}',
#                     receiver_contact: '{{ receiver_contact }}',
#                     message: message
#                 });
#                 messageInput.value = '';
#             }
#         });
#     </script>
# </body>

# </html>


#aving /get_username



# <!DOCTYPE html>
# <html lang="en">

# <head>
#     <!-- Include necessary meta tags, stylesheets, and title -->
# </head>

# <body>
#     <div class="container">
#         <h2>Welcome to the Chat Room, {{ username }}</h2>

#         <!-- New form to connect with other user -->
#         <form id="connect-form" class="form-inline mt-3" method="post" action="/chat">
#             <div class="form-group">
#                 <label for="receiver_contact">Connect with:</label>
#                 <input type="text" class="form-control" id="receiver_contact" name="receiver_contact"
#                        placeholder="Enter contact/user ID">
#             </div>
#             <button type="submit" class="btn btn-success" id="connect-button">Connect</button>
#         </form>

#         <div id="connected-user">
#             <strong>Connected User: </strong><span id="connected-username"></span>
#         </div>

#         <div id="chat-messages">
#             {% for message in messages %}
#             {% if message.sender_contact == contact %}
#             <div class="my-message">
#                 <strong>You: </strong>{{ message.message }}
#             </div>
#             {% else %}
#             <div class="other-message">
#                 <strong>{{ message.sender_username }}: </strong>{{ message.message }}
#             </div>
#             {% endif %}
#             {% endfor %}
#         </div>

#         <form id="message-form" class="form-inline mt-3">
#             <div class="form-group">
#                 <input type="text" class="form-control" id="message-input" placeholder="Type your message...">
#             </div>
#             <button type="button" class="btn btn-primary" id="send-button">Send</button>
#         </form>
#     </div>
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.1.2/socket.io.js"></script>
#     <script>
#         const socket = io.connect();

#         socket.on('message', (data) => {
#             const messagesDiv = document.getElementById('chat-messages');
#             const newMessage = document.createElement('div');
#             newMessage.className = data.sender_username === '{{ username }}' ? 'my-message' : 'other-message';
#             newMessage.innerHTML = `<strong>${data.sender_username}: </strong>${data.message}`;
#             messagesDiv.appendChild(newMessage);
#         });

#         document.getElementById('message-form').addEventListener('submit', function (event) {
#             event.preventDefault();

#             const messageInput = document.getElementById('message-input');
#             const message = messageInput.value.trim();

#             if (message !== '') {
#                 socket.emit('message', {
#                     sender_contact: '{{ contact }}',
#                     receiver_contact: '{{ receiver_contact }}',
#                     message: message
#                 });
#                 messageInput.value = '';
#             }
#         });

#         document.getElementById('connect-form').addEventListener('submit', function (event) {
#             event.preventDefault();

#             const connectContactInput = document.getElementById('receiver_contact');
#             const connectContact = connectContactInput.value.trim();

#             if (connectContact !== '') {
#                 // Fetch the connected user's username from the server
#                 fetch(`/get_username?contact=${connectContact}`)
#                     .then(response => response.json())
#                     .then(data => {
#                         if (data.success) {
#                             const connectedUsername = data.username;
#                             const connectedUsernameElement = document.getElementById('connected-username');
#                             connectedUsernameElement.textContent = connectedUsername;
#                         } else {
#                             console.log('User not found');
#                         }
#                     })
#                     .catch(error => {
#                         console.error('Error fetching username:', error);
#                     });
#             }
#         });
#     </script>
# </body>

# </html>


