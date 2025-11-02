#!/usr/bin/env python3
"""
Role-Based Access Control (RBAC) for Garage Management System
"""
from pathlib import Path
import json

# Define permissions for each role
ROLE_PERMISSIONS = {
    'admin': {
        'users': ['create', 'read', 'update', 'delete'],
        'customers': ['create', 'read', 'update', 'delete'],
        'jobs': ['create', 'read', 'update', 'delete'],
        'invoices': ['create', 'read', 'update', 'delete', 'send_email'],
        'reports': ['read', 'export'],
        'settings': ['read', 'update'],
        'email': ['configure', 'send'],
        'pdf': ['generate', 'download']
    },
    'garage_owner': {
        'users': ['read'],
        'customers': ['create', 'read', 'update', 'delete'],
        'jobs': ['create', 'read', 'update', 'delete'],
        'invoices': ['create', 'read', 'update', 'delete', 'send_email'],
        'reports': ['read', 'export'],
        'settings': ['read', 'update'],
        'email': ['configure', 'send'],
        'pdf': ['generate', 'download']
    },
    'employee': {
        'users': [],
        'customers': ['create', 'read', 'update'],
        'jobs': ['create', 'read', 'update'],
        'invoices': ['create', 'read'],
        'reports': ['read'],
        'settings': ['read'],
        'email': ['send'],
        'pdf': ['generate']
    },
    'customer': {
        'users': [],
        'customers': ['read'],  # Only their own data
        'jobs': ['read'],  # Only their own jobs
        'invoices': ['read'],  # Only their own invoices
        'reports': [],
        'settings': [],
        'email': [],
        'pdf': ['generate']  # Only their own invoices
    }
}

def has_permission(user_role, resource, action):
    """
    Check if a user role has permission for a specific action on a resource
    
    Args:
        user_role: User's role (admin, garage_owner, employee, customer)
        resource: Resource type (users, customers, jobs, invoices, etc.)
        action: Action to perform (create, read, update, delete, etc.)
    
    Returns:
        bool: True if permission granted, False otherwise
    """
    if user_role not in ROLE_PERMISSIONS:
        return False
    
    resource_permissions = ROLE_PERMISSIONS[user_role].get(resource, [])
    return action in resource_permissions

def get_user_permissions(user_role):
    """Get all permissions for a user role"""
    return ROLE_PERMISSIONS.get(user_role, {})

def can_access_resource(user_role, user_id, resource_type, resource_owner_id=None):
    """
    Check if user can access a specific resource
    
    Args:
        user_role: User's role
        user_id: User's ID
        resource_type: Type of resource
        resource_owner_id: ID of the resource owner (for customer-specific checks)
    
    Returns:
        bool: True if access granted
    """
    # Admins and garage owners can access everything
    if user_role in ['admin', 'garage_owner']:
        return True
    
    # Employees can access most things except user management
    if user_role == 'employee':
        return resource_type != 'users'
    
    # Customers can only access their own data
    if user_role == 'customer':
        if resource_owner_id:
            return user_id == resource_owner_id
        return False
    
    return False

def require_permission(resource, action):
    """
    Decorator to require specific permission for an endpoint
    Usage: @require_permission('invoices', 'create')
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # Get user from request (would need to implement session/token management)
            # For now, this is a placeholder
            user_role = getattr(self, 'user_role', 'guest')
            
            if not has_permission(user_role, resource, action):
                self.send_error(403, f"Permission denied: {action} on {resource}")
                return
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def get_permission_matrix():
    """Get full permission matrix for documentation"""
    return ROLE_PERMISSIONS

def validate_role(role):
    """Check if role is valid"""
    return role in ROLE_PERMISSIONS

# Activity logging
class ActivityLogger:
    """Log user activities for audit trail"""
    
    def __init__(self):
        self.log_file = Path(__file__).parent / 'activity_log.json'
        self.logs = []
        self.load_logs()
    
    def load_logs(self):
        """Load existing logs"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    self.logs = json.load(f)
            except:
                self.logs = []
    
    def save_logs(self):
        """Save logs to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.logs[-1000:], f, indent=2)  # Keep last 1000 entries
    
    def log_activity(self, user_id, user_role, action, resource_type, resource_id=None, details=None):
        """Log a user activity"""
        from datetime import datetime
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'user_role': user_role,
            'action': action,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'details': details
        }
        
        self.logs.append(log_entry)
        self.save_logs()
        print(f"[ACTIVITY] {user_role} (ID:{user_id}) {action} {resource_type} {resource_id or ''}")
    
    def get_user_activity(self, user_id, limit=50):
        """Get activity logs for a specific user"""
        user_logs = [log for log in self.logs if log['user_id'] == user_id]
        return user_logs[-limit:]
    
    def get_recent_activity(self, limit=100):
        """Get recent activity across all users"""
        return self.logs[-limit:]
    
    def get_activity_by_resource(self, resource_type, resource_id=None):
        """Get activity for a specific resource"""
        if resource_id:
            return [log for log in self.logs 
                   if log['resource_type'] == resource_type 
                   and log.get('resource_id') == resource_id]
        return [log for log in self.logs if log['resource_type'] == resource_type]

# Global activity logger instance
activity_logger = ActivityLogger()

if __name__ == "__main__":
    print("Permissions Module")
    print("\nRole Permissions:")
    for role, perms in ROLE_PERMISSIONS.items():
        print(f"\n{role.upper()}:")
        for resource, actions in perms.items():
            print(f"  {resource}: {', '.join(actions)}")
