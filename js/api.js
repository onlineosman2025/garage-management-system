// Professional API Integration for Unified GMS - FINAL UPDATE 2025-11-03-13-30-RENDER-BACKEND
class GarageAPI {
    constructor() {
        // Render backend URL - FINAL VERSION
        this.baseURL = 'https://garage-management-system-oa8e.onrender.com/api';
        this.token = localStorage.getItem('auth_token');
        console.log('🚀 API INITIALIZED - RENDER BACKEND:', this.baseURL);
        console.log('📅 Updated: 2025-11-03-13-30-FINAL');
    }

    // Authentication
    async login(email, password) {
        try {
            console.log('[API DEBUG] Login called with:', { email, password });
            console.log('[API DEBUG] Base URL:', this.baseURL);
            
            const response = await fetch(`${this.baseURL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            console.log('[API DEBUG] Response status:', response.status);
            console.log('[API DEBUG] Response ok:', response.ok);

            if (!response.ok) {
                const errorText = await response.text();
                console.log('[API DEBUG] Error response:', errorText);
                throw new Error('Invalid credentials');
            }

            const data = await response.json();
            this.token = data.access_token;
            localStorage.setItem('auth_token', this.token);
            localStorage.setItem('user_data', JSON.stringify(data.user));
            localStorage.setItem('garage_data', JSON.stringify(data.garage));
            
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    async register(userData) {
        try {
            const response = await fetch(`${this.baseURL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                throw new Error('Registration failed');
            }

            return await response.json();
        } catch (error) {
            console.error('Registration error:', error);
            throw error;
        }
    }

    // Dashboard APIs
    async getDashboardStats() {
        return this.makeRequest('/dashboard/stats');
    }

    async getRevenueChart(period = '12months') {
        return this.makeRequest(`/dashboard/revenue?period=${period}`);
    }

    // Customer Management
    async getCustomers(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.makeRequest(`/customers?${queryString}`);
    }

    async createCustomer(customerData) {
        return this.makeRequest('/customers', 'POST', customerData);
    }

    async updateCustomer(id, customerData) {
        return this.makeRequest(`/customers/${id}`, 'PUT', customerData);
    }

    async deleteCustomer(id) {
        return this.makeRequest(`/customers/${id}`, 'DELETE');
    }


    // Garage Management
    async getGarageProfile() {
        return this.makeRequest('/garage/profile');
    }

    async updateGarageProfile(garageData) {
        return this.makeRequest('/garage/profile', 'PUT', garageData);
    }

    async getGarageServices() {
        return this.makeRequest('/garage/services');
    }

    async createService(serviceData) {
        return this.makeRequest('/garage/services', 'POST', serviceData);
    }

    // Job Management
    async getJobs(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.makeRequest(`/jobs?${queryString}`);
    }

    async createJob(jobData) {
        return this.makeRequest('/jobs', 'POST', jobData);
    }

    async updateJobStatus(id, status) {
        return this.makeRequest(`/jobs/${id}/status`, 'PUT', { status });
    }

    // Invoice Management
    async getInvoices(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.makeRequest(`/invoices?${queryString}`);
    }

    async createInvoice(invoiceData) {
        return this.makeRequest('/invoices', 'POST', invoiceData);
    }

    async updateInvoice(id, invoiceData) {
        return this.makeRequest(`/invoices/${id}`, 'PUT', invoiceData);
    }

    async deleteInvoice(id) {
        return this.makeRequest(`/invoices/${id}`, 'DELETE');
    }

    async markInvoicePaid(id, paymentData) {
        return this.makeRequest(`/invoices/${id}/pay`, 'POST', paymentData);
    }

    // Reports
    async getRevenueReport(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.makeRequest(`/reports/revenue?${queryString}`);
    }

    async getCustomerReport(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.makeRequest(`/reports/customers?${queryString}`);
    }

    // Subscription Management
    async getSubscriptionStatus() {
        return this.makeRequest('/subscription/status');
    }

    async upgradeSubscription(planId) {
        return this.makeRequest('/subscription/upgrade', 'POST', { plan_id: planId });
    }

    // Utility Methods
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        return headers;
    }

    async makeRequest(endpoint, method = 'GET', data = null) {
        try {
            const config = {
                method,
                headers: this.getHeaders(),
            };

            if (data && (method === 'POST' || method === 'PUT')) {
                config.body = JSON.stringify(data);
            }

            const response = await fetch(`${this.baseURL}${endpoint}`, config);

            if (response.status === 401) {
                // Token expired, redirect to login
                localStorage.removeItem('auth_token');
                localStorage.removeItem('user_data');
                localStorage.removeItem('garage_data');
                window.location.href = '/index.html';
                return;
            }

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }

    // Logout
    logout() {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data');
        localStorage.removeItem('garage_data');
        window.location.href = '/index.html';
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.token;
    }

    // Get current user data
    getCurrentUser() {
        const userData = localStorage.getItem('user_data');
        return userData ? JSON.parse(userData) : null;
    }

    // Get current garage data
    getCurrentGarage() {
        const garageData = localStorage.getItem('garage_data');
        return garageData ? JSON.parse(garageData) : null;
    }
}

// Global API instance
window.api = new GarageAPI();
