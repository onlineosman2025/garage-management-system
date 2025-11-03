// Professional Dashboard with Real Data
class Dashboard {
    constructor() {
        this.api = window.api;
        this.charts = {};
        this.refreshInterval = null;
    }

    async init() {
        if (!this.api.isAuthenticated()) {
            window.location.href = '/index.html';
            return;
        }

        await this.loadDashboardData();
        this.setupEventListeners();
        this.startAutoRefresh();
    }

    async loadDashboardData() {
        try {
            this.showLoading(true);
            
            // Load dashboard stats
            const stats = await this.api.getDashboardStats();
            this.updateStatsCards(stats);

            // Load revenue chart
            const revenueData = await this.api.getRevenueChart();
            this.updateRevenueChart(revenueData);

            // Load recent activities
            await this.loadRecentActivities();

        } catch (error) {
            console.error('Dashboard loading error:', error);
            this.showError('Failed to load dashboard data');
        } finally {
            this.showLoading(false);
        }
    }

    updateStatsCards(stats) {
        // Update stat numbers with real data
        const statElements = {
            'totalCustomers': stats.total_customers || 0,
            'activeJobs': stats.total_jobs || 0,
            'monthlyRevenue': this.formatCurrency(stats.monthly_revenue || 0),
            'pendingInvoices': stats.pending_invoices || 0
        };

        Object.entries(statElements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                this.animateNumber(element, value);
            }
        });
    }

    updateRevenueChart(data) {
        const ctx = document.getElementById('revenueChart');
        if (!ctx) return;

        if (this.charts.revenue) {
            this.charts.revenue.destroy();
        }

        this.charts.revenue = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels || [],
                datasets: [{
                    label: 'Revenue',
                    data: data.values || [],
                    borderColor: '#FF6B35',
                    backgroundColor: 'rgba(255, 107, 53, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    async loadRecentActivities() {
        try {
            const activities = await this.api.makeRequest('/dashboard/activities?limit=10');
            this.updateActivitiesList(activities);
        } catch (error) {
            console.error('Activities loading error:', error);
        }
    }

    updateActivitiesList(activities) {
        const container = document.getElementById('recent-activities');
        if (!container) return;

        container.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-icon">${this.getActivityIcon(activity.type)}</div>
                <div class="activity-content">
                    <div class="activity-text">${activity.description}</div>
                    <div class="activity-time">${this.formatTime(activity.created_at)}</div>
                </div>
            </div>
        `).join('');
    }

    getActivityIcon(type) {
        const icons = {
            'job_created': '🔧',
            'invoice_paid': '💰',
            'customer_added': '👤',
            'service_completed': '✅',
            'payment_received': '💳'
        };
        return icons[type] || '📝';
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} minutes ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} hours ago`;
        return `${Math.floor(diff / 86400000)} days ago`;
    }

    formatCurrency(amount) {
        // Get currency from settings
        if (window.SettingsManager) {
            const currency = window.SettingsManager.getCurrency();
            const symbol = window.SettingsManager.getCurrencySymbol();
            const formatted = window.SettingsManager.formatCurrency(amount);
            console.log(`Dashboard formatCurrency: amount=${amount}, currency=${currency}, symbol=${symbol}, formatted=${formatted}`);
            return formatted;
        }
        
        // Fallback to AED if SettingsManager not available
        console.warn('SettingsManager not available, using AED fallback');
        const formatted = parseFloat(amount).toFixed(2);
        return `AED ${formatted}`;
    }

    animateNumber(element, targetValue) {
        const startValue = parseInt(element.textContent) || 0;
        const duration = 1000;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = Math.floor(startValue + (targetValue - startValue) * progress);
            element.textContent = typeof targetValue === 'string' ? targetValue : currentValue;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    setupEventListeners() {
        // Refresh button
        const refreshBtn = document.getElementById('refresh-dashboard');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadDashboardData());
        }

        // Quick action buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action]')) {
                const action = e.target.getAttribute('data-action');
                this.handleQuickAction(action);
            }
        });
    }

    async handleQuickAction(action) {
        switch (action) {
            case 'new-job':
                await this.openNewJobModal();
                break;
            case 'new-customer':
                await this.openNewCustomerModal();
                break;
            case 'view-reports':
                window.location.href = '/reports.html';
                break;
            default:
                console.log('Unknown action:', action);
        }
    }

    async openNewJobModal() {
        const modal = this.createModal('New Job', this.getNewJobForm());
        modal.show();
        
        // Wait for modal to be fully rendered, then load customers
        await this.initializeJobForm(modal);
    }
    
    async initializeJobForm(modal) {
        // Wait for DOM to be ready
        await new Promise(resolve => setTimeout(resolve, 150));
        
        // Load customers, vehicles, and services into dropdowns
        await Promise.all([
            this.loadCustomersForJob(),
            this.loadVehiclesForJob(),
            this.loadServicesForJob()
        ]);
        
        // Setup form submission handler
        this.setupJobFormSubmit(modal);
    }
    
    async loadCustomersForJob() {
        const customerSelect = document.getElementById('jobCustomerSelect');
        
        if (!customerSelect) {
            console.error('❌ Customer select element not found in job form');
            return;
        }
        
        try {
            customerSelect.innerHTML = '<option value="">Loading customers...</option>';
            customerSelect.disabled = true;
            
            console.log('🔄 Fetching customers for job...');
            
            const response = await this.api.getCustomers({ limit: 1000, _t: Date.now() });
            const customers = Array.isArray(response) ? response : (response.customers || []);
            
            console.log(`📊 Received ${customers.length} customers from API`);
            
            if (customers.length === 0) {
                customerSelect.innerHTML = '<option value="">No customers available</option>';
                console.warn('⚠️ No customers found');
                return;
            }
            
            const options = ['<option value="">Select Customer</option>'];
            customers.forEach(c => {
                options.push(`<option value="${c.id}">${c.name} - ${c.email || c.phone || ''}</option>`);
            });
            
            customerSelect.innerHTML = options.join('');
            customerSelect.disabled = false;
            
            console.log(`✅ Loaded ${customers.length} customers into job dropdown`);
            
        } catch (error) {
            console.error('❌ Failed to load customers:', error);
            customerSelect.innerHTML = '<option value="">Error loading customers</option>';
            customerSelect.disabled = false;
        }
    }
    
    async loadVehiclesForJob() {
        const vehicleInput = document.getElementById('jobVehicleInput');
        const vehicleList = document.getElementById('vehicleList');
        
        if (!vehicleInput || !vehicleList) {
            console.error('❌ Vehicle input/datalist element not found in job form');
            return;
        }
        
        try {
            console.log('🔄 Fetching vehicles for job...');
            
            const vehicles = await this.api.makeRequest('/vehicles?active_only=true');
            
            console.log(`📊 Received ${vehicles.length} vehicles from API`);
            
            if (vehicles.length === 0) {
                vehicleList.innerHTML = '';
                console.warn('⚠️ No vehicles found - user can type manually');
                return;
            }
            
            const options = [];
            vehicles.forEach(v => {
                const vehicleLabel = `${v.make} ${v.model} ${v.year || ''} - ${v.plate_number || ''}`.trim();
                options.push(`<option value="${vehicleLabel}">`);
            });
            
            vehicleList.innerHTML = options.join('');
            
            console.log(`✅ Loaded ${vehicles.length} vehicles into autocomplete (user can also type custom)`);
            
        } catch (error) {
            console.error('❌ Failed to load vehicles:', error);
            vehicleList.innerHTML = '';
        }
    }
    
    async loadServicesForJob() {
        const serviceSelect = document.getElementById('jobServiceSelect');
        
        if (!serviceSelect) {
            console.error('❌ Service select element not found in job form');
            return;
        }
        
        try {
            serviceSelect.innerHTML = '<option value="">Loading services...</option>';
            serviceSelect.disabled = true;
            
            console.log('🔄 Fetching services for job...');
            
            const services = await this.api.makeRequest('/services?active_only=true');
            
            console.log(`📊 Received ${services.length} active services from API`);
            console.log('📊 Services data:', services);
            
            if (services.length === 0) {
                serviceSelect.innerHTML = '<option value="">No services available - Add services in Settings</option>';
                console.warn('⚠️ No active services found');
                return;
            }
            
            const options = ['<option value="">Select Service</option>'];
            services.forEach(s => {
                console.log(`Adding service: ${s.name}, price: ${s.default_price}`);
                options.push(`<option value="${s.name}" data-price="${s.default_price}">${s.name}</option>`);
            });
            
            serviceSelect.innerHTML = options.join('');
            serviceSelect.disabled = false;
            
            // Add event listener using event delegation on the select element itself
            // Remove old listener if exists
            if (serviceSelect._priceChangeHandler) {
                serviceSelect.removeEventListener('change', serviceSelect._priceChangeHandler);
            }
            
            // Create and store the handler
            serviceSelect._priceChangeHandler = (e) => {
                const selectedOption = e.target.options[e.target.selectedIndex];
                const price = selectedOption.getAttribute('data-price');
                const costInput = document.querySelector('input[name="estimated_cost"]');
                
                console.log(`🔍 Service selected: ${e.target.value}`);
                console.log(`🔍 Price from data-price: ${price}`);
                console.log(`🔍 Cost input found: ${costInput ? 'Yes' : 'No'}`);
                
                if (price && costInput) {
                    costInput.value = parseFloat(price).toFixed(2);
                    console.log(`💰 Auto-filled price: ${price}`);
                } else {
                    console.warn(`⚠️ Could not auto-fill price. Price: ${price}, Input: ${costInput}`);
                }
            };
            
            serviceSelect.addEventListener('change', serviceSelect._priceChangeHandler);
            
            console.log(`✅ Loaded ${services.length} services into job dropdown with price auto-fill`);
            
        } catch (error) {
            console.error('❌ Failed to load services:', error);
            serviceSelect.innerHTML = '<option value="">Error loading services</option>';
            serviceSelect.disabled = false;
        }
    }
    
    setupJobFormSubmit(modal) {
        const form = document.getElementById('new-job-form');
        if (!form) {
            console.error('❌ Job form not found');
            return;
        }
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            try {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Creating Job...';
                
                const formData = new FormData(form);
                const jobData = Object.fromEntries(formData.entries());
                
                if (!jobData.customer_id) {
                    alert('Please select a customer');
                    return;
                }
                
                console.log('🔧 Creating job:', jobData);
                
                const newJob = await this.api.createJob(jobData);
                
                console.log('✅ Job created successfully:', newJob);
                alert('Job created successfully!');
                
                modal.hide();
                await this.loadDashboardData();
                
            } catch (error) {
                console.error('❌ Job creation failed:', error);
                alert('Error creating job: ' + error.message);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        });
    }

    async openNewCustomerModal() {
        const modal = this.createModal('New Customer', this.getNewCustomerForm());
        modal.show();
        
        // Add form submission handler
        setTimeout(() => {
            const form = document.getElementById('new-customer-form');
            if (form) {
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const formData = new FormData(form);
                    const customerData = Object.fromEntries(formData.entries());
                    
                    try {
                        const newCustomer = await this.api.createCustomer(customerData);
                        alert('Customer added successfully!');
                        modal.hide();
                        this.loadDashboardData(); // Refresh data
                    } catch (error) {
                        alert('Error adding customer: ' + error.message);
                    }
                });
            }
        }, 100);
    }


    createModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Close modal functionality
        modal.querySelector('.modal-close').addEventListener('click', () => {
            modal.remove();
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });

        return {
            show: () => modal.style.display = 'flex',
            hide: () => modal.remove()
        };
    }

    getNewJobForm() {
        // Get currency from settings
        const currencySymbol = window.SettingsManager ? window.SettingsManager.getCurrencySymbol() : 'AED';
        
        return `
            <form id="new-job-form">
                <div class="form-group">
                    <label data-translate="customer">Customer</label>
                    <select name="customer_id" required id="jobCustomerSelect">
                        <option value="" data-translate="loading_customers">Loading customers...</option>
                    </select>
                </div>
                <div class="form-group">
                    <label data-translate="vehicle">Vehicle</label>
                    <input type="text" name="vehicle" list="vehicleList" placeholder="Type or select vehicle (e.g., Toyota Camry 2020)" required id="jobVehicleInput">
                    <datalist id="vehicleList">
                        <option value="Loading vehicles..."></option>
                    </datalist>
                </div>
                <div class="form-group">
                    <label data-translate="service_type">Service Type</label>
                    <select name="service_type" required id="jobServiceSelect">
                        <option value="" data-translate="loading">Loading services...</option>
                    </select>
                </div>
                <div class="form-group">
                    <label data-translate="description">Description</label>
                    <textarea name="description" rows="3" placeholder="Job description..." required></textarea>
                </div>
                <div class="form-group">
                    <label data-translate="estimated_cost">Estimated Cost (${currencySymbol})</label>
                    <input type="number" name="estimated_cost" step="0.01" placeholder="0.00" required>
                </div>
                <div class="form-group">
                    <label data-translate="priority">Priority</label>
                    <select name="priority">
                        <option value="normal" data-translate="normal">Normal</option>
                        <option value="high" data-translate="high">High</option>
                        <option value="urgent" data-translate="urgent">Urgent</option>
                    </select>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary" data-translate="new_job">Create Job</button>
                    <button type="button" class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()" data-translate="cancel">Cancel</button>
                </div>
            </form>
        `;
    }

    getNewCustomerForm() {
        return `
            <form id="new-customer-form">
                <div class="form-group">
                    <label data-translate="full_name">Full Name</label>
                    <input type="text" name="name" placeholder="Enter customer full name" required>
                </div>
                <div class="form-group">
                    <label data-translate="email">Email</label>
                    <input type="email" name="email" placeholder="customer@email.com" required>
                </div>
                <div class="form-group">
                    <label data-translate="phone">Phone</label>
                    <input type="tel" name="phone" placeholder="+971 50 123 4567" required>
                </div>
                <div class="form-group">
                    <label data-translate="address">Address</label>
                    <textarea name="address" rows="2" placeholder="Customer address"></textarea>
                </div>
                <div class="form-group">
                    <label data-translate="vehicle_info">Vehicle Information</label>
                    <input type="text" name="vehicle" placeholder="e.g., Toyota Camry 2020, License: ABC-1234">
                </div>
                <div class="form-group">
                    <label data-translate="notes">Notes</label>
                    <textarea name="notes" rows="2" placeholder="Any special notes about this customer"></textarea>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn-primary" data-translate="add_customer">Add Customer</button>
                    <button type="button" class="btn-secondary" onclick="this.closest('.modal-overlay').remove()" data-translate="cancel">Cancel</button>
                </div>
            </form>
        `;
    }

    getNewInvoiceForm() {
        // Get tax rate from settings
        const taxRate = window.SettingsManager ? window.SettingsManager.getTaxRate() : 5;
        const currency = window.SettingsManager ? window.SettingsManager.getCurrency() : 'AED';
        const currencySymbol = window.SettingsManager ? window.SettingsManager.getCurrencySymbol() : 'AED';
        
        return `
            <form id="new-invoice-form">
                <div class="form-group">
                    <label data-translate="customer">Customer *</label>
                    <select name="customer_id" required id="invoiceCustomerSelect">
                        <option value="" data-translate="loading_customers">Loading customers...</option>
                    </select>
                </div>
                <div class="form-group">
                    <label data-translate="select_job">Related Job (Optional)</label>
                    <select name="job_id" id="invoiceJobSelect" disabled>
                        <option value="">Select customer first</option>
                    </select>
                </div>
                <div class="form-group">
                    <label data-translate="invoice_amount">Invoice Amount (${currencySymbol}) *</label>
                    <input type="number" name="amount" id="invoiceAmount" step="0.01" placeholder="0.00" required>
                </div>
                <div class="form-group">
                    <label data-translate="tax_rate">Tax Rate (%) *</label>
                    <input type="number" name="tax_rate" value="${taxRate}" step="0.01" placeholder="${taxRate}" required>
                    <small style="color: #666; font-size: 0.9em;">Default from settings: ${taxRate}%</small>
                </div>
                <div class="form-group">
                    <label data-translate="description">Description *</label>
                    <textarea name="description" rows="3" placeholder="Invoice description or services provided..." required></textarea>
                </div>
                <div class="form-group">
                    <label data-translate="due_date">Due Date *</label>
                    <input type="date" name="due_date" required>
                </div>
                <div class="form-group">
                    <label data-translate="payment_terms">Payment Terms</label>
                    <select name="payment_terms">
                        <option value="due_on_receipt" data-translate="due_on_receipt">Due on Receipt</option>
                        <option value="net_15" data-translate="net_15">Net 15 Days</option>
                        <option value="net_30" data-translate="net_30" selected>Net 30 Days</option>
                        <option value="net_60" data-translate="net_60">Net 60 Days</option>
                    </select>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn-primary" data-translate="create_invoice">Create Invoice</button>
                    <button type="button" class="btn-secondary" onclick="this.closest('.modal-overlay').remove()" data-translate="cancel">Cancel</button>
                </div>
            </form>
        `;
    }


    startAutoRefresh() {
        // Refresh dashboard every 5 minutes
        this.refreshInterval = setInterval(() => {
            this.loadDashboardData();
        }, 300000);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
    }

    showLoading(show) {
        const loader = document.getElementById('dashboard-loader');
        if (loader) {
            loader.style.display = show ? 'flex' : 'none';
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-toast';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);

        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
    window.dashboard.init();
});
