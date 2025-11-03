/**
 * Trial Tracker - 14 Days Free Trial Progress Bar
 * Shows remaining trial days and upgrade prompts
 */

class TrialTracker {
    constructor() {
        this.trialDays = 14;
        this.init();
    }

    init() {
        this.checkTrialStatus();
        this.renderTrialBar();
        this.startDailyCheck();
    }

    checkTrialStatus() {
        const trialStartDate = localStorage.getItem('trial_start_date');
        const trialEndDate = localStorage.getItem('trial_end_date');
        
        if (!trialStartDate || !trialEndDate) {
            // Set trial dates if not exists
            const startDate = new Date();
            const endDate = new Date();
            endDate.setDate(endDate.getDate() + this.trialDays);
            
            localStorage.setItem('trial_start_date', startDate.toISOString());
            localStorage.setItem('trial_end_date', endDate.toISOString());
        }
    }

    getDaysRemaining() {
        const trialEndDate = new Date(localStorage.getItem('trial_end_date'));
        const today = new Date();
        const diffTime = trialEndDate - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        return Math.max(0, diffDays);
    }

    getTrialProgress() {
        const daysRemaining = this.getDaysRemaining();
        const daysUsed = this.trialDays - daysRemaining;
        const percentage = (daysUsed / this.trialDays) * 100;
        
        return {
            daysRemaining,
            daysUsed,
            percentage: Math.min(100, Math.max(0, percentage)),
            isExpired: daysRemaining <= 0
        };
    }

    renderTrialBar() {
        const progress = this.getTrialProgress();
        
        // Create trial bar HTML
        const trialBarHTML = `
            <div class="trial-progress-bar" id="trial-progress-bar">
                <div class="trial-header">
                    <div class="trial-info">
                        <i class="fas fa-gift"></i>
                        <span class="trial-text">
                            ${progress.isExpired ? 
                                '<strong>Trial Expired</strong>' : 
                                `<strong>${progress.daysRemaining} Days</strong> left in your trial`
                            }
                        </span>
                    </div>
                    <button class="upgrade-btn" onclick="trialTracker.showUpgradeModal()">
                        <i class="fas fa-crown"></i> Upgrade Now
                    </button>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill ${progress.isExpired ? 'expired' : ''}" 
                         style="width: ${progress.percentage}%">
                    </div>
                </div>
                <div class="trial-footer">
                    <span class="trial-days-info">
                        Day ${progress.daysUsed} of ${this.trialDays}
                    </span>
                    <span class="trial-end-date">
                        ${progress.isExpired ? 
                            'Trial ended' : 
                            `Ends on ${this.formatDate(localStorage.getItem('trial_end_date'))}`
                        }
                    </span>
                </div>
            </div>
        `;
        
        // Insert trial bar at the top of the page
        const targetElement = document.querySelector('.header') || document.body;
        const trialBar = document.createElement('div');
        trialBar.innerHTML = trialBarHTML;
        targetElement.parentNode.insertBefore(trialBar.firstElementChild, targetElement.nextSibling);
        
        // Add styles
        this.addStyles();
        
        // Show warning if trial is ending soon
        if (progress.daysRemaining <= 3 && progress.daysRemaining > 0) {
            this.showTrialWarning(progress.daysRemaining);
        }
        
        // Show expired message if trial ended
        if (progress.isExpired) {
            this.showTrialExpiredModal();
        }
    }

    addStyles() {
        if (document.getElementById('trial-tracker-styles')) return;
        
        const styles = `
            <style id="trial-tracker-styles">
                .trial-progress-bar {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 20px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    animation: slideDown 0.5s ease-out;
                }
                
                @keyframes slideDown {
                    from {
                        opacity: 0;
                        transform: translateY(-20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                .trial-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }
                
                .trial-info {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                
                .trial-info i {
                    font-size: 20px;
                }
                
                .trial-text {
                    font-size: 14px;
                }
                
                .upgrade-btn {
                    background: rgba(255,255,255,0.2);
                    color: white;
                    border: 2px solid white;
                    padding: 8px 20px;
                    border-radius: 25px;
                    cursor: pointer;
                    font-weight: 600;
                    transition: all 0.3s;
                    font-size: 14px;
                }
                
                .upgrade-btn:hover {
                    background: white;
                    color: #667eea;
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }
                
                .progress-bar-container {
                    background: rgba(255,255,255,0.3);
                    height: 8px;
                    border-radius: 10px;
                    overflow: hidden;
                    margin-bottom: 8px;
                }
                
                .progress-bar-fill {
                    height: 100%;
                    background: white;
                    border-radius: 10px;
                    transition: width 0.5s ease-out;
                    box-shadow: 0 0 10px rgba(255,255,255,0.5);
                }
                
                .progress-bar-fill.expired {
                    background: #ef4444;
                }
                
                .trial-footer {
                    display: flex;
                    justify-content: space-between;
                    font-size: 12px;
                    opacity: 0.9;
                }
                
                @media (max-width: 768px) {
                    .trial-header {
                        flex-direction: column;
                        gap: 10px;
                        align-items: flex-start;
                    }
                    
                    .upgrade-btn {
                        width: 100%;
                        text-align: center;
                    }
                }
            </style>
        `;
        
        document.head.insertAdjacentHTML('beforeend', styles);
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }

    showTrialWarning(daysRemaining) {
        // Show a notification about trial ending soon
        setTimeout(() => {
            if (typeof showNotification === 'function') {
                showNotification(
                    `⚠️ Your trial ends in ${daysRemaining} days. Upgrade now to continue using all features!`,
                    'warning'
                );
            }
        }, 2000);
    }

    showTrialExpiredModal() {
        const modalHTML = `
            <div class="trial-expired-modal" id="trial-expired-modal">
                <div class="trial-expired-content">
                    <div class="trial-expired-icon">
                        <i class="fas fa-hourglass-end"></i>
                    </div>
                    <h2>Your Trial Has Ended</h2>
                    <p>Thank you for trying our Garage Management System!</p>
                    <p>Upgrade now to continue managing your garage efficiently.</p>
                    <div class="trial-expired-actions">
                        <button class="upgrade-now-btn" onclick="trialTracker.showUpgradeModal()">
                            <i class="fas fa-crown"></i> Upgrade Now
                        </button>
                        <button class="contact-btn" onclick="trialTracker.contactSupport()">
                            <i class="fas fa-envelope"></i> Contact Support
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.addModalStyles();
    }

    addModalStyles() {
        if (document.getElementById('trial-modal-styles')) return;
        
        const styles = `
            <style id="trial-modal-styles">
                .trial-expired-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0,0,0,0.8);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                    animation: fadeIn 0.3s ease-out;
                }
                
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                
                .trial-expired-content {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    text-align: center;
                    max-width: 500px;
                    animation: scaleIn 0.3s ease-out;
                }
                
                @keyframes scaleIn {
                    from {
                        opacity: 0;
                        transform: scale(0.9);
                    }
                    to {
                        opacity: 1;
                        transform: scale(1);
                    }
                }
                
                .trial-expired-icon {
                    font-size: 64px;
                    color: #f59e0b;
                    margin-bottom: 20px;
                }
                
                .trial-expired-content h2 {
                    color: #333;
                    margin-bottom: 15px;
                }
                
                .trial-expired-content p {
                    color: #666;
                    margin-bottom: 10px;
                    line-height: 1.6;
                }
                
                .trial-expired-actions {
                    display: flex;
                    gap: 15px;
                    margin-top: 30px;
                }
                
                .upgrade-now-btn,
                .contact-btn {
                    flex: 1;
                    padding: 15px 25px;
                    border: none;
                    border-radius: 10px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s;
                }
                
                .upgrade-now-btn {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                
                .upgrade-now-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
                }
                
                .contact-btn {
                    background: #f3f4f6;
                    color: #333;
                }
                
                .contact-btn:hover {
                    background: #e5e7eb;
                }
            </style>
        `;
        
        document.head.insertAdjacentHTML('beforeend', styles);
    }

    showUpgradeModal() {
        alert('Upgrade feature coming soon!\n\nContact us at:\nsupport@garagemanagement.com\n+971 50 123 4567');
    }

    contactSupport() {
        window.location.href = 'mailto:support@garagemanagement.com?subject=Trial Upgrade Inquiry';
    }

    startDailyCheck() {
        // Check trial status every hour
        setInterval(() => {
            const progress = this.getTrialProgress();
            if (progress.isExpired) {
                this.showTrialExpiredModal();
            }
        }, 3600000); // 1 hour
    }
}

// Initialize trial tracker when DOM is loaded
let trialTracker;
document.addEventListener('DOMContentLoaded', () => {
    trialTracker = new TrialTracker();
});
