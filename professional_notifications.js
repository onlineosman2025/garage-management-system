// Professional notification system to replace alert() popups
class ProfessionalNotifications {
    constructor() {
        this.createNotificationContainer();
    }

    createNotificationContainer() {
        if (document.getElementById('notification-container')) return;
        
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            pointer-events: none;
        `;
        document.body.appendChild(container);
    }

    show(message, type = 'success', duration = 4000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        const colors = {
            success: { bg: '#10b981', border: '#059669' },
            error: { bg: '#ef4444', border: '#dc2626' },
            warning: { bg: '#f59e0b', border: '#d97706' },
            info: { bg: '#3b82f6', border: '#2563eb' }
        };

        notification.innerHTML = `
            <div style="
                background: ${colors[type].bg};
                color: white;
                padding: 16px 20px;
                border-radius: 12px;
                border-left: 4px solid ${colors[type].border};
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                display: flex;
                align-items: center;
                gap: 12px;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 500;
                min-width: 300px;
                max-width: 400px;
                pointer-events: auto;
                cursor: pointer;
                transform: translateX(100%);
                transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
                margin-bottom: 12px;
            ">
                <span style="
                    background: rgba(255,255,255,0.2);
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    font-weight: bold;
                ">${icons[type]}</span>
                <span style="flex: 1;">${message}</span>
                <span style="
                    opacity: 0.7;
                    font-size: 18px;
                    cursor: pointer;
                    padding: 0 4px;
                " onclick="this.closest('.notification').remove()">×</span>
            </div>
        `;

        document.getElementById('notification-container').appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.firstElementChild.style.transform = 'translateX(0)';
        }, 100);

        // Auto remove
        setTimeout(() => {
            if (notification.parentNode) {
                notification.firstElementChild.style.transform = 'translateX(100%)';
                setTimeout(() => notification.remove(), 400);
            }
        }, duration);

        // Click to dismiss
        notification.addEventListener('click', () => {
            notification.firstElementChild.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 400);
        });
    }

    success(message, duration = 4000) {
        this.show(message, 'success', duration);
    }

    error(message, duration = 6000) {
        this.show(message, 'error', duration);
    }

    warning(message, duration = 5000) {
        this.show(message, 'warning', duration);
    }

    info(message, duration = 4000) {
        this.show(message, 'info', duration);
    }
}

// Global notification instance
window.notify = new ProfessionalNotifications();

// Override alert function for better UX
window.originalAlert = window.alert;
window.alert = function(message) {
    if (message.toLowerCase().includes('success') || message.toLowerCase().includes('created') || message.toLowerCase().includes('added')) {
        window.notify.success(message);
    } else if (message.toLowerCase().includes('error') || message.toLowerCase().includes('failed')) {
        window.notify.error(message);
    } else {
        window.notify.info(message);
    }
};
