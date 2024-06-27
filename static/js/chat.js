// Fetch CSRF token from the cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
console.log(csrftoken);

document.getElementById('send-message-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Fetch CSRF token from the cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    const recipientId = document.getElementById('recipient').value;
    const subject = document.getElementById('subject').value;
    const body = document.getElementById('body').value;

    fetch('/api/messages/send/', { // Correct URL based on your patterns
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // Ensure you have the CSRF token
            },
            body: JSON.stringify({
                recipient_id: recipientId, // Use 'recipient_id' to match the backend
                subject: subject,
                body: body
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert('Message sent successfully!');
            // Optionally, clear the form or perform other actions
            // Clear the form fields
            document.getElementById('send-message-form').reset();
        })
        .catch(error => console.error('Error:', error));
});


function fetchMessages() {
    console.log('Fetching messages...');
    fetch('/api/messages/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // You should fetch the CSRF token as shown before
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(messages => {
            console.log('Messages received:', messages);
            const messagesContainer = document.getElementById('messages-container');
            if (!messagesContainer) {
                console.error('Messages container not found');
                return;
            }
            messagesContainer.innerHTML = ''; // Clear previous messages
            messages.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.className = 'card mb-3';
                messageElement.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${message.subject}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">From: ${message.sender}</h6>
                        <p class="card-text">${message.body}</p>
                        <small class="text-muted">${new Date(message.timestamp).toLocaleString()}</small>
                    </div>
                `;
                messagesContainer.appendChild(messageElement);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Call fetchMessages() when the page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document loaded');
    fetchMessages();
});

// 
function fetchSentMessages() {
    fetch('/api/messages/sent/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => response.json())
        .then(messages => {
            const sentMessagesContainer = document.getElementById('sent-messages-container');
            sentMessagesContainer.innerHTML = ''; // Clear previous messages
            messages.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.className = 'card mb-3';
                messageElement.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">${message.subject}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">To: ${message.recipient}</h6>
                    <p class="card-text">${message.body}</p>
                    <small class="text-muted">${new Date(message.timestamp).toLocaleString()}</small>
                </div>
            `;
                sentMessagesContainer.appendChild(messageElement);
            });
        })
        .catch(error => console.error('Error:', error));
}
// Call fetchMessages() when the page loads
document.addEventListener('DOMContentLoaded', fetchSentMessages);

// OBTAINING USERS
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/alluser/', { // Replace with your actual endpoint to get users
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // You should fetch the CSRF token as shown before
            },
        })
        .then(response => response.json())
        .then(users => {
            const recipientSelect = document.getElementById('recipient');
            users.forEach(user => {
                const option = document.createElement('option');
                option.value = user.id;
                option.textContent = `${user.first_name} ${user.last_name} ${user.is_staff}`; // Adjust based on your user model
                recipientSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
});