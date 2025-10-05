/**
 * Логика выбора роли (Мастер/Игрок)
 */

// Проверка авторизации при загрузке
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    
    const user = Storage.getUser();
    if (user) {
        console.log('Пользователь:', user.username);
    }
});

let selectedRole = null;

/**
 * Выбор роли
 */
function selectRole(role) {
    selectedRole = role;
    
    // Сохраняем роль в localStorage
    localStorage.setItem('dnd_user_role', role);
    
    // Скрываем выбор роли
    document.getElementById('roleSelection').classList.add('hidden');
    
    // Показываем соответствующую панель
    if (role === 'master') {
        document.getElementById('masterPanel').classList.remove('hidden');
        console.log('Выбрана роль: Мастер');
    } else if (role === 'player') {
        document.getElementById('playerPanel').classList.remove('hidden');
        console.log('Выбрана роль: Игрок');
    }
}

/**
 * Возврат к выбору роли
 */
function backToRoleSelection() {
    selectedRole = null;
    localStorage.removeItem('dnd_user_role');
    
    // Показываем выбор роли
    document.getElementById('roleSelection').classList.remove('hidden');
    
    // Скрываем панели
    document.getElementById('masterPanel').classList.add('hidden');
    document.getElementById('playerPanel').classList.add('hidden');
    document.getElementById('codeGenerated').classList.add('hidden');
}

/**
 * ФУНКЦИИ ДЛЯ МАСТЕРА
 */

/**
 * Продолжить существующую историю
 */
function continueStory() {
    console.log('Продолжить историю');
    
    // TODO: Показать список существующих комнат мастера
    UI.showMessage('Загрузка ваших историй...', 'info');
    
    // Пока просто переходим в приложение
    setTimeout(() => {
        enterGame();
    }, 1000);
}

/**
 * Начать новую историю (создать новую комнату)
 */
function newStory() {
    console.log('Начать новую историю');
    
    // Генерируем код комнаты (6 символов)
    const roomCode = generateRoomCode();
    document.getElementById('roomCode').textContent = roomCode;
    
    // Сохраняем код комнаты
    localStorage.setItem('dnd_room_code', roomCode);
    
    // Показываем блок с кодом
    document.getElementById('codeGenerated').classList.remove('hidden');
    
    UI.showMessage('Код комнаты создан! Поделитесь им с игроками.', 'success');
}

/**
 * Генерация кода комнаты
 */
function generateRoomCode() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';
    for (let i = 0; i < 6; i++) {
        code += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return code;
}

/**
 * ФУНКЦИИ ДЛЯ ИГРОКА
 */

/**
 * Создать нового персонажа
 */
function createCharacter() {
    console.log('Создать нового персонажа');
    
    // TODO: Открыть форму создания персонажа
    UI.showMessage('Функция создания персонажа в разработке', 'info');
}

/**
 * Удалить персонажа
 */
function deleteCharacter() {
    console.log('Удалить персонажа');
    
    // TODO: Показать список персонажей для удаления
    UI.showMessage('Функция удаления персонажа в разработке', 'info');
}

/**
 * Подключиться к лобби (ввести код комнаты)
 */
function joinLobby() {
    console.log('Подключиться к лобби');
    
    // Показываем prompt для ввода кода
    const roomCode = prompt('Введите код комнаты:');
    
    if (roomCode && roomCode.trim()) {
        const code = roomCode.trim().toUpperCase();
        
        // Сохраняем код комнаты
        localStorage.setItem('dnd_room_code', code);
        
        UI.showMessage(`Подключение к комнате ${code}...`, 'success');
        
        // Переходим в игру
        setTimeout(() => {
            enterGame();
        }, 1000);
    } else {
        UI.showMessage('Код комнаты не введен', 'error');
    }
}

/**
 * ОБЩИЕ ФУНКЦИИ
 */

/**
 * Войти в игру (перейти на app.html)
 */
function enterGame() {
    const role = localStorage.getItem('dnd_user_role');
    const roomCode = localStorage.getItem('dnd_room_code');
    
    console.log('Вход в игру:', { role, roomCode });
    
    // Переходим на страницу приложения
    window.location.href = 'app.html';
}

/**
 * Контейнер для сообщений (если его нет на странице)
 */
if (!document.getElementById('messageContainer')) {
    const messageContainer = document.createElement('div');
    messageContainer.id = 'messageContainer';
    messageContainer.className = 'fixed top-4 right-4 z-50 hidden';
    messageContainer.innerHTML = `
        <div id="messageBox" class="p-4 rounded border-2 shadow-lg max-w-md">
            <!-- Сообщение будет здесь -->
        </div>
    `;
    document.body.appendChild(messageContainer);
}