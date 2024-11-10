// Choose the correct WebSocket protocol
const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
let socket = new WebSocket(protocol + window.location.host + '/ws/notifications/');

// When the connection is opened
socket.onopen = function (e) {
    console.log('WebSocket connection established');
};

// When a message is received
socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log('Notification received:', data.message);

    // Display the notification in the dropdown
    const notificationDropdown = document.getElementById('notifications-dropdown');
    const newNotification = document.createElement('li');
    newNotification.innerHTML = `<strong>New Notification:</strong> ${data.message}`;
    notificationDropdown.appendChild(newNotification);

    // Update notification count
    const notificationCount = document.getElementById('notification-count');
    let count = parseInt(notificationCount.textContent);
    notificationCount.textContent = count + 1;
};

// Handle WebSocket errors
socket.onerror = function (error) {
    console.error('WebSocket error:', error);
    alert('WebSocket connection error. Please refresh the page.');
};

// When the WebSocket connection is closed
socket.onclose = function (e) {
    console.log('WebSocket connection closed');
    setTimeout(function () {
        // Attempt to reconnect after 5 seconds
        socket = new WebSocket(protocol + window.location.host + '/ws/notifications/');
    }, 5000);
};
