/**
 * Hamburger Menu Component
 * Adds consistent navigation menu to all pages
 */

class HamburgerMenu {
    constructor() {
        this.init();
    }

    init() {
        this.injectMenuHTML();
        this.injectMenuStyles();
        this.attachEventListeners();
        this.setActivePage();
    }

    injectMenuHTML() {
        // Check if menu already exists
        if (document.querySelector('.hamburger-side-menu')) return;

        const menuHTML = `
            <!-- Hamburger Menu Overlay -->
            <div class="hamburger-menu-overlay" onclick="window.hamburgerMenu.toggle()"></div>
            
            <!-- Hamburger Side Menu -->
            <div class="hamburger-side-menu" id="hamburgerSideMenu">
                <div class="hamburger-menu-header">
                    <h3>🚗 GMS Menu</h3>
                    <button class="hamburger-close" onclick="window.hamburgerMenu.toggle()">&times;</button>
                </div>
                <nav class="hamburger-menu-nav">
                    <a href="/garage-dashboard.html" class="hamburger-menu-item" data-page="dashboard">
                        <span class="hamburger-menu-icon">🏠</span>
                        <span>Dashboard</span>
                    </a>
                    <a href="/invoices.html" class="hamburger-menu-item" data-page="invoices">
                        <span class="hamburger-menu-icon">💰</span>
                        <span>Invoices</span>
                    </a>
                    <a href="/customers.html" class="hamburger-menu-item" data-page="customers">
                        <span class="hamburger-menu-icon">👥</span>
                        <span>Customers</span>
                    </a>
                    <a href="/reports.html" class="hamburger-menu-item" data-page="reports">
                        <span class="hamburger-menu-icon">📊</span>
                        <span>Reports</span>
                    </a>
                    <a href="/vat-reports.html" class="hamburger-menu-item" data-page="vat">
                        <span class="hamburger-menu-icon">🇦🇪</span>
                        <span>UAE VAT</span>
                    </a>
                    <a href="/inventory.html" class="hamburger-menu-item" data-page="inventory">
                        <span class="hamburger-menu-icon">📦</span>
                        <span>Inventory</span>
                    </a>
                    <a href="/users.html" class="hamburger-menu-item" data-page="users">
                        <span class="hamburger-menu-icon">👤</span>
                        <span>Users</span>
                    </a>
                    <a href="/settings.html" class="hamburger-menu-item" data-page="settings">
                        <span class="hamburger-menu-icon">⚙️</span>
                        <span>Settings</span>
                    </a>
                </nav>
            </div>
        `;

        document.body.insertAdjacentHTML('afterbegin', menuHTML);

        // Add hamburger button to header if not exists
        this.addHamburgerButton();
    }

    addHamburgerButton() {
        const header = document.querySelector('.header');
        if (!header) return;

        // Check if hamburger already exists anywhere
        if (document.querySelector('.hamburger-menu-btn')) return;

        // Find or create header-left
        let headerLeft = header.querySelector('.header-left');
        if (!headerLeft) {
            headerLeft = document.createElement('div');
            headerLeft.className = 'header-left';
            
            // Find the logo or h1
            const logo = header.querySelector('.logo') || header.querySelector('h1');
            if (logo) {
                // If it's an h1, wrap it in a div with logo class
                if (logo.tagName === 'H1') {
                    const logoDiv = document.createElement('div');
                    logoDiv.className = 'logo';
                    logoDiv.textContent = logo.textContent;
                    logo.replaceWith(logoDiv);
                    headerLeft.appendChild(logoDiv);
                } else {
                    headerLeft.appendChild(logo);
                }
                header.insertBefore(headerLeft, header.firstChild);
            } else {
                // No logo found, just add header-left at the beginning
                header.insertBefore(headerLeft, header.firstChild);
            }
        }

        // Add hamburger button
        const hamburgerBtn = document.createElement('button');
        hamburgerBtn.className = 'hamburger-menu-btn';
        hamburgerBtn.setAttribute('onclick', 'window.hamburgerMenu.toggle()');
        hamburgerBtn.setAttribute('aria-label', 'Menu');
        hamburgerBtn.innerHTML = '<span></span><span></span><span></span>';
        
        headerLeft.insertBefore(hamburgerBtn, headerLeft.firstChild);
    }

