/**
 * Frontend RBAC Manager
 * Handles role-based permissions and UI element visibility
 */

class RBACManager {
    constructor() {
        this.currentUser = null;
        this.permissions = [];
        this.role = null;
        this.init();
    }

    init() {
        // Load user data from localStorage
        const userData = localStorage.getItem('user_data');
        if (userData) {
            try {
                this.currentUser = JSON.parse(userData);
                this.role = this.currentUser.role || 'mechanic';
                this.permissions = this.getRolePermissions(this.role);
            } catch (e) {
                console.error('[RBAC] Error loading user data:', e);
            }
        }
    }

    getRolePermissions(role) {
        const rolePermissions = {
            'admin': [
                'system.manage', 'system.view_all_garages', 'system.manage_users',
                'garage.manage', 'garage.view',
                'customers.create', 'customers.read', 'customers.update', 'customers.delete',
                'vehicles.create', 'vehicles.read', 'vehicles.update', 'vehicles.delete',
                'jobs.create', 'jobs.read', 'jobs.update', 'jobs.delete', 'jobs.assign',
                'financials.view', 'financials.manage',
                'invoices.create', 'invoices.read', 'invoices.update', 'invoices.delete',
                'services.create', 'services.read', 'services.update', 'services.delete',
                'staff.create', 'staff.read', 'staff.update', 'staff.delete',
                'reports.view', 'reports.export'
            ],
            'owner': [
                'garage.manage', 'garage.view',
                'customers.create', 'customers.read', 'customers.update', 'customers.delete',
                'vehicles.create', 'vehicles.read', 'vehicles.update', 'vehicles.delete',
                'jobs.create', 'jobs.read', 'jobs.update', 'jobs.delete', 'jobs.assign',
                'financials.view', 'financials.manage',
                'invoices.create', 'invoices.read', 'invoices.update', 'invoices.delete',
                'services.create', 'services.read', 'services.update', 'services.delete',
                'staff.create', 'staff.read', 'staff.update', 'staff.delete',
                'reports.view', 'reports.export'
            ],
            'mechanic': [
                'customers.read', 'vehicles.read',
                'jobs.read', 'jobs.update',
                'services.read'
            ],
            'accountant': [
                'customers.read', 'vehicles.read', 'jobs.read',
                'financials.view', 'financials.manage',
                'invoices.create', 'invoices.read', 'invoices.update',
                'reports.view', 'reports.export'
            ],
            'receptionist': [
                'customers.create', 'customers.read', 'customers.update',
                'vehicles.create', 'vehicles.read', 'vehicles.update',
                'jobs.create', 'jobs.read',
                'services.read'
            ]
        };

        return rolePermissions[role] || [];
    }

    hasPermission(permission) {
        return this.permissions.includes(permission);
    }

    hasAnyPermission(permissions) {
        return permissions.some(perm => this.permissions.includes(perm));
    }

    hasAllPermissions(permissions) {
        return permissions.every(perm => this.permissions.includes(perm));
    }

    canCreate(resource) {
        return this.hasPermission(`${resource}.create`);
    }

    canRead(resource) {
        return this.hasPermission(`${resource}.read`);
    }

    canUpdate(resource) {
        return this.hasPermission(`${resource}.update`);
    }

    canDelete(resource) {
        return this.hasPermission(`${resource}.delete`);
    }

    // UI Helper Methods
    showElement(elementId, permission) {
        const element = document.getElementById(elementId);
        if (element) {
            if (this.hasPermission(permission)) {
                element.style.display = '';
            } else {
                element.style.display = 'none';
            }
        }
    }

    hideElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'none';
        }
    }

    disableElement(elementId, permission) {
        const element = document.getElementById(elementId);
        if (element) {
            if (!this.hasPermission(permission)) {
                element.disabled = true;
                element.style.opacity = '0.5';
                element.style.cursor = 'not-allowed';
                element.title = 'You do not have permission for this action';
            }
        }
    }

    applyPermissions() {
        // Apply permissions to all elements with data-permission attribute
        document.querySelectorAll('[data-permission]').forEach(element => {
            const permission = element.getAttribute('data-permission');
            if (!this.hasPermission(permission)) {
                element.style.display = 'none';
            }
        });

        // Apply permissions to elements with data-require-role attribute
        document.querySelectorAll('[data-require-role]').forEach(element => {
            const requiredRoles = element.getAttribute('data-require-role').split(',');
            if (!requiredRoles.includes(this.role)) {
                element.style.display = 'none';
            }
        });

        // Disable buttons without permission
        document.querySelectorAll('button[data-permission]').forEach(button => {
            const permission = button.getAttribute('data-permission');
            if (!this.hasPermission(permission)) {
                button.disabled = true;
                button.style.opacity = '0.5';
                button.style.cursor = 'not-allowed';
                button.title = 'You do not have permission for this action';
            }
        });
    }

    getRoleName() {
        const roleNames = {
            'admin': 'System Administrator',
            'owner': 'Garage Owner',
            'mechanic': 'Mechanic',
            'accountant': 'Accountant',
            'receptionist': 'Receptionist'
        };
        return roleNames[this.role] || 'User';
    }

    getRoleIcon() {
        const roleIcons = {
            'admin': '🔧',
            'owner': '🏪',
            'mechanic': '👨‍🔧',
            'accountant': '📊',
            'receptionist': '📋'
        };
        return roleIcons[this.role] || '👤';
    }

    getAvailableFeatures() {
        const features = {
            dashboard: this.hasPermission('garage.view'),
            customers: this.hasAnyPermission(['customers.read', 'customers.create']),
            vehicles: this.hasAnyPermission(['vehicles.read', 'vehicles.create']),
            jobs: this.hasAnyPermission(['jobs.read', 'jobs.create']),
            invoices: this.hasAnyPermission(['invoices.read', 'invoices.create']),
            services: this.hasAnyPermission(['services.read', 'services.create']),
            staff: this.hasAnyPermission(['staff.read', 'staff.create']),
            reports: this.hasPermission('reports.view'),
            settings: this.hasPermission('garage.manage'),
            financials: this.hasPermission('financials.view')
        };

        return features;
    }

    generateNavigationMenu() {
        const features = this.getAvailableFeatures();
        const menuItems = [];

        if (features.dashboard) {
            menuItems.push({
                name: 'Dashboard',
                icon: '📊',
                url: 'garage-dashboard.html',
                permission: 'garage.view'
            });
        }

        if (features.customers) {
            menuItems.push({
                name: 'Customers',
                icon: '👥',
                url: 'customers.html',
                permission: 'customers.read'
            });
        }

        if (features.vehicles) {
            menuItems.push({
                name: 'Vehicles',
                icon: '🚗',
                url: 'vehicles.html',
                permission: 'vehicles.read'
            });
        }

        if (features.jobs) {
            menuItems.push({
                name: 'Jobs',
                icon: '🔧',
                url: 'jobs.html',
                permission: 'jobs.read'
            });
        }

        if (features.invoices) {
            menuItems.push({
                name: 'Invoices',
                icon: '📄',
                url: 'invoices.html',
                permission: 'invoices.read'
            });
        }

        if (features.services) {
            menuItems.push({
                name: 'Services',
                icon: '⚙️',
                url: 'services.html',
                permission: 'services.read'
            });
        }

        if (features.staff) {
            menuItems.push({
                name: 'Staff',
                icon: '👨‍💼',
                url: 'users.html',
                permission: 'staff.read'
            });
        }

        if (features.reports) {
            menuItems.push({
                name: 'Reports',
                icon: '📈',
                url: 'reports.html',
                permission: 'reports.view'
            });
        }

        if (features.settings) {
            menuItems.push({
                name: 'Settings',
                icon: '⚙️',
                url: 'settings.html',
                permission: 'garage.manage'
            });
        }

        return menuItems;
    }

    displayRoleBadge() {
        const badge = document.createElement('div');
        badge.className = 'role-badge';
        badge.innerHTML = `
            <span class="role-icon">${this.getRoleIcon()}</span>
            <span class="role-name">${this.getRoleName()}</span>
        `;
        badge.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #FF6600 0%, #FF8C32 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 14px;
            box-shadow: 0 4px 15px rgba(255, 102, 0, 0.3);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 8px;
        `;
        document.body.appendChild(badge);
    }

    checkAccess(requiredPermission) {
        if (!this.hasPermission(requiredPermission)) {
            this.showAccessDenied(requiredPermission);
            return false;
        }
        return true;
    }

    showAccessDenied(requiredPermission) {
        const modal = document.createElement('div');
        modal.innerHTML = `
            <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 10000;">
                <div style="background: white; padding: 40px; border-radius: 20px; text-align: center; max-width: 400px;">
                    <div style="font-size: 64px; margin-bottom: 20px;">🔒</div>
                    <h2 style="color: #333; margin-bottom: 15px;">Access Denied</h2>
                    <p style="color: #666; margin-bottom: 10px;">You don't have permission to access this feature.</p>
                    <p style="color: #999; font-size: 14px; margin-bottom: 25px;">Required: ${requiredPermission}</p>
                    <button onclick="this.closest('div').parentElement.remove()" style="background: linear-gradient(135deg, #FF6600 0%, #FF8C32 100%); color: white; border: none; padding: 12px 30px; border-radius: 8px; font-weight: 600; cursor: pointer;">
                        OK
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
}

// Initialize RBAC Manager
let rbacManager;
document.addEventListener('DOMContentLoaded', () => {
    rbacManager = new RBACManager();
    rbacManager.applyPermissions();
    
    console.log('🔐 RBAC Manager initialized');
    console.log('👤 Role:', rbacManager.getRoleName());
    console.log('✅ Permissions:', rbacManager.permissions.length);
});
