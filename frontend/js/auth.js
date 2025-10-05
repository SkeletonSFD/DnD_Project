/**
 * Модуль аутентификации D&D Application
 */

// Переключение между формами входа и регистрации
function showTab(tab) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const tabs = document.querySelectorAll('.tab-button');
    
    tabs.forEach(t => t.classList.remove('active'));
    
    UI.hideMessage();
    
    if (tab === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        tabs[0].classList.add('active');
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        tabs[1].classList.add('active');
    }
}

// Обработка формы входа
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;
    const remember = document.getElementById('remember').checked;
    const submitButton = event.target.querySelector('button[type="submit"]');
    
    // Валидация
    if (!username || !password) {
        UI.showMessage('Пожалуйста, заполните все поля', 'error');
        return;
    }
    
    try {
        UI.setButtonLoading(submitButton, true);
        UI.hideMessage();
        
        // Отправляем данные в формате form-data (как требует OAuth2)
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.LOGIN}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Ошибка входа');
        }
        
        // Сохраняем токен
        Storage.setToken(data.access_token);
        Storage.setRememberMe(remember);
        
        // Получаем данные пользователя
        const userData = await API.get(API_CONFIG.ENDPOINTS.ME);
        Storage.setUser(userData);
        
        UI.showMessage('Добро пожаловать в королевство!', 'success');
        
        // Перенаправляем на страницу выбора роли через 1 секунду
        setTimeout(() => {
            window.location.href = 'role-select.html';
        }, 1000);
        
    } catch (error) {
        console.error('Login error:', error);
        UI.showMessage(error.message || 'Ошибка входа. Проверьте имя и пароль.', 'error');
    } finally {
        UI.setButtonLoading(submitButton, false);
    }
}

// Обработка формы регистрации
async function handleRegister(event) {
    event.preventDefault();
    
    const username = document.getElementById('registerUsername').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value;
    const passwordConfirm = document.getElementById('registerPasswordConfirm').value;
    const terms = document.getElementById('terms').checked;
    const submitButton = event.target.querySelector('button[type="submit"]');
    
    // Валидация
    if (!username || !email || !password || !passwordConfirm) {
        UI.showMessage('Пожалуйста, заполните все поля', 'error');
        return;
    }
    
    if (username.length < 3) {
        UI.showMessage('Имя должно содержать минимум 3 символа', 'error');
        return;
    }
    
    if (password.length < 8) {
        UI.showMessage('Пароль должен содержать минимум 8 символов', 'error');
        return;
    }
    
    // Проверка сложности пароля
    if (!/\d/.test(password)) {
        UI.showMessage('Пароль должен содержать хотя бы одну цифру', 'error');
        return;
    }
    
    if (!/[A-Z]/.test(password)) {
        UI.showMessage('Пароль должен содержать хотя бы одну заглавную букву', 'error');
        return;
    }
    
    if (!/[a-z]/.test(password)) {
        UI.showMessage('Пароль должен содержать хотя бы одну строчную букву', 'error');
        return;
    }
    
    if (password !== passwordConfirm) {
        UI.showMessage('Пароли не совпадают', 'error');
        return;
    }
    
    if (!terms) {
        UI.showMessage('Необходимо принять условия', 'error');
        return;
    }
    
    // Валидация email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        UI.showMessage('Неверный формат email', 'error');
        return;
    }
    
    try {
        UI.setButtonLoading(submitButton, true);
        UI.hideMessage();
        
        // Регистрация
        const registerData = {
            username: username,
            email: email,
            password: password,
            confirm_password: passwordConfirm
        };
        
        const response = await API.post(API_CONFIG.ENDPOINTS.REGISTER, registerData, { skipAuth: true });
        
        UI.showMessage('Регистрация успешна! Выполняется вход...', 'success');
        
        // Автоматический вход после регистрации
        setTimeout(async () => {
            try {
                const formData = new URLSearchParams();
                formData.append('username', username);
                formData.append('password', password);
                
                const loginResponse = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.LOGIN}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: formData
                });
                
                const loginData = await loginResponse.json();
                
                if (loginResponse.ok) {
                    Storage.setToken(loginData.access_token);
                    
                    const userData = await API.get(API_CONFIG.ENDPOINTS.ME);
                    Storage.setUser(userData);
                    
                    window.location.href = 'role-select.html';
                } else {
                    UI.showMessage('Регистрация успешна! Теперь войдите в систему.', 'success');
                    showTab('login');
                }
            } catch (error) {
                console.error('Auto-login error:', error);
                UI.showMessage('Регистрация успешна! Теперь войдите в систему.', 'success');
                showTab('login');
            }
        }, 1000);
        
    } catch (error) {
        console.error('Register error:', error);
        let errorMessage = 'Ошибка регистрации';
        
        if (error.message.includes('already registered')) {
            errorMessage = 'Пользователь с таким именем уже существует';
        } else if (error.message.includes('email')) {
            errorMessage = 'Email уже используется';
        } else {
            errorMessage = error.message || errorMessage;
        }
        
        UI.showMessage(errorMessage, 'error');
    } finally {
        UI.setButtonLoading(submitButton, false);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    // Проверяем авторизацию
    checkAuth();
    
    // Привязываем обработчики форм
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Делаем функцию showTab глобальной
    window.showTab = showTab;
    
    // Проверяем "Запомнить меня"
    const rememberCheckbox = document.getElementById('remember');
    if (rememberCheckbox && Storage.getRememberMe()) {
        rememberCheckbox.checked = true;
    }
});