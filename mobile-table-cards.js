/**
 * Mobile Table Cards Converter
 * Converts data tables to mobile-friendly card views
 */

class MobileTableCards {
    constructor() {
        this.init();
        window.addEventListener('resize', () => this.handleResize());
    }

    init() {
        this.convertTables();
    }

    handleResize() {
        this.convertTables();
    }

    convertTables() {
        // Only convert on mobile
        if (window.innerWidth > 768) return;

        const tables = document.querySelectorAll('.data-table, .invoice-table, .customer-table');
        tables.forEach(table => {
            if (!table.classList.contains('card-mobile')) return;
            
            const cardView = this.createCardView(table);
            if (cardView) {
                // Insert card view after table
                if (!table.nextElementSibling || !table.nextElementSibling.classList.contains('mobile-card-view')) {
                    table.parentNode.insertBefore(cardView, table.nextSibling);
                }
            }
        });
    }

    createCardView(table) {
        const tbody = table.querySelector('tbody');
        if (!tbody) return null;

        const headers = Array.from(table.querySelectorAll('thead th')).map(th => ({
            text: th.textContent.trim(),
            key: th.dataset.key || th.textContent.trim().toLowerCase().replace(/\s+/g, '_')
        }));

        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        const container = document.createElement('div');
        container.className = 'mobile-card-view';

        rows.forEach((row, index) => {
            const cells = Array.from(row.querySelectorAll('td'));
            const card = this.createCard(headers, cells, index);
            container.appendChild(card);
        });

        return container;
    }

    createCard(headers, cells, index) {
        const card = document.createElement('div');
        card.className = 'mobile-card';

        // Extract data
        const data = {};
        headers.forEach((header, i) => {
            data[header.key] = cells[i] ? cells[i].innerHTML : '';
        });

        // Build card HTML
        card.innerHTML = this.getCardHTML(data, headers);

        return card;
    }

    getCardHTML(data, headers) {
        // Default card template
        let html = '<div class="mobile-card-body">';
        
        headers.forEach(header => {
            const value = data[header.key] || '';
            if (value && !value.includes('<button')) {
                html += `
                    <div class="mobile-card-row">
                        <span class="mobile-card-label">${header.text}:</span>
                        <span class="mobile-card-value">${value}</span>
                    </div>
                `;
            }
        });

        html += '</div>';

        // Add actions if present
        const actionsKey = headers.find(h => h.text.toLowerCase().includes('action'));
        if (actionsKey && data[actionsKey.key]) {
            html += `<div class="mobile-card-actions">${data[actionsKey.key]}</div>`;
        }

        return html;
    }
}

// Helper function to create invoice card
function createInvoiceCard(invoice) {
    return `
        <div class="mobile-card">
            <div class="mobile-card-header">
                <span class="mobile-card-title">#${invoice.id}</span>
                <span class="mobile-card-badge ${invoice.status === 'paid' ? 'badge-success' : 'badge-warning'}">
                    ${invoice.status}
                </span>
            </div>
            <div class="mobile-card-body">
                <div class="mobile-card-row">
                    <span class="mobile-card-label">Customer:</span>
                    <span class="mobile-card-value">${invoice.customer_name || 'Unknown'}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label">Date:</span>
                    <span class="mobile-card-value">${invoice.created_at || ''}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label">Amount:</span>
                    <span class="mobile-card-value">AED ${parseFloat(invoice.amount || 0).toFixed(2)}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label">Total:</span>
                    <span class="mobile-card-value" style="font-size: 1.1em; color: #FF6600;">
                        AED ${parseFloat(invoice.total_amount || 0).toFixed(2)}
                    </span>
                </div>
            </div>
            <div class="mobile-card-actions">
                <button onclick="viewInvoice(${invoice.id})" style="background: #4CAF50; color: white;">
                    👁️ View
                </button>
                <button onclick="emailInvoice(${invoice.id})" style="background: #2196F3; color: white;">
                    📧 Email
                </button>
                <button onclick="editInvoice(${invoice.id})" style="background: #FF9800; color: white;">
                    ✏️ Edit
                </button>
            </div>
        </div>
    `;
}

// Helper function to create customer card
function createCustomerCard(customer) {
    return `
        <div class="mobile-card">
            <div class="mobile-card-header">
                <span class="mobile-card-title">${customer.name}</span>
            </div>
            <div class="mobile-card-body">
                <div class="mobile-card-row">
                    <span class="mobile-card-label">Email:</span>
                    <span class="mobile-card-value">${customer.email || 'N/A'}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label">Phone:</span>
                    <span class="mobile-card-value">${customer.phone || 'N/A'}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label">Vehicle:</span>
                    <span class="mobile-card-value">${customer.vehicle || 'N/A'}</span>
                </div>
            </div>
            <div class="mobile-card-actions">
                <button onclick="viewCustomer(${customer.id})" style="background: #4CAF50; color: white;">
                    👁️ View
                </button>
                <button onclick="editCustomer(${customer.id})" style="background: #FF9800; color: white;">
                    ✏️ Edit
                </button>
            </div>
        </div>
    `;
}

// Helper function to render mobile cards for invoices
function renderMobileInvoiceCards(invoices) {
    const container = document.getElementById('mobile-invoice-cards');
    if (!container) return;

    container.innerHTML = invoices.map(invoice => createInvoiceCard(invoice)).join('');
}

// Helper function to render mobile cards for customers
function renderMobileCustomerCards(customers) {
    const container = document.getElementById('mobile-customer-cards');
    if (!container) return;

    container.innerHTML = customers.map(customer => createCustomerCard(customer)).join('');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new MobileTableCards();
    });
} else {
    new MobileTableCards();
}
