/**
 * Mobile Navigation Handler
 * Handles hamburger menu, overlay, and navigation
 */

class MobileNav {
    constructor() {
        this.isOpen = false;
        this.init();
    }

    init() {
        // Create mobile navigation structure
        this.createMobileNav();
        
        // Add event listeners
        this.addEventListeners();
        
        // Handle resize events
        window.addEventListener('resize', () => this.handleResize());
    }

    createMobileNav() {
        // Check if already exists
        if (document.querySelector('.mobile-nav-menu')) return;

        // Create hamburger toggle button
        const header = document.querySelector('.header');
        if (!header) return;

        const headerActions = header.querySelector('.header-actions');
        if (!headerActions) return;

        // Add hamburger button
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'mobile-nav-toggle';
        toggleBtn.innerHTML = '☰';
        toggleBtn.setAttribute('aria-label', 'Toggle mobile menu');
        headerActions.appendChild(toggleBtn);

        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'mobile-menu-overlay';
        document.body.appendChild(overlay);

        // Create mobile menu
        const mobileMenu = document.createElement('div');
        mobileMenu.className = 'mobile-nav-menu';
        mobileMenu.innerHTML = this.getMenuHTML();
        document.body.appendChild(mobileMenu);
    }

    getMenuHTML() {
        const userRole = this.getUserRole();
        const userName = this.getUserName();

        return `
            <div class="mobile-nav-header">
                <span>🚗 GMS Menu</span>
                <button class="mobile-nav-close" aria-label="Close menu">×</button>
            </div>
            <ul class="mobile-nav-items">
                <li>
                    <a href="/garage-dashboard.html">
                        <span class="icon">🏠</span> Dashboard
                    </a>
                </li>
                <li>
                    <a href="/invoices.html">
                        <span class="icon">💰</span> Invoices
                    </a>
                </li>
                <li>
                    <a href="/customers.html">
                        <span class="icon">👥</span> Customers
                    </a>
                </li>
                <li>
                    <a href="/reports.html">
                        <span class="icon">📊</span> Reports
                    </a>
                </li>
                <li>
                    <a href="/vat-reports.html">
                        <span class="icon">🇦🇪</span> UAE VAT
                    </a>
                </li>
                <li>
                    <a href="/inventory.html">
                        <span class="icon">📦</span> Inventory
                    </a>
                </li>
                <li>
                    <a href="/users.html">
                        <span class="icon">👤</span> Users
                    </a>
                </li>
                <li>
                    <a href="/settings.html">
                        <span class="icon">⚙️</span> Settings
                    </a>
                </li>
                <li style="margin-top: 20px; border-top: 2px solid #f0f0f0; padding-top: 10px;">
                    <button onclick="logout()" style="color: #ef4444;">
                        <span class="icon">🚪</span> Logout
                    </button>
                </li>
            </ul>
            ${userName ? `
                <div style="padding: 20px; background: #f9f9f9; margin-top: auto;">
                    <div style="font-size: 0.85em; color: #666;">Logged in as</div>
                    <div style="font-weight: 600; color: #333;">${userName}</div>
                    <div style="font-size: 0.8em; color: #999;">${userRole}</div>
                </div>
            ` : ''}
        `;
    }

    getUserRole() {
        try {
            const user = JSON.parse(localStorage.getItem('user') || '{}');
            return user.role || 'User';
        } catch {
            return 'User';
        }
    }

    getUserName() {
        try {
            const user = JSON.parse(localStorage.getItem('user') || '{}');
            return user.name || user.email || '';
        } catch {
            return '';
        }
    }

    addEventListeners() {
        // Toggle button
        document.addEventListener('click', (e) => {
            if (e.target.closest('.mobile-nav-toggle')) {
                this.toggle();
            }
        });

        // Close button
        document.addEventListener('click', (e) => {
            if (e.target.closest('.mobile-nav-close')) {
                this.close();
            }
        });

        // Overlay click
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('mobile-menu-overlay')) {
                this.close();
            }
        });

        // Menu item clicks
        document.addEventListener('click', (e) => {
            if (e.target.closest('.mobile-nav-items a')) {
                this.close();
            }
        });

        // Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        const menu = document.querySelector('.mobile-nav-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');
        
        if (menu) menu.classList.add('active');
        if (overlay) overlay.classList.add('active');
        
        document.body.style.overflow = 'hidden';
        this.isOpen = true;
    }

    close() {
        const menu = document.querySelector('.mobile-nav-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');
        
        if (menu) menu.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
        
        document.body.style.overflow = '';
        this.isOpen = false;
    }

    handleResize() {
        // Close menu on resize to desktop
        if (window.innerWidth > 768 && this.isOpen) {
            this.close();
        }
    }
}

// Initialize mobile nav when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new MobileNav();
    });
} else {
    new MobileNav();
}

// Logout function (if not already defined)
if (typeof logout === 'undefined') {
    function logout() {
        localStorage.clear();
        sessionStorage.clear();
        window.location.href = '/index.html';
    }
}
