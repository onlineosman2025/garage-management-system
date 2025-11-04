"""
Role-Based Access Control (RBAC) Permissions System
Defines roles, permissions, and access control for Garage Management System
"""

from functools import wraps
from flask import request, jsonify

# Define all available permissions
PERMISSIONS = {
    # System Management
    'system.manage': 'Manage system settings and configurations',
    'system.view_all_garages': 'View all garages in the system',
    'system.manage_users': 'Manage all users across garages',
    
    # Garage Management
    'garage.manage': 'Manage garage settings',
    'garage.view': 'View garage information',
    
    # Customer Management
    'customers.create': 'Create new customers',
    'customers.read': 'View customer information',
    'customers.update': 'Update customer information',
    'customers.delete': 'Delete customers',
    
    # Vehicle Management
    'vehicles.create': 'Add new vehicles',
    'vehicles.read': 'View vehicle information',
    'vehicles.update': 'Update vehicle information',
    'vehicles.delete': 'Delete vehicles',
    
    # Job Management
    'jobs.create': 'Create new jobs',
    'jobs.read': 'View jobs',
    'jobs.update': 'Update job status and details',
    'jobs.delete': 'Delete jobs',
    'jobs.assign': 'Assign jobs to mechanics',
    
    # Financial Management
    'financials.view': 'View financial reports and data',
    'financials.manage': 'Manage invoices and payments',
    'invoices.create': 'Create invoices',
    'invoices.read': 'View invoices',
    'invoices.update': 'Update invoices',
    'invoices.delete': 'Delete invoices',
    
    # Service Management
    'services.create': 'Add new services',
    'services.read': 'View services',
    'services.update': 'Update service details',
    'services.delete': 'Delete services',
    
    # Staff Management
    'staff.create': 'Add new staff members',
    'staff.read': 'View staff information',
    'staff.update': 'Update staff details',
    'staff.delete': 'Remove staff members',
    
    # Reports
    'reports.view': 'View reports',
    'reports.export': 'Export reports',
}

# Define role permissions
ROLE_PERMISSIONS = {
    'admin': [
        # System Admin has ALL permissions
        'system.manage',
        'system.view_all_garages',
        'system.manage_users',
        'garage.manage',
        'garage.view',
        'customers.create',
        'customers.read',
        'customers.update',
        'customers.delete',
        'vehicles.create',
        'vehicles.read',
        'vehicles.update',
        'vehicles.delete',
        'jobs.create',
        'jobs.read',
        'jobs.update',
        'jobs.delete',
        'jobs.assign',
        'financials.view',
        'financials.manage',
        'invoices.create',
        'invoices.read',
        'invoices.update',
        'invoices.delete',
        'services.create',
        'services.read',
        'services.update',
        'services.delete',
        'staff.create',
        'staff.read',
        'staff.update',
        'staff.delete',
        'reports.view',
        'reports.export',
    ],
    
    'owner': [
        # Garage Owner - Full control of their garage
        'garage.manage',
        'garage.view',
        'customers.create',
        'customers.read',
        'customers.update',
        'customers.delete',
        'vehicles.create',
        'vehicles.read',
        'vehicles.update',
        'vehicles.delete',
        'jobs.create',
        'jobs.read',
        'jobs.update',
        'jobs.delete',
        'jobs.assign',
        'financials.view',
        'financials.manage',
        'invoices.create',
        'invoices.read',
        'invoices.update',
        'invoices.delete',
        'services.create',
        'services.read',
        'services.update',
        'services.delete',
        'staff.create',
        'staff.read',
        'staff.update',
        'staff.delete',
        'reports.view',
        'reports.export',
    ],
    
    'mechanic': [
        # Mechanic - Limited to job management
        'customers.read',
        'vehicles.read',
        'jobs.read',
        'jobs.update',
        'services.read',
    ],
    
    'accountant': [
        # Accountant - Financial focus
        'customers.read',
        'vehicles.read',
        'jobs.read',
        'financials.view',
        'financials.manage',
        'invoices.create',
        'invoices.read',
        'invoices.update',
        'reports.view',
        'reports.export',
    ],
    
    'receptionist': [
        # Receptionist - Customer and job intake
        'customers.create',
        'customers.read',
        'customers.update',
        'vehicles.create',
        'vehicles.read',
        'vehicles.update',
        'jobs.create',
        'jobs.read',
        'services.read',
    ],
}

