/**
 * PWA Installer
 * Handles service worker registration and install prompt
 */

class PWAInstaller {
    constructor() {
        this.deferredPrompt = null;
        this.init();
    }

    init() {
        // Register service worker
        if ('serviceWorker' in navigator) {
            this.registerServiceWorker();
        }

        // Handle install prompt
        window.addEventListener('beforeinstallprompt', (e) => {
            console.log('[PWA] Install prompt triggered');
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallButton();
        });

        // Handle app installed
        window.addEventListener('appinstalled', () => {
            console.log('[PWA] App installed successfully');
            this.hideInstallButton();
            this.deferredPrompt = null;
        });

        // Check if already installed
        if (window.matchMedia('(display-mode: standalone)').matches) {
            console.log('[PWA] App is running in standalone mode');
        }
    }

    async registerServiceWorker() {
        try {
            const registration = await navigator.serviceWorker.register('/service-worker.js', {
                scope: '/'
            });

            console.log('[PWA] Service Worker registered:', registration.scope);

            // Handle updates
            registration.addEventListener('updatefound', () => {
                const newWorker = registration.installing;
                console.log('[PWA] New Service Worker found');

                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        console.log('[PWA] New content available, please refresh');
                        this.showUpdateNotification();
                    }
                });
            });

        } catch (error) {
            console.error('[PWA] Service Worker registration failed:', error);
        }
    }

    showInstallButton() {
        // Create install button if it doesn't exist
        let installBtn = document.getElementById('pwa-install-btn');
        
        if (!installBtn) {
            installBtn = document.createElement('button');
            installBtn.id = 'pwa-install-btn';
            installBtn.className = 'pwa-install-button';
            installBtn.innerHTML = `
                <span class="install-icon">📱</span>
                <span>Install App</span>
            `;
            installBtn.onclick = () => this.promptInstall();

            // Add to page
            document.body.appendChild(installBtn);

            // Add CSS if not exists
            if (!document.getElementById('pwa-install-styles')) {
                const style = document.createElement('style');
                style.id = 'pwa-install-styles';
                style.textContent = `
                    .pwa-install-button {
                        position: fixed;
                        bottom: 20px;
                        right: 20px;
                        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                        color: white;
                        border: none;
                        padding: 12px 24px;
                        border-radius: 50px;
                        font-size: 14px;
                        font-weight: 600;
                        cursor: pointer;
                        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
                        z-index: 9999;
                        display: flex;
                        align-items: center;
                        gap: 8px;
                        transition: all 0.3s;
                        animation: slideInUp 0.5s ease;
                    }

                    .pwa-install-button:hover {
                        transform: translateY(-3px);
                        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
                    }

                    .pwa-install-button .install-icon {
                        font-size: 18px;
                    }

                    @keyframes slideInUp {
                        from {
                            transform: translateY(100px);
                            opacity: 0;
                        }
                        to {
                            transform: translateY(0);
                            opacity: 1;
                        }
                    }

                    @media (max-width: 768px) {
                        .pwa-install-button {
                            bottom: 80px;
                            right: 15px;
                            font-size: 13px;
                            padding: 10px 20px;
                        }
                    }
                `;
                document.head.appendChild(style);
            }
        }

        installBtn.style.display = 'flex';
    }

    hideInstallButton() {
        const installBtn = document.getElementById('pwa-install-btn');
        if (installBtn) {
            installBtn.style.display = 'none';
        }
    }

    async promptInstall() {
        if (!this.deferredPrompt) {
            console.log('[PWA] Install prompt not available');
            return;
        }

        // Show install prompt
        this.deferredPrompt.prompt();

        // Wait for user choice
        const { outcome } = await this.deferredPrompt.userChoice;
        console.log('[PWA] User choice:', outcome);

        if (outcome === 'accepted') {
            console.log('[PWA] User accepted install');
        } else {
            console.log('[PWA] User dismissed install');
        }

        // Clear prompt
        this.deferredPrompt = null;
        this.hideInstallButton();
    }

    showUpdateNotification() {
        // Create update notification
        const notification = document.createElement('div');
        notification.className = 'pwa-update-notification';
        notification.innerHTML = `
            <div class="update-content">
                <span class="update-icon">🔄</span>
                <div class="update-text">
                    <strong>New version available!</strong>
                    <p>Click to update and get the latest features</p>
                </div>
                <button class="update-btn" onclick="window.location.reload()">
                    Update Now
                </button>
            </div>
        `;

        // Add CSS if not exists
        if (!document.getElementById('pwa-update-styles')) {
            const style = document.createElement('style');
            style.id = 'pwa-update-styles';
            style.textContent = `
                .pwa-update-notification {
                    position: fixed;
                    top: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
                    z-index: 10000;
                    padding: 16px 20px;
                    min-width: 320px;
                    max-width: 500px;
                    animation: slideDown 0.5s ease;
                }

                .update-content {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }

                .update-icon {
                    font-size: 32px;
                }

                .update-text {
                    flex: 1;
                }

                .update-text strong {
                    display: block;
                    color: #333;
                    margin-bottom: 4px;
                }

                .update-text p {
                    color: #666;
                    font-size: 0.9em;
                    margin: 0;
                }

                .update-btn {
                    background: linear-gradient(135deg, #FF6600 0%, #FF8C32 100%);
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    white-space: nowrap;
                }

                @keyframes slideDown {
                    from {
                        transform: translate(-50%, -100px);
                        opacity: 0;
                    }
                    to {
                        transform: translate(-50%, 0);
                        opacity: 1;
                    }
                }

                @media (max-width: 768px) {
                    .pwa-update-notification {
                        min-width: auto;
                        width: calc(100% - 40px);
                        left: 20px;
                        transform: none;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(notification);

        // Auto-remove after 10 seconds
        setTimeout(() => {
            notification.remove();
        }, 10000);
    }
}

// Initialize PWA installer when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new PWAInstaller();
    });
} else {
    new PWAInstaller();
}