    injectMenuStyles() {
        // Check if styles already injected
        if (document.getElementById('hamburger-menu-styles')) return;

        const style = document.createElement('style');
        style.id = 'hamburger-menu-styles';
        style.textContent = `
            /* Header Left Container */
            .header-left {
                display: flex;
                align-items: center;
                gap: 15px;
            }

            /* Hamburger Button */
            .hamburger-menu-btn {
                background: none;
                border: none;
                cursor: pointer;
                padding: 8px;
                display: flex;
                flex-direction: column;
                gap: 5px;
                width: 40px;
                height: 40px;
                justify-content: center;
                align-items: center;
                border-radius: 8px;
                transition: all 0.3s;
                z-index: 101;
            }

            .hamburger-menu-btn:hover {
                background: rgba(255, 255, 255, 0.15);
            }

            .hamburger-menu-btn span {
                display: block;
                width: 24px;
                height: 3px;
                background: white;
                border-radius: 2px;
                transition: all 0.3s;
            }

            /* Menu Overlay */
            .hamburger-menu-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 998;
                display: none;
                opacity: 0;
                transition: opacity 0.3s;
            }

            .hamburger-menu-overlay.active {
                display: block;
                opacity: 1;
            }

            /* Side Menu */
            .hamburger-side-menu {
                position: fixed;
                top: 0;
                left: -280px;
                width: 280px;
                height: 100%;
                background: white;
                box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
                z-index: 999;
                transition: left 0.3s ease;
                overflow-y: auto;
            }

            .hamburger-side-menu.active {
                left: 0;
            }

            /* Menu Header */
            .hamburger-menu-header {
                background: linear-gradient(135deg, #FF6B35 0%, #FFA726 100%);
                color: white;
                padding: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .hamburger-menu-header h3 {
                margin: 0;
                font-size: 1.3em;
            }

            .hamburger-close {
                background: none;
                border: none;
                color: white;
                font-size: 32px;
                cursor: pointer;
                padding: 0;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 4px;
                transition: background 0.2s;
            }

            .hamburger-close:hover {
                background: rgba(255, 255, 255, 0.2);
            }

            /* Menu Navigation */
            .hamburger-menu-nav {
                padding: 10px 0;
            }

            .hamburger-menu-item {
                display: flex;
                align-items: center;
                gap: 15px;
                padding: 15px 20px;
                color: #333;
                text-decoration: none;
                transition: all 0.2s;
                border-left: 4px solid transparent;
            }

            .hamburger-menu-item:hover {
                background: #f8f9fa;
                border-left-color: #FF6B35;
            }

            .hamburger-menu-item.active {
                background: #fff5f0;
                border-left-color: #FF6B35;
                color: #FF6B35;
                font-weight: 600;
            }

            .hamburger-menu-icon {
                font-size: 1.4em;
                width: 30px;
                text-align: center;
            }

            /* Mobile Responsive */
            @media (max-width: 768px) {
                .hamburger-menu-btn {
                    width: 36px;
                    height: 36px;
                }
                
                .hamburger-menu-btn span {
                    width: 20px;
                }
                
                .hamburger-side-menu {
                    width: 260px;
                    left: -260px;
                }
            }

            @media (max-width: 480px) {
                .hamburger-menu-btn {
                    width: 32px;
                    height: 32px;
                    padding: 6px;
                }
                
                .hamburger-menu-btn span {
                    width: 18px;
                    height: 2px;
                }
                
                .hamburger-side-menu {
                    width: 240px;
                    left: -240px;
                }
                
                .hamburger-menu-header {
                    padding: 15px;
                }
                
                .hamburger-menu-header h3 {
                    font-size: 1.1em;
                }
                
                .hamburger-menu-item {
                    padding: 12px 15px;
                    font-size: 0.95em;
                }
                
                .hamburger-menu-icon {
                    font-size: 1.2em;
                    width: 25px;
                }
            }
        `;
        document.head.appendChild(style);
    }

    attachEventListeners() {
        // Close menu on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const menu = document.getElementById('hamburgerSideMenu');
                if (menu && menu.classList.contains('active')) {
                    this.toggle();
                }
            }
        });

        // Close menu when clicking menu items
        document.querySelectorAll('.hamburger-menu-item').forEach(item => {
            item.addEventListener('click', () => {
                setTimeout(() => this.toggle(), 200);
            });
        });
    }

    toggle() {
        const menu = document.getElementById('hamburgerSideMenu');
        const overlay = document.querySelector('.hamburger-menu-overlay');
        
        if (!menu || !overlay) return;

        menu.classList.toggle('active');
        overlay.classList.toggle('active');
        
        // Prevent body scroll when menu is open
        if (menu.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }

    setActivePage() {
        const currentPage = window.location.pathname.toLowerCase();
        const menuItems = document.querySelectorAll('.hamburger-menu-item');
        
        menuItems.forEach(item => {
            item.classList.remove('active');
            
            const href = item.getAttribute('href').toLowerCase();
            if (currentPage.includes(href.replace('/', '').replace('.html', '')) ||
                (currentPage === '/' && href.includes('dashboard'))) {
                item.classList.add('active');
            }
        });
    }
}

// Initialize hamburger menu when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.hamburgerMenu = new HamburgerMenu();
    });
} else {
    window.hamburgerMenu = new HamburgerMenu();
}
