# Available Login Accounts in Database

## Database Location
- **Main Database**: `c:\GMS\unified_app\garage.db`

## Current Login Accounts

### 1. Admin Account
- **Email**: `admin@garage.com`
- **Password**: `admin123` (default)
- **Name**: System Administrator
- **Role**: `admin`
- **Status**: Active
- **Last Login**: 2025-11-01T13:37:52

### 2. Garage Owner Account
- **Email**: `owner@garage.com`
- **Password**: `garage123` (default)
- **Name**: Ahmed Al-Rashid
- **Role**: `garage_owner`
- **Status**: Active
- **Last Login**: 2025-11-02T09:04:52

### 3. Customer Account
- **Email**: `customer@email.com`
- **Password**: (Not documented - check database hash)
- **Name**: Sarah Johnson
- **Role**: `customer`
- **Status**: Active
- **Last Login**: 2025-11-01T19:51:46

## Default Passwords (from code)

Based on the initialization scripts:
- **Admin**: `admin123`
- **Owner**: `garage123`

## Role Hierarchy

1. **admin** - Full system access
2. **garage_owner** - Garage management access
3. **technician** - Limited technical access
4. **customer** - Customer portal access

## How to Check Accounts

Run the following command from `c:\GMS\unified_app\`:
```bash
python check_users.py
```

Or query directly:
```bash
python -c "import sqlite3; conn = sqlite3.connect('garage.db'); cursor = conn.cursor(); cursor.execute('SELECT id, email, name, role FROM users'); [print(row) for row in cursor.fetchall()]; conn.close()"
```

## Database Schema

The `users` table contains:
- `id` - User ID (Primary Key)
- `email` - Email address (Unique)
- `password_hash` - SHA-256 hashed password
- `name` - Full name
- `role` - User role
- `phone` - Phone number
- `is_active` - Active status (1=active, 0=inactive)
- `created_at` - Account creation timestamp
- `last_login` - Last login timestamp

## Security Notes

- Passwords are hashed using SHA-256
- Default passwords should be changed in production
- All accounts are currently active
- Authentication is handled via `/api/auth/login` endpoint

## Creating New Users

To create a new user programmatically:
```python
from database import create_user

create_user(
    email='newuser@example.com',
    password='password123',
    name='New User',
    role='technician',  # or 'admin', 'garage_owner', 'customer'
    phone='+1234567890'
)
```

## Password Reset

To reset a user's password:
```python
from database import update_user

update_user(user_id, {'password': 'new_password'})
```
