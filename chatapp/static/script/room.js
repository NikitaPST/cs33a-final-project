var chatSocket = null;

document.addEventListener('DOMContentLoaded', function () {
    const roomName = document.querySelector('#room').value;
    chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

    chatSocket.onerror = function (e) {
        console.error('connection error');
    }

    chatSocket.onopen = function () {
        chatSocket.onmessage = function (e) {
            const message = JSON.parse(e.data);
            if (message.type === 'message') {
                handleMessage(message.data);
            } else if (message.type === 'roomData') {
                handleRoomData(message.data);
            }
        }
    }

    document.querySelector('#tbMessage').addEventListener('keyup', handleMessageChange);
    document.querySelector('#btnSend').addEventListener('click', handleSend);
});

function handleMessage(msg) {
    const messageTemplate = document.querySelector('#message-template').innerHTML;
    let html = Mustache.render(messageTemplate, {
        username: msg.username,
        message: msg.text,
        createdAt: moment(msg.createdAt).format('h:mm a')
    });
    if (msg.username === 'Admin') {
        html = html.replace('class="message"', 'class="message admin"');
    }
    document.querySelector('#messages').insertAdjacentHTML('beforeend', html);
    autoscroll();
}

function handleRoomData(data) {
    const sidebarTemplate = document.querySelector('#sidebar-template').innerHTML;
    const html = Mustache.render(sidebarTemplate, {
        room: data.room,
        users: data.users
    });
    document.querySelector('#sidebar').innerHTML = html;
}

function handleMessageChange(event) {
    const msg = document.querySelector('#tbMessage').value;
    document.querySelector('#btnSend').disabled = !msg;

    if (event.keyCode === 13 && msg) {
        handleSend();
    }
}

function handleSend() {
    const messageInput = document.querySelector('#tbMessage');
    const sendButton = document.querySelector('#btnSend');

    let msg = messageInput.value;
    if (msg === '!location' || msg === '!weather') {
        if (!navigator.geolocation) {
            return alert('Geolocation is not supported by your browser.');
        }

        navigator.geolocation.getCurrentPosition((position) => {
            msg = `${msg} ${position.coords.latitude} ${position.coords.longitude}`;
            chatSocket.send(JSON.stringify({
                type: 'send_message',
                message: msg
            }));
        });
    } else {
        chatSocket.send(JSON.stringify({
            type: 'send_message',
            message: msg
        }));
    }

    messageInput.value = '';
    sendButton.disabled = true;
    messageInput.focus();
}

function autoscroll() {
    const messages = document.querySelector('#messages')
    const newMessage = messages.lastElementChild;

    const newMessageStyles = getComputedStyle(newMessage);
    const newMessageMargin = parseInt(newMessageStyles.marginBottom);
    const newMessageHeight = newMessage.offsetHeight + newMessageMargin;

    const visibleHeight = messages.offsetHeight;
    const containerHeight = messages.scrollHeight;
    const scrollOffset = messages.scrollTop + visibleHeight;

    if (containerHeight - newMessageHeight <= scrollOffset) {
        messages.scrollTop = messages.scrollHeight;
    }
}