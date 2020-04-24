document.addEventListener('DOMContentLoaded', function () {
    const roomName = document.querySelector('#room').value;
    const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

    chatSocket.onerror = function (e) {
        console.error('connection error');
    }

    chatSocket.onopen = function () {
        console.log('connected to server')
    }
});