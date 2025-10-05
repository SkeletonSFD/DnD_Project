/**
 * Конфигурация приложения D&D
 */

const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:8000',
    ENDPOINTS: {
        REGISTER: '/api/users/register',
        LOGIN: '/api/users/login',
        ME: '/api/users/me',
        USERS: '/api/users/',
        HEALTH: '/health'
    },
    SOCKET_URL: 'http://127.0.0.1:8000'
};

// Ключи для localStorage
const STORAGE_KEYS = {
    TOKEN: 'dnd_auth_token',
    USER: 'dnd_user_data',
    REMEMBER: 'dnd_remember_me'
};

// Утилиты для работы с localStorage
const Storage = {
    setToken(token) {
        localStorage.setItem(STORAGE_KEYS.TOKEN, token);
    },
    
    getToken() {
        return localStorage.getItem(STORAGE_KEYS.TOKEN);
    },
    
    removeToken() {
        localStorage.removeItem(STORAGE_KEYS.TOKEN);
    },
    
    setUser(user) {
        localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    },
    
    getUser() {
        const user = localStorage.getItem(STORAGE_KEYS.USER);
        return user ? JSON.parse(user) : null;
    },
    
    removeUser() {
        localStorage.removeItem(STORAGE_KEYS.USER);
    },
    
    setRememberMe(value) {
        localStorage.setItem(STORAGE_KEYS.REMEMBER, value);
    },
    
    getRememberMe() {
        return localStorage.getItem(STORAGE_KEYS.REMEMBER) === 'true';
    },
    
    clearAll() {
        this.removeToken();
        this.removeUser();
        localStorage.removeItem(STORAGE_KEYS.REMEMBER);
    }
};

// Утилиты для работы с API
const API = {
    async request(endpoint, options = {}) {
        const url = `${API_CONFIG.BASE_URL}${endpoint}`;
        const token = Storage.getToken();
        
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        if (token && !options.skipAuth) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        try {
            const response = await fetch(url, {
                ...options,
                headers
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'Произошла ошибка');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    },
    
    async post(endpoint, data, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async put(endpoint, data, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    async delete(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'DELETE' });
    }
};

// Утилиты для отображения сообщений
const UI = {
    showMessage(message, type = 'info') {
        const container = document.getElementById('messageContainer');
        const box = document.getElementById('messageBox');
        
        if (!container || !box) return;
        
        // Удаляем предыдущие классы
        box.className = 'p-4 rounded border-2';
        
        // Добавляем новый класс в зависимости от типа
        box.classList.add(`message-${type}`);
        box.textContent = message;
        
        container.classList.remove('hidden');
        
        // Автоматически скрываем через 5 секунд
        setTimeout(() => {
            container.classList.add('hidden');
        }, 5000);
    },
    
    hideMessage() {
        const container = document.getElementById('messageContainer');
        if (container) {
            container.classList.add('hidden');
        }
    },
    
    setButtonLoading(button, loading = true) {
        if (loading) {
            button.disabled = true;
            button.dataset.originalText = button.textContent;
            button.innerHTML = '<span class="loading inline-block">⚔️</span> Загрузка...';
        } else {
            button.disabled = false;
            button.textContent = button.dataset.originalText || button.textContent;
        }
    }
};

// Проверка авторизации при загрузке страницы
function checkAuth() {
    const token = Storage.getToken();
    const currentPage = window.location.pathname;
    
    // Если есть токен и мы на странице входа - перенаправляем на выбор роли
    if (token && (currentPage.includes('index.html') || currentPage === '/')) {
        window.location.href = 'role-select.html';
    }
    
    // Если нет токена и мы в приложении или на выборе роли - перенаправляем на вход
    if (!token && (currentPage.includes('app.html') || currentPage.includes('role-select.html'))) {
        window.location.href = 'index.html';
    }
}

// Выход из системы
function logout() {
    Storage.clearAll();
    window.location.href = 'index.html';
}