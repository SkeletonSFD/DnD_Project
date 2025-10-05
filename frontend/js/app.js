/**
 * Главная логика приложения D&D
 */

let socket = null;
let currentRoom = null;
let currentUser = null;
let userRole = null;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    // Проверяем авторизацию
    checkAuth();
    
    // Получаем роль пользователя
    userRole = localStorage.getItem('dnd_user_role');
    if (!userRole) {
        // Если роль не выбрана, перенаправляем на выбор роли
        window.location.href = 'role-select.html';
        return;
    }
    
    console.log('Роль пользователя:', userRole);
    
    // Настраиваем интерфейс в зависимости от роли
    setupRoleBasedUI();
    
    // Получаем данные пользователя
    currentUser = Storage.getUser();
    if (!currentUser) {
        try {
            currentUser = await API.get(API_CONFIG.ENDPOINTS.ME);
            Storage.setUser(currentUser);
        } catch (error) {
            console.error('Failed to get user data:', error);
            logout();
            return;
        }
    }
    
    // Отображаем имя пользователя
    document.getElementById('username').textContent = currentUser.username;
    
    // Инициализируем Socket.IO
    initSocket();
    
    // Привязываем обработчики
    document.getElementById('messageForm').addEventListener('submit', sendMessage);
});

// Инициализация Socket.IO
function initSocket() {
    const token = Storage.getToken();
    
    socket = io(API_CONFIG.SOCKET_URL, {
        auth: {
            token: token
        },
        transports: ['websocket', 'polling']
    });
    
    // Обработчики событий Socket.IO
    socket.on('connect', () => {
        console.log('✅ Connected to Socket.IO');
        showConnectionStatus('connected');
    });
    
    socket.on('disconnect', () => {
        console.log('❌ Disconnected from Socket.IO');
        showConnectionStatus('disconnected');
    });
    
    socket.on('connect_error', (error) => {
        console.error('Connection error:', error);
        showConnectionStatus('disconnected');
    });
    
    // Получение списка комнат
    socket.on('rooms_list', (data) => {
        updateRoomsList(data.rooms);
    });
    
    // Присоединение к комнате
    socket.on('room_joined', (data) => {
        currentRoom = data.room;
        document.getElementById('currentRoom').textContent = `Комната: ${data.room}`;
        document.getElementById('messageInput').disabled = false;
        document.querySelector('#messageForm button').disabled = false;
        
        // Очищаем чат
        document.getElementById('messagesArea').innerHTML = '';
        
        addSystemMessage(`Вы присоединились к комнате "${data.room}"`);
    });
    
    // Выход из комнаты
    socket.on('room_left', (data) => {
        if (currentRoom === data.room) {
            currentRoom = null;
            document.getElementById('currentRoom').textContent = 'Выберите комнату';
            document.getElementById('messageInput').disabled = true;
            document.querySelector('#messageForm button').disabled = true;
        }
    });
    
    // Новое сообщение
    socket.on('new_message', (data) => {
        addMessage(data);
    });
    
    // Системное сообщение
    socket.on('system_message', (data) => {
        addSystemMessage(data.message);
    });
    
    // Результат броска кубика
    socket.on('dice_result', (data) => {
        showDiceResult(data);
    });
    
    // Список пользователей онлайн
    socket.on('users_online', (data) => {
        updateOnlineUsers(data.users);
    });
    
    // Запрашиваем список комнат
    setTimeout(() => {
        socket.emit('get_rooms');
    }, 500);
}

// Показать статус подключения
function showConnectionStatus(status) {
    let existingStatus = document.querySelector('.connection-status');
    if (existingStatus) {
        existingStatus.remove();
    }
    
    const statusDiv = document.createElement('div');
    statusDiv.className = `connection-status ${status}`;
    
    const statusText = {
        connected: '🟢 Подключено',
        disconnected: '🔴 Отключено',
        connecting: '🟡 Подключение...'
    };
    
    statusDiv.textContent = statusText[status] || statusText.connecting;
    document.body.appendChild(statusDiv);
    
    // Автоматически скрываем через 3 секунды для успешного подключения
    if (status === 'connected') {
        setTimeout(() => {
            statusDiv.remove();
        }, 3000);
    }
}

// Обновление списка комнат
function updateRoomsList(rooms) {
    const roomsList = document.getElementById('roomsList');
    
    if (!rooms || rooms.length === 0) {
        roomsList.innerHTML = '<div class="text-center text-amber-900 text-sm">Нет доступных комнат</div>';
        return;
    }
    
    roomsList.innerHTML = rooms.map(room => `
        <div class="room-item ${currentRoom === room.name ? 'active' : ''}" onclick="joinRoom('${room.name}')">
            <div class="room-name">${room.name}</div>
            <div class="room-users">👥 ${room.users} ${getUsersWord(room.users)}</div>
        </div>
    `).join('');
}

// Обновление списка пользователей онлайн
function updateOnlineUsers(users) {
    const onlineUsers = document.getElementById('onlineUsers');
    
    if (!users || users.length === 0) {
        onlineUsers.innerHTML = '<div class="text-center text-amber-900 text-sm">Никого нет онлайн</div>';
        return;
    }
    
    onlineUsers.innerHTML = users.map(user => `
        <div class="user-item">
            <div class="user-status"></div>
            <div class="user-name">${user}</div>
        </div>
    `).join('');
}

// Создание комнаты
function createRoom() {
    const roomName = document.getElementById('roomNameInput').value.trim();
    
    if (!roomName) {
        alert('Введите название комнаты');
        return;
    }
    
    if (roomName.length < 3) {
        alert('Название комнаты должно содержать минимум 3 символа');
        return;
    }
    
    socket.emit('create_room', { room: roomName });
    document.getElementById('roomNameInput').value = '';
    
    // Автоматически присоединяемся к созданной комнате
    setTimeout(() => {
        joinRoom(roomName);
    }, 500);
}

// Присоединение к комнате
function joinRoom(roomName) {
    if (currentRoom === roomName) {
        return;
    }
    
    // Если уже в другой комнате, сначала выходим
    if (currentRoom) {
        socket.emit('leave_room', { room: currentRoom });
    }
    
    socket.emit('join_room', { room: roomName });
}

// Отправка сообщения
function sendMessage(event) {
    event.preventDefault();
    
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message || !currentRoom) {
        return;
    }
    
    socket.emit('send_message', {
        room: currentRoom,
        message: message
    });
    
    messageInput.value = '';
}

