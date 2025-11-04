/**
 * Professional Admin Dashboard Functions
 * Complete Garage Management System
 */

const AdminAPI = {
    baseURL: 'https://garage-management-system-oa8e.onrender.com/api',
    
    getAuthToken() {
        return localStorage.getItem('auth_token');
    },

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.getAuthToken()}`,
            ...options.headers
        };

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || error.error || 'Request failed');
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    },

    // User Management
    async getUsers(filters = {}) {
        const params = new URLSearchParams(filters);
        return await this.request(`/admin/users?${params}`);
    },

    async createUser(userData) {
        return await this.request('/admin/users', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },

    async updateUser(userId, userData) {
        return await this.request(`/admin/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    },

    async deleteUser(userId) {
        return await this.request(`/admin/users/${userId}`, {
            method: 'DELETE'
        });
    },

    async resetUserPassword(userId, newPassword) {
        return await this.request(`/admin/users/${userId}/reset-password`, {
            method: 'POST',
            body: JSON.stringify({ password: newPassword })
        });
    },

    // Garage Management
    async getGarages(filters = {}) {
        const params = new URLSearchParams(filters);
        return await this.request(`/admin/garages?${params}`);
    },

    async getGarageDetails(garageId) {
        return await this.request(`/admin/garages/${garageId}`);
    },

    async updateGarage(garageId, garageData) {
        return await this.request(`/admin/garages/${garageId}`, {
            method: 'PUT',
            body: JSON.stringify(garageData)
        });
    },

    async suspendGarage(garageId, reason) {
        return await this.request(`/admin/garages/${garageId}/suspend`, {
            method: 'POST',
            body: JSON.stringify({ reason })
        });
    },

    async activateGarage(garageId) {
        return await this.request(`/admin/garages/${garageId}/activate`, {
            method: 'POST'
        });
    },

    async extendTrial(garageId, days) {
        return await this.request(`/admin/garages/${garageId}/extend-trial`, {
            method: 'POST',
            body: JSON.stringify({ days })
        });
    },

    async deleteGarage(garageId) {
        return await this.request(`/admin/garages/${garageId}`, {
            method: 'DELETE'
        });
    },

    // Subscription Management
    async upgradeSubscription(garageId, plan) {
        return await this.request(`/admin/subscriptions/${garageId}/upgrade`, {
            method: 'POST',
            body: JSON.stringify({ plan })
        });
    },

    async cancelSubscription(garageId) {
        return await this.request(`/admin/subscriptions/${garageId}/cancel`, {
            method: 'POST'
        });
    },

    // Analytics
    async getAnalytics(dateRange = {}) {
        const params = new URLSearchParams(dateRange);
        return await this.request(`/admin/analytics?${params}`);
    },

    async getRevenue(period = 'month') {
        return await this.request(`/admin/analytics/revenue?period=${period}`);
    },

    // System Settings
    async getSettings() {
        return await this.request('/admin/settings');
    },

    async updateSettings(settings) {
        return await this.request('/admin/settings', {
            method: 'PUT',
            body: JSON.stringify(settings)
        });
    }
};

// UI Helper Functions
const UI = {
    showModal(modalId) {
        document.getElementById(modalId).style.display = 'flex';
    },

    hideModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    },

    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },

    showLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '<div class="loading-spinner"></div>';
        }
    },

    hideLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '';
        }
    },

    confirm(message) {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'confirm-modal';
            modal.innerHTML = `
                <div class="confirm-content">
                    <h3>Confirm Action</h3>
                    <p>${message}</p>
                    <div class="confirm-buttons">
                        <button class="btn-cancel" onclick="this.closest('.confirm-modal').remove(); window.confirmResolve(false);">Cancel</button>
                        <button class="btn-confirm" onclick="this.closest('.confirm-modal').remove(); window.confirmResolve(true);">Confirm</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            window.confirmResolve = resolve;
        });
    }
};

// Form Validation
const Validator = {
    email(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    password(password) {
        return password.length >= 8;
    },

    phone(phone) {
        const re = /^\+?[\d\s-()]+$/;
        return re.test(phone);
    },

    required(value) {
        return value && value.trim().length > 0;
    }
};

// Data Formatting
const Format = {
    date(dateString) {
        return new Date(dateString).toLocaleDateString();
    },

    datetime(dateString) {
        return new Date(dateString).toLocaleString();
    },

    currency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },

    number(num) {
        return new Intl.NumberFormat().format(num);
    }
};
