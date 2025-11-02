#!/usr/bin/env python3
"""
SQLite Database Module for Garage Management System
Handles all database operations with automatic initialization
"""
import sqlite3
import json
import hashlib
import secrets
from datetime import datetime
from pathlib import Path

DB_FILE = Path(__file__).parent / 'garage.db'

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_database():
    """Initialize database with tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            phone TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            total_jobs INTEGER DEFAULT 0,
            total_spent REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            vehicle TEXT NOT NULL,
            service_type TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            estimated_cost REAL DEFAULT 0.0,
            date TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # Invoices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            job_id INTEGER,
            amount REAL NOT NULL,
            tax_rate REAL DEFAULT 5.0,
            tax_amount REAL NOT NULL,
            total_amount REAL NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            due_date TEXT,
            payment_terms TEXT DEFAULT 'net_30',
            created_at TEXT,
            paid_at TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        )
    ''')
    
    # Settings table for garage configuration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Services table for managing service types
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_ar TEXT,
            name_ur TEXT,
            description TEXT,
            default_price REAL DEFAULT 0.0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Vehicles table for managing vehicle information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER,
            plate_number TEXT,
            vin TEXT,
            color TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"[DB] Database initialized at {DB_FILE}")

# ============= CUSTOMER OPERATIONS =============

def get_all_customers():
    """Get all customers"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers ORDER BY id DESC')
    customers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return customers

def get_customer_by_id(customer_id):
    """Get customer by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_customer(data):
    """Create new customer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO customers (name, email, phone, address)
        VALUES (?, ?, ?, ?)
    ''', (data['name'], data['email'], data.get('phone', ''), data.get('address', '')))
    customer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"[DB] Created customer #{customer_id}: {data['name']}")
    return get_customer_by_id(customer_id)

def update_customer(customer_id, data):
    """Update customer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE customers 
        SET name = ?, email = ?, phone = ?, address = ?
        WHERE id = ?
    ''', (data['name'], data['email'], data.get('phone', ''), data.get('address', ''), customer_id))
    conn.commit()
    conn.close()
    print(f"[DB] Updated customer #{customer_id}")
    return get_customer_by_id(customer_id)

def delete_customer(customer_id):
    """Delete customer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
    conn.commit()
    conn.close()
    print(f"[DB] Deleted customer #{customer_id}")

# ============= JOB OPERATIONS =============

def get_all_jobs(limit=None):
    """Get all jobs"""
    conn = get_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM jobs ORDER BY id DESC'
    if limit:
        query += f' LIMIT {limit}'
    cursor.execute(query)
    jobs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Enrich with customer names
    for job in jobs:
        customer = get_customer_by_id(job['customer_id'])
        job['customer_name'] = customer['name'] if customer else 'Unknown Customer'
    
    return jobs

def get_job_by_id(job_id):
    """Get job by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        job = dict(row)
        customer = get_customer_by_id(job['customer_id'])
        job['customer_name'] = customer['name'] if customer else 'Unknown Customer'
        return job
    return None

def create_job(data):
    """Create new job"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO jobs (customer_id, vehicle, service_type, status, estimated_cost, date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['customer_id'],
        data['vehicle'],
        data['service_type'],
        data.get('status', 'pending'),
        data.get('estimated_cost', 0),
        data.get('date', datetime.now().strftime('%Y-%m-%d')),
        data.get('notes', '')
    ))
    job_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"[DB] Created job #{job_id}")
    return get_job_by_id(job_id)

def update_job_status(job_id, status):
    """Update job status"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE jobs SET status = ? WHERE id = ?', (status, job_id))
    conn.commit()
    conn.close()
    print(f"[DB] Updated job #{job_id} status to {status}")
    return get_job_by_id(job_id)

# ============= INVOICE OPERATIONS =============

def get_all_invoices(customer_id=None):
    """Get all invoices, optionally filtered by customer"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if customer_id:
        cursor.execute('SELECT * FROM invoices WHERE customer_id = ? ORDER BY id DESC', (customer_id,))
    else:
        cursor.execute('SELECT * FROM invoices ORDER BY id DESC')
    
    invoices = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Enrich with customer names
    for invoice in invoices:
        customer = get_customer_by_id(invoice['customer_id'])
        invoice['customer_name'] = customer['name'] if customer else 'Unknown Customer'
    
    return invoices

def get_invoice_by_id(invoice_id):
    """Get invoice by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM invoices WHERE id = ?', (invoice_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        invoice = dict(row)
        customer = get_customer_by_id(invoice['customer_id'])
        invoice['customer_name'] = customer['name'] if customer else 'Unknown Customer'
        return invoice
    return None

def create_invoice(data):
    """Create new invoice"""
    conn = get_connection()
    cursor = conn.cursor()
    
    amount = float(data['amount'])
    tax_rate = float(data.get('tax_rate', 5))
    tax_amount = round(amount * (tax_rate / 100), 2)
    total_amount = round(amount + tax_amount, 2)
    
    cursor.execute('''
        INSERT INTO invoices (
            customer_id, job_id, amount, tax_rate, tax_amount, total_amount,
            description, status, due_date, payment_terms, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['customer_id'],
        data.get('job_id'),
        amount,
        tax_rate,
        tax_amount,
        total_amount,
        data.get('description', ''),
        'pending',
        data.get('due_date', ''),
        data.get('payment_terms', 'net_30'),
        datetime.now().strftime('%Y-%m-%d')
    ))
    invoice_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"[DB] Created invoice #{invoice_id}")
    return get_invoice_by_id(invoice_id)

def update_invoice(invoice_id, data):
    """Update invoice"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Recalculate if amount or tax changed
    if 'amount' in data or 'tax_rate' in data:
        current = get_invoice_by_id(invoice_id)
        amount = float(data.get('amount', current['amount']))
        tax_rate = float(data.get('tax_rate', current['tax_rate']))
        tax_amount = round(amount * (tax_rate / 100), 2)
        total_amount = round(amount + tax_amount, 2)
        
        cursor.execute('''
            UPDATE invoices 
            SET amount = ?, tax_rate = ?, tax_amount = ?, total_amount = ?
            WHERE id = ?
        ''', (amount, tax_rate, tax_amount, total_amount, invoice_id))
    
    conn.commit()
    conn.close()
    print(f"[DB] Updated invoice #{invoice_id}")
    return get_invoice_by_id(invoice_id)

def mark_invoice_paid(invoice_id):
    """Mark invoice as paid"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE invoices 
        SET status = 'paid', paid_at = ?
        WHERE id = ?
    ''', (datetime.now().strftime('%Y-%m-%d'), invoice_id))
    conn.commit()
    conn.close()
    print(f"[DB] Invoice #{invoice_id} marked as paid")
    return get_invoice_by_id(invoice_id)

def delete_invoice(invoice_id):
    """Delete invoice"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM invoices WHERE id = ?', (invoice_id,))
    conn.commit()
    conn.close()
    print(f"[DB] Deleted invoice #{invoice_id}")

# ============= DASHBOARD STATS =============

def get_dashboard_stats():
    """Get dashboard statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total customers
    cursor.execute('SELECT COUNT(*) as count FROM customers')
    total_customers = cursor.fetchone()['count']
    
    # Active jobs (not completed)
    cursor.execute("SELECT COUNT(*) as count FROM jobs WHERE status != 'completed'")
    active_jobs = cursor.fetchone()['count']
    
    # Monthly revenue (completed jobs)
    cursor.execute("SELECT SUM(estimated_cost) as total FROM jobs WHERE status = 'completed'")
    result = cursor.fetchone()
    monthly_revenue = result['total'] if result['total'] else 0
    
    # Pending invoices
    cursor.execute("SELECT COUNT(*) as count FROM invoices WHERE status = 'pending'")
    pending_invoices = cursor.fetchone()['count']
    
    conn.close()
    
    return {
        'total_customers': total_customers,
        'total_jobs': active_jobs,
        'monthly_revenue': monthly_revenue,
        'pending_invoices': pending_invoices
    }

# ============= USER AUTHENTICATION =============

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hash_password(password) == password_hash

def create_user(email, password, name, role='garage_owner', phone=''):
    """Create new user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO users (email, password_hash, name, role, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, password_hash, name, role, phone))
        user_id = cursor.lastrowid
        conn.commit()
        print(f"[DB] Created user #{user_id}: {email} ({role})")
        return get_user_by_id(user_id)
    except sqlite3.IntegrityError:
        print(f"[DB] User with email {email} already exists")
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    """Get user by email"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def authenticate_user(email, password):
    """Authenticate user and return user data"""
    user = get_user_by_email(email)
    if user and verify_password(password, user['password_hash']):
        # Update last login
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET last_login = ? WHERE id = ?
        ''', (datetime.now().isoformat(), user['id']))
        conn.commit()
        conn.close()
        
        # Remove password hash from returned data
        user_data = dict(user)
        del user_data['password_hash']
        print(f"[DB] User authenticated: {email}")
        return user_data
    return None

def get_all_users():
    """Get all users (without password hashes)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, name, role, phone, is_active, created_at, last_login FROM users ORDER BY id DESC')
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

def update_user(user_id, data):
    """Update user data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Build update query dynamically
    fields = []
    values = []
    
    if 'name' in data:
        fields.append('name = ?')
        values.append(data['name'])
    if 'phone' in data:
        fields.append('phone = ?')
        values.append(data['phone'])
    if 'role' in data:
        fields.append('role = ?')
        values.append(data['role'])
    if 'is_active' in data:
        fields.append('is_active = ?')
        values.append(data['is_active'])
    if 'password' in data:
        fields.append('password_hash = ?')
        values.append(hash_password(data['password']))
    
    if fields:
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        print(f"[DB] Updated user #{user_id}")
    
    conn.close()
    return get_user_by_id(user_id)

def delete_user(user_id):
    """Delete user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    print(f"[DB] Deleted user #{user_id}")

def create_default_users():
    """Create default users if they don't exist"""
    default_users = [
        ('admin@garage.com', 'admin123', 'System Administrator', 'admin'),
        ('owner@garage.com', 'garage123', 'Ahmed Al-Rashid', 'garage_owner'),
        ('customer@email.com', 'customer123', 'Sarah Johnson', 'customer')
    ]
    
    for email, password, name, role in default_users:
        if not get_user_by_email(email):
            create_user(email, password, name, role)

# ============= SETTINGS OPERATIONS =============

def get_setting(key, default=None):
    """Get a setting value"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    return row['value'] if row else default

def set_setting(key, value):
    """Set a setting value"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO settings (key, value, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', (key, value))
    conn.commit()
    conn.close()
    print(f"[DB] Setting updated: {key} = {value}")

def get_all_settings():
    """Get all settings as a dictionary"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM settings')
    settings = {row['key']: row['value'] for row in cursor.fetchall()}
    conn.close()
    return settings

def get_garage_info():
    """Get garage information for invoices and emails"""
    return {
        'name': get_setting('garage_name', ''),
        'address': get_setting('garage_address', ''),
        'phone': get_setting('garage_phone', ''),
        'email': get_setting('garage_email', ''),
        'tax_number': get_setting('garage_tax_number', ''),
        'license_number': get_setting('garage_license_number', '')
    }

def init_default_settings():
    """Initialize default settings if they don't exist"""
    defaults = {
        'garage_name': '',
        'garage_address': '',
        'garage_phone': '',
        'garage_email': '',
        'currency': 'AED',
        'tax_rate': '5.0',
        'language': 'en'
    }
    
    for key, value in defaults.items():
        if get_setting(key) is None:
            set_setting(key, value)
    
    print("[DB] Default settings initialized")

# ============= SERVICE OPERATIONS =============

def get_all_services(active_only=False):
    """Get all services"""
    conn = get_connection()
    cursor = conn.cursor()
    if active_only:
        cursor.execute('SELECT * FROM services WHERE is_active = 1 ORDER BY name')
    else:
        cursor.execute('SELECT * FROM services ORDER BY name')
    services = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return services

def get_service_by_id(service_id):
    """Get service by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM services WHERE id = ?', (service_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_service(data):
    """Create new service"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO services (name, name_ar, name_ur, description, default_price, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data.get('name_ar', ''),
        data.get('name_ur', ''),
        data.get('description', ''),
        data.get('default_price', 0.0),
        data.get('is_active', 1)
    ))
    service_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"[DB] Created service #{service_id}: {data['name']}")
    return get_service_by_id(service_id)

def update_service(service_id, data):
    """Update service"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE services 
        SET name = ?, name_ar = ?, name_ur = ?, description = ?, 
            default_price = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (
        data['name'],
        data.get('name_ar', ''),
        data.get('name_ur', ''),
        data.get('description', ''),
        data.get('default_price', 0.0),
        data.get('is_active', 1),
        service_id
    ))
    conn.commit()
    conn.close()
    print(f"[DB] Updated service #{service_id}")
    return get_service_by_id(service_id)

def delete_service(service_id):
    """Delete service (soft delete by setting is_active to 0)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE services SET is_active = 0 WHERE id = ?', (service_id,))
    conn.commit()
    conn.close()
    print(f"[DB] Deleted service #{service_id}")
    return True

def init_default_services():
    """Initialize default services if table is empty"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM services')
    count = cursor.fetchone()['count']
    conn.close()
    
    if count == 0:
        default_services = [
            {'name': 'Oil Change', 'name_ar': 'تغيير الزيت', 'name_ur': 'تیل کی تبدیلی', 'description': 'Engine oil change service', 'default_price': 150.0},
            {'name': 'Brake Service', 'name_ar': 'خدمة الفرامل', 'name_ur': 'بریک کی سروس', 'description': 'Brake inspection and repair', 'default_price': 300.0},
            {'name': 'Engine Repair', 'name_ar': 'إصلاح المحرك', 'name_ur': 'انجن کی مرمت', 'description': 'Engine diagnostics and repair', 'default_price': 800.0},
            {'name': 'AC Service', 'name_ar': 'خدمة التكييف', 'name_ur': 'اے سی کی سروس', 'description': 'Air conditioning service', 'default_price': 250.0},
            {'name': 'Transmission Repair', 'name_ar': 'إصلاح ناقل الحركة', 'name_ur': 'ٹرانسمیشن کی مرمت', 'description': 'Transmission service and repair', 'default_price': 1200.0},
            {'name': 'Diagnostic', 'name_ar': 'التشخيص', 'name_ur': 'تشخیص', 'description': 'Vehicle diagnostic check', 'default_price': 100.0},
            {'name': 'Tire Service', 'name_ar': 'خدمة الإطارات', 'name_ur': 'ٹائر کی سروس', 'description': 'Tire rotation, balancing, and replacement', 'default_price': 200.0},
            {'name': 'Battery Service', 'name_ar': 'خدمة البطارية', 'name_ur': 'بیٹری کی سروس', 'description': 'Battery testing and replacement', 'default_price': 180.0}
        ]
        
        for service in default_services:
            create_service(service)
        
        print("[DB] Default services initialized")

# ============= VEHICLE OPERATIONS =============

def get_all_vehicles(active_only=False, customer_id=None):
    """Get all vehicles with optional filtering"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM vehicles WHERE 1=1'
    params = []
    
    if active_only:
        query += ' AND is_active = 1'
    
    if customer_id:
        query += ' AND customer_id = ?'
        params.append(customer_id)
    
    query += ' ORDER BY created_at DESC'
    
    cursor.execute(query, params)
    vehicles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return vehicles

def get_vehicle_by_id(vehicle_id):
    """Get vehicle by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles WHERE id = ?', (vehicle_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_vehicle(data):
    """Create new vehicle"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vehicles (customer_id, make, model, year, plate_number, vin, color, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('customer_id'),
        data['make'],
        data['model'],
        data.get('year'),
        data.get('plate_number', ''),
        data.get('vin', ''),
        data.get('color', ''),
        data.get('is_active', 1)
    ))
    vehicle_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"[DB] Created vehicle #{vehicle_id}")
    return get_vehicle_by_id(vehicle_id)

def update_vehicle(vehicle_id, data):
    """Update vehicle"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE vehicles 
        SET customer_id = ?, make = ?, model = ?, year = ?, 
            plate_number = ?, vin = ?, color = ?, is_active = ?, 
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (
        data.get('customer_id'),
        data['make'],
        data['model'],
        data.get('year'),
        data.get('plate_number', ''),
        data.get('vin', ''),
        data.get('color', ''),
        data.get('is_active', 1),
        vehicle_id
    ))
    conn.commit()
    conn.close()
    print(f"[DB] Updated vehicle #{vehicle_id}")
    return get_vehicle_by_id(vehicle_id)

def delete_vehicle(vehicle_id):
    """Soft delete vehicle by setting is_active to 0"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE vehicles SET is_active = 0 WHERE id = ?', (vehicle_id,))
    conn.commit()
    conn.close()
    print(f"[DB] Deleted vehicle #{vehicle_id}")
    return True

def search_vehicles(search_term):
    """Search vehicles by make, model, plate number, or VIN"""
    conn = get_connection()
    cursor = conn.cursor()
    search_pattern = f'%{search_term}%'
    cursor.execute('''
        SELECT * FROM vehicles 
        WHERE is_active = 1 
        AND (make LIKE ? OR model LIKE ? OR plate_number LIKE ? OR vin LIKE ?)
        ORDER BY created_at DESC
    ''', (search_pattern, search_pattern, search_pattern, search_pattern))
    vehicles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return vehicles

def init_default_vehicles():
    """Initialize some default vehicles for testing"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM vehicles')
    count = cursor.fetchone()['count']
    conn.close()
    
    if count == 0:
        default_vehicles = [
            {'make': 'Toyota', 'model': 'Camry 2020', 'year': 2020, 'plate_number': 'DXB-12345', 'color': 'White'},
            {'make': 'Honda', 'model': 'Accord 2019', 'year': 2019, 'plate_number': 'DXB-67890', 'color': 'Black'},
            {'make': 'Nissan', 'model': 'Altima 2021', 'year': 2021, 'plate_number': 'DXB-54321', 'color': 'Silver'},
            {'make': 'BMW', 'model': '320i 2022', 'year': 2022, 'plate_number': 'DXB-99999', 'color': 'Blue'},
            {'make': 'Mercedes', 'model': 'C-Class 2021', 'year': 2021, 'plate_number': 'DXB-88888', 'color': 'Gray'},
        ]
        
        for vehicle in default_vehicles:
            create_vehicle(vehicle)
        
        print("[DB] Default vehicles initialized")

# Initialize database on import
init_database()
create_default_users()
init_default_settings()
init_default_services()
init_default_vehicles()
