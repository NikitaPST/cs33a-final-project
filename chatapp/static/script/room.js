document.addEventListener('DOMContentLoaded', function () {
    const roomName = document.querySelector('#room').value;
    const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

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
});

function handleMessage(msg) {
    const messageTemplate = document.querySelector('#message-template').innerHTML;
    const html = Mustache.render(messageTemplate, {
        username: msg.username,
        message: msg.text,
        createdAt: moment(msg.createdAt).format('h:mm a')
    });
    document.querySelector('#messages').insertAdjacentHTML('beforeend', html);
    // autoscroll
}

function handleRoomData(data) {
    const sidebarTemplate = document.querySelector('#sidebar-template').innerHTML;
    const html = Mustache.render(sidebarTemplate, {
        room: data.room,
        users: data.users
    });
    document.querySelector('#sidebar').innerHTML = html;
}