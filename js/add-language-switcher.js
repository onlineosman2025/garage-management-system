/**
 * Helper script to add language switcher to any page
 * Include this after translations.js
 */

(function() {
    // Check if we're on a page that should have a language switcher
    const excludedPages = ['index.html', 'check-currency.html', 'diagnostic.html'];
    const currentPage = window.location.pathname.split('/').pop();
    
    if (excludedPages.includes(currentPage)) {
        return; // Don't add switcher to these pages
    }

    // Add language switcher to header if it doesn't exist
    function addLanguageSwitcher() {
        // Find the header user-info or header-actions section
        const userInfo = document.querySelector('.user-info, .header-actions');
        
        if (userInfo && !document.querySelector('.language-switcher')) {
            // Create language switcher
            const langSwitcher = document.createElement('div');
            langSwitcher.className = 'language-switcher';
            langSwitcher.innerHTML = `
                <button class="lang-btn" onclick="switchLanguage('en')" id="lang-en">EN</button>
                <button class="lang-btn" onclick="switchLanguage('ar')" id="lang-ar">عربي</button>
                <button class="lang-btn" onclick="switchLanguage('ur')" id="lang-ur">اردو</button>
            `;
            
            // Insert at the beginning of user-info
            userInfo.insertBefore(langSwitcher, userInfo.firstChild);
            
            // Add CSS if not already present
            if (!document.getElementById('lang-switcher-styles')) {
                const style = document.createElement('style');
                style.id = 'lang-switcher-styles';
                style.textContent = `
                    .language-switcher {
                        display: flex;
                        gap: 8px;
                        margin-right: 15px;
                    }
                    .lang-btn {
                        background: rgba(255, 255, 255, 0.1);
                        color: white;
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        padding: 8px 12px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 0.85em;
                        font-weight: 500;
                        transition: all 0.3s;
                    }
                    .lang-btn:hover {
                        background: rgba(255, 255, 255, 0.2);
                        transform: translateY(-1px);
                    }
                    .lang-btn.active {
                        background: rgba(255, 255, 255, 0.3);
                        border-color: rgba(255, 255, 255, 0.5);
                    }
                `;
                document.head.appendChild(style);
            }
            
            // Initialize active language
            updateActiveLangButton();
        }
    }

    // Update active language button
    function updateActiveLangButton() {
        if (window.TranslationManager) {
            const currentLang = TranslationManager.getCurrentLanguage();
            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
            const activeLangBtn = document.getElementById(`lang-${currentLang}`);
            if (activeLangBtn) activeLangBtn.classList.add('active');
        }
    }

    // Make switchLanguage function globally available
    window.switchLanguage = function(lang) {
        if (window.TranslationManager) {
            TranslationManager.setLanguage(lang);
            updateActiveLangButton();
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addLanguageSwitcher);
    } else {
        addLanguageSwitcher();
    }
})();