class RBACManager:
    """Role-Based Access Control Manager"""
    
    @staticmethod
    def has_permission(role, permission):
        """Check if a role has a specific permission"""
        if not role or role not in ROLE_PERMISSIONS:
            return False
        return permission in ROLE_PERMISSIONS.get(role, [])
    
    @staticmethod
    def has_any_permission(role, permissions):
        """Check if role has any of the given permissions"""
        if not role or role not in ROLE_PERMISSIONS:
            return False
        role_perms = ROLE_PERMISSIONS.get(role, [])
        return any(perm in role_perms for perm in permissions)
    
    @staticmethod
    def has_all_permissions(role, permissions):
        """Check if role has all of the given permissions"""
        if not role or role not in ROLE_PERMISSIONS:
            return False
        role_perms = ROLE_PERMISSIONS.get(role, [])
        return all(perm in role_perms for perm in permissions)
    
    @staticmethod
    def get_role_permissions(role):
        """Get all permissions for a role"""
        return ROLE_PERMISSIONS.get(role, [])
    
    @staticmethod
    def get_user_permissions(user_data):
        """Get permissions for a user based on their role"""
        role = user_data.get('role', 'mechanic')
        return RBACManager.get_role_permissions(role)


def require_permission(permission):
    """
    Decorator to require specific permission for an endpoint
    Usage: @require_permission('customers.create')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get user info from request (you'll need to implement token verification)
            auth_header = request.headers.get('Authorization', '')
            
            # For now, we'll extract role from token (simplified)
            # In production, verify JWT token and extract user info
            if not auth_header:
                return jsonify({'error': 'Authentication required'}), 401
            
            # Extract user role from token (simplified - implement proper JWT verification)
            try:
                # This is a placeholder - implement proper token verification
                token_parts = auth_header.replace('Bearer ', '').split('_')
                # Token format: token_garage_id_user_id
                # You'll need to fetch user role from database
                
                # For demo purposes, we'll check a header
                user_role = request.headers.get('X-User-Role', 'mechanic')
                
                if not RBACManager.has_permission(user_role, permission):
                    return jsonify({
                        'error': 'Permission denied',
                        'required_permission': permission,
                        'user_role': user_role
                    }), 403
                
            except Exception as e:
                return jsonify({'error': 'Invalid authentication token'}), 401
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_role(allowed_roles):
    """
    Decorator to require specific role(s) for an endpoint
    Usage: @require_role(['admin', 'owner'])
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            
            if not auth_header:
                return jsonify({'error': 'Authentication required'}), 401
            
            try:
                # Get user role (implement proper token verification)
                user_role = request.headers.get('X-User-Role', 'mechanic')
                
                if user_role not in allowed_roles:
                    return jsonify({
                        'error': 'Access denied',
                        'required_roles': allowed_roles,
                        'user_role': user_role
                    }), 403
                
            except Exception as e:
                return jsonify({'error': 'Invalid authentication token'}), 401
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_user_from_token(token):
    """
    Extract user information from authentication token
    This is a placeholder - implement proper JWT verification
    """
    # TODO: Implement JWT token verification
    # For now, return mock data
    return {
        'user_id': 1,
        'role': 'owner',
        'garage_id': 'demo123'
    }


# Export permission checking functions for frontend
def get_permissions_for_role(role):
    """Get all permissions for a specific role (for frontend)"""
    return {
        'role': role,
        'permissions': ROLE_PERMISSIONS.get(role, []),
        'permission_descriptions': {
            perm: PERMISSIONS.get(perm, '')
            for perm in ROLE_PERMISSIONS.get(role, [])
        }
    }


# Role hierarchy for display
ROLE_HIERARCHY = {
    'admin': {
        'name': 'System Administrator',
        'icon': '🔧',
        'level': 1,
        'description': 'Full system access and control'
    },
    'owner': {
        'name': 'Garage Owner',
        'icon': '🏪',
        'level': 2,
        'description': 'Full control of their garage'
    },
    'accountant': {
        'name': 'Accountant',
        'icon': '📊',
        'level': 3,
        'description': 'Financial management and reporting'
    },
    'receptionist': {
        'name': 'Receptionist',
        'icon': '📋',
        'level': 4,
        'description': 'Customer service and job intake'
    },
    'mechanic': {
        'name': 'Mechanic',
        'icon': '👨‍🔧',
        'level': 5,
        'description': 'Job execution and updates'
    }
}
