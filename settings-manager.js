/**
 * Centralized Settings Manager for Garage Management System
 * Provides consistent access to garage settings across all pages
 */

const SettingsManager = {
    // Default settings (fallback only)
    defaults: {
        garage: {
            name: 'My Garage',
            email: 'info@garage.com',
            phone: '+971 4 123 4567',
            website: '',
            address: '',
            description: ''
        },
        business: {
            currency: 'AED',
            currencySymbol: 'AED',
            timezone: 'Asia/Dubai',
            language: 'en',
            dateFormat: 'DD/MM/YYYY',
            workingHours: 'Sunday - Thursday: 8:00 AM - 6:00 PM',
            taxRate: 5.0
        },
        notifications: {
            emailNotifications: true,
            smsNotifications: false,
            jobAlerts: true,
            paymentReminders: true,
            stockAlerts: true,
            dailyReports: false
        },
        security: {
            twoFactorAuth: false,
            loginAlerts: true
        }
    },

    // Cache for database settings
    _dbSettingsCache: null,
    _dbSettingsLoaded: false,

    /**
     * Load settings from database API
     */
    async loadFromDatabase() {
        try {
            const response = await fetch('/api/settings');
            if (response.ok) {
                const dbSettings = await response.json();
                this._dbSettingsCache = this.convertDbToSettings(dbSettings);
                this._dbSettingsLoaded = true;
                // Save to localStorage for offline access
                this.saveAll(this._dbSettingsCache);
                return this._dbSettingsCache;
            }
        } catch (error) {
            console.error('Error loading settings from database:', error);
        }
        return null;
    },

    /**
     * Convert database settings format to SettingsManager format
     */
    convertDbToSettings(dbSettings) {
        return {
            garage: {
                name: dbSettings.garage_name || this.defaults.garage.name,
                email: dbSettings.garage_email || this.defaults.garage.email,
                phone: dbSettings.garage_phone || this.defaults.garage.phone,
                website: dbSettings.garage_website || this.defaults.garage.website,
                address: dbSettings.garage_address || this.defaults.garage.address,
                description: dbSettings.garage_description || this.defaults.garage.description
            },
            business: {
                currency: dbSettings.currency || this.defaults.business.currency,
                currencySymbol: dbSettings.currency || this.defaults.business.currencySymbol,
                timezone: dbSettings.timezone || this.defaults.business.timezone,
                language: dbSettings.language || this.defaults.business.language,
                dateFormat: dbSettings.date_format || this.defaults.business.dateFormat,
                workingHours: dbSettings.working_hours || this.defaults.business.workingHours,
                taxRate: parseFloat(dbSettings.tax_rate) || this.defaults.business.taxRate
            },
            notifications: this.defaults.notifications,
            security: this.defaults.security
        };
    },

    /**
     * Get all settings (prioritize database, fallback to localStorage, then defaults)
     */
    getAll() {
        // If database settings are loaded, use them
        if (this._dbSettingsLoaded && this._dbSettingsCache) {
            return this._dbSettingsCache;
        }
        
        // Otherwise try localStorage
        try {
            const saved = localStorage.getItem('garage_settings');
            if (saved) {
                const settings = JSON.parse(saved);
                // Merge with defaults to ensure all fields exist
                return this.mergeWithDefaults(settings);
            }
        } catch (error) {
            console.error('Error loading settings:', error);
        }
        return this.defaults;
    },

    /**
     * Merge saved settings with defaults
     */
    mergeWithDefaults(saved) {
        return {
            garage: { ...this.defaults.garage, ...saved.garage },
            business: { ...this.defaults.business, ...saved.business },
            notifications: { ...this.defaults.notifications, ...saved.notifications },
            security: { ...this.defaults.security, ...saved.security }
        };
    },

    /**
     * Get a specific setting value
     * @param {string} path - Dot notation path (e.g., 'business.currency')
     */
    get(path) {
        const settings = this.getAll();
        const keys = path.split('.');
        let value = settings;
        
        for (const key of keys) {
            if (value && typeof value === 'object' && key in value) {
                value = value[key];
            } else {
                return undefined;
            }
        }
        
        return value;
    },

    /**
     * Save all settings to localStorage
     */
    saveAll(settings) {
        try {
            localStorage.setItem('garage_settings', JSON.stringify(settings));
            return true;
        } catch (error) {
            console.error('Error saving settings:', error);
            return false;
        }
    },

    /**
     * Update a specific setting
     * @param {string} path - Dot notation path (e.g., 'business.currency')
     * @param {any} value - New value
     */
    set(path, value) {
        const settings = this.getAll();
        const keys = path.split('.');
        let current = settings;
        
        for (let i = 0; i < keys.length - 1; i++) {
            const key = keys[i];
            if (!(key in current)) {
                current[key] = {};
            }
            current = current[key];
        }
        
        current[keys[keys.length - 1]] = value;
        return this.saveAll(settings);
    },

    // Convenience getters for commonly used settings
    getGarageName() {
        return this.get('garage.name') || this.defaults.garage.name;
    },

    getGarageEmail() {
        return this.get('garage.email') || this.defaults.garage.email;
    },

    getGaragePhone() {
        return this.get('garage.phone') || this.defaults.garage.phone;
    },

    getGarageAddress() {
        return this.get('garage.address') || this.defaults.garage.address;
    },

    getCurrency() {
        return this.get('business.currency') || this.defaults.business.currency;
    },

    getCurrencySymbol() {
        const currency = this.getCurrency();
        const symbols = {
            'AED': 'AED',
            'USD': '$',
            'EUR': '€',
            'SAR': 'SAR',
            'GBP': '£'
        };
        return symbols[currency] || currency;
    },

    getTaxRate() {
        return parseFloat(this.get('business.taxRate')) || this.defaults.business.taxRate;
    },

    getTimezone() {
        return this.get('business.timezone') || this.defaults.business.timezone;
    },

    getLanguage() {
        return this.get('business.language') || this.defaults.business.language;
    },

    getDateFormat() {
        return this.get('business.dateFormat') || this.defaults.business.dateFormat;
    },

    getWorkingHours() {
        return this.get('business.workingHours') || this.defaults.business.workingHours;
    },

    /**
     * Format currency amount
     * @param {number} amount - Amount to format
     * @param {boolean} includeSymbol - Whether to include currency symbol
     */
    formatCurrency(amount, includeSymbol = true) {
        const currency = this.getCurrency();
        const symbol = this.getCurrencySymbol();
        const formatted = parseFloat(amount).toFixed(2);
        
        if (includeSymbol) {
            // For symbols that go before the amount (like $)
            if (currency === 'USD' || currency === 'GBP' || currency === 'EUR') {
                return `${symbol}${formatted}`;
            }
            // For symbols that go after (like AED, SAR)
            return `${symbol} ${formatted}`;
        }
        
        return formatted;
    },

    /**
     * Calculate tax amount
     * @param {number} amount - Base amount
     */
    calculateTax(amount) {
        const taxRate = this.getTaxRate();
        return parseFloat((amount * (taxRate / 100)).toFixed(2));
    },

    /**
     * Calculate total with tax
     * @param {number} amount - Base amount
     */
    calculateTotal(amount) {
        const tax = this.calculateTax(amount);
        return parseFloat((amount + tax).toFixed(2));
    },

    /**
     * Format date according to settings
     * @param {Date|string} date - Date to format
     */
    formatDate(date) {
        const dateObj = typeof date === 'string' ? new Date(date) : date;
        const format = this.getDateFormat();
        
        const day = String(dateObj.getDate()).padStart(2, '0');
        const month = String(dateObj.getMonth() + 1).padStart(2, '0');
        const year = dateObj.getFullYear();
        
        switch (format) {
            case 'DD/MM/YYYY':
                return `${day}/${month}/${year}`;
            case 'MM/DD/YYYY':
                return `${month}/${day}/${year}`;
            case 'YYYY-MM-DD':
                return `${year}-${month}-${day}`;
            default:
                return `${day}/${month}/${year}`;
        }
    },

    /**
     * Update UI elements with garage info
     * Call this on page load to update common elements
     */
    updateUIElements() {
        // Update garage name in logo/header
        const logoElements = document.querySelectorAll('#garageLogo, .garage-name, [data-garage-name]');
        logoElements.forEach(el => {
            const currentText = el.textContent;
            const emoji = currentText.match(/^[\u{1F300}-\u{1F9FF}]/u);
            const garageName = this.getGarageName();
            el.textContent = emoji ? `${emoji[0]} ${garageName}` : garageName;
        });

        // Update currency symbols
        const currencyElements = document.querySelectorAll('[data-currency]');
        currencyElements.forEach(el => {
            el.textContent = this.getCurrencySymbol();
        });

        // Update tax rate displays
        const taxElements = document.querySelectorAll('[data-tax-rate]');
        taxElements.forEach(el => {
            el.textContent = `${this.getTaxRate()}%`;
        });
    },

    /**
     * Listen for settings changes from other tabs
     */
    watchForChanges(callback) {
        window.addEventListener('storage', (e) => {
            if (e.key === 'garage_settings') {
                callback(this.getAll());
            }
        });
    },

    /**
     * Initialize settings by loading from database
     */
    async init() {
        await this.loadFromDatabase();
        this.updateUIElements();
    }
};

// Make it globally available
window.SettingsManager = SettingsManager;

// Auto-load settings from database and update UI on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', async () => {
        await SettingsManager.init();
    });
} else {
    // If DOM already loaded, init immediately
    SettingsManager.init();
}