// Добавление сообщения в чат
function addMessage(data) {
    const messagesArea = document.getElementById('messagesArea');
    const isOwnMessage = data.username === currentUser.username;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-item ${isOwnMessage ? 'own-message' : ''}`;
    
    const time = new Date(data.timestamp || Date.now()).toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit'
    });
    
    messageDiv.innerHTML = `
        <div class="flex justify-between items-start">
            <span class="message-author">${data.username}</span>
            <span class="message-time">${time}</span>
        </div>
        <div class="message-text">${escapeHtml(data.message)}</div>
    `;
    
    messagesArea.appendChild(messageDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

// Добавление системного сообщения
function addSystemMessage(message) {
    const messagesArea = document.getElementById('messagesArea');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-item system-message';
    messageDiv.innerHTML = `<div class="message-text">${escapeHtml(message)}</div>`;
    
    messagesArea.appendChild(messageDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

// Бросок кубика
function rollDice(sides) {
    if (!currentRoom) {
        alert('Присоединитесь к комнате для броска кубиков');
        return;
    }
    
    // Анимация
    const diceResult = document.getElementById('diceResult');
    diceResult.className = 'dice-rolling mt-4 text-center text-xl font-bold text-amber-900';
    diceResult.textContent = '🎲';
    
    socket.emit('roll_dice', {
        room: currentRoom,
        sides: sides
    });
}

// Показать результат броска кубика
function showDiceResult(data) {
    const diceResult = document.getElementById('diceResult');
    diceResult.className = 'mt-4 text-center text-xl font-bold text-amber-900';
    diceResult.textContent = `🎲 ${data.username} бросил d${data.sides}: ${data.result}`;
    
    // Добавляем в чат
    addSystemMessage(`🎲 ${data.username} бросил d${data.sides} и выпало: ${data.result}`);
    
    // Очищаем через 5 секунд
    setTimeout(() => {
        diceResult.textContent = '';
    }, 5000);
}

// Вспомогательные функции
function getUsersWord(count) {
    if (count % 10 === 1 && count % 100 !== 11) {
        return 'игрок';
    } else if ([2, 3, 4].includes(count % 10) && ![12, 13, 14].includes(count % 100)) {
        return 'игрока';
    } else {
        return 'игроков';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Настройка интерфейса в зависимости от роли
 */
function setupRoleBasedUI() {
    const role = localStorage.getItem('dnd_user_role');
    const roomCode = localStorage.getItem('dnd_room_code');
    
    console.log('Настройка UI для роли:', role, 'Код комнаты:', roomCode);
    
    if (role === 'player') {
        // Для игрока: скрываем кнопку создания комнаты
        const createRoomSection = document.querySelector('#roomNameInput').parentElement;
        if (createRoomSection) {
            createRoomSection.style.display = 'none';
        }
        
        // Добавляем информационное сообщение
        const roomsPanel = document.querySelector('#roomsList').parentElement;
        const infoDiv = document.createElement('div');
        infoDiv.className = 'bg-blue-100 border-2 border-blue-600 rounded p-3 mb-4 text-sm text-blue-900';
        infoDiv.innerHTML = `
            <strong>🗡️ Режим игрока</strong><br>
            Вы можете присоединяться к существующим комнатам
        `;
        roomsPanel.insertBefore(infoDiv, roomsPanel.firstChild);
    } else if (role === 'master') {
        // Для мастера: добавляем информационное сообщение
        const roomsPanel = document.querySelector('#roomsList').parentElement;
        const infoDiv = document.createElement('div');
        infoDiv.className = 'bg-red-100 border-2 border-red-600 rounded p-3 mb-4 text-sm text-red-900';
        infoDiv.innerHTML = `
            <strong>🎭 Режим мастера</strong><br>
            Вы можете создавать и управлять комнатами
        `;
        roomsPanel.insertBefore(infoDiv, roomsPanel.firstChild);
        
        // Если есть код комнаты, автоматически создаем/присоединяемся к ней
        if (roomCode) {
            console.log('Автоматическое создание комнаты:', roomCode);
            // Ждем инициализации socket
            setTimeout(() => {
                if (socket && socket.connected) {
                    socket.emit('create_room', { room: roomCode });
                    setTimeout(() => {
                        joinRoom(roomCode);
                    }, 500);
                }
            }, 1000);
        }
    }
    
    // Добавляем кнопку смены роли в навигацию
    const nav = document.querySelector('.medieval-nav .container > div:last-child');
    const changeRoleBtn = document.createElement('button');
    changeRoleBtn.textContent = 'Сменить роль';
    changeRoleBtn.className = 'medieval-button-small px-4 py-2 rounded mr-2';
    changeRoleBtn.onclick = () => {
        if (confirm('Вы уверены, что хотите сменить роль? Вы выйдете из текущей комнаты.')) {
            localStorage.removeItem('dnd_user_role');
            localStorage.removeItem('dnd_room_code');
            window.location.href = 'role-select.html';
        }
    };
    nav.insertBefore(changeRoleBtn, nav.firstChild);
}

// Делаем функции глобальными
window.createRoom = createRoom;
window.joinRoom = joinRoom;
window.rollDice = rollDice;