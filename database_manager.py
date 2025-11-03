"""
Multi-Tenant Database Manager for Garage Management System
Each garage owner gets their own separate SQLite database
All databases are stored in the 'databases' folder
"""

import os
import sqlite3
import hashlib
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, base_path='databases'):
        self.base_path = base_path
        # Create databases folder if it doesn't exist
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
            print(f"Created databases folder: {self.base_path}")
    
    def get_database_name(self, garage_id):
        """Generate database filename for a garage"""
        return f"garage_{garage_id}.db"
    
    def get_database_path(self, garage_id):
        """Get full path to garage database"""
        db_name = self.get_database_name(garage_id)
        return os.path.join(self.base_path, db_name)
    
    def create_garage_database(self, garage_data):
        """
        Create a new database for a garage owner
        Returns: garage_id and database path
        """
        # Generate unique garage ID
        garage_id = self.generate_garage_id(garage_data['email'])
        db_path = self.get_database_path(garage_id)
        
        print(f"Creating database for garage: {garage_data['garage_name']}")
        print(f"Database path: {db_path}")
        
        # Create database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create all necessary tables
        self._create_tables(cursor)
        
        # Insert garage owner information
        self._insert_garage_info(cursor, garage_id, garage_data)
        
        # Insert trial information
        self._insert_trial_info(cursor, garage_id, garage_data.get('trial_days', 14))
        
        # Commit and close
        conn.commit()
        conn.close()
        
        print(f"✅ Database created successfully: {db_path}")
        
        return {
            'garage_id': garage_id,
            'database_path': db_path,
            'database_name': self.get_database_name(garage_id)
        }
    
    def generate_garage_id(self, email):
        """Generate unique garage ID from email"""
        # Use hash of email + timestamp for uniqueness
        unique_string = f"{email}_{datetime.now().isoformat()}"
        hash_object = hashlib.md5(unique_string.encode())
        return hash_object.hexdigest()[:12]
    
    def _create_tables(self, cursor):
        """Create all necessary tables for a garage database"""
        
        # Garage Information Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS garage_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                garage_id TEXT UNIQUE NOT NULL,
                garage_name TEXT NOT NULL,
                owner_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                address TEXT,
                currency TEXT DEFAULT 'AED',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Trial Information Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trial_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                garage_id TEXT UNIQUE NOT NULL,
                trial_start_date TIMESTAMP NOT NULL,
                trial_end_date TIMESTAMP NOT NULL,
                trial_days INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                upgraded_at TIMESTAMP,
                subscription_plan TEXT
            )
        ''')
        
        # Customers Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT NOT NULL,
                address TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Vehicles Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER,
                license_plate TEXT UNIQUE NOT NULL,
                vin TEXT,
                color TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Services Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_ar TEXT,
                name_ur TEXT,
                description TEXT,
                default_price REAL NOT NULL,
                duration INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Jobs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                vehicle_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                total_amount REAL DEFAULT 0,
                paid_amount REAL DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
            )
        ''')
        
        # Job Services Table (many-to-many)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                price REAL NOT NULL,
                FOREIGN KEY (job_id) REFERENCES jobs(id),
                FOREIGN KEY (service_id) REFERENCES services(id)
            )
        ''')
        
        # Invoices Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                invoice_number TEXT UNIQUE NOT NULL,
                total_amount REAL NOT NULL,
                tax_amount REAL DEFAULT 0,
                discount_amount REAL DEFAULT 0,
                final_amount REAL NOT NULL,
                status TEXT DEFAULT 'unpaid',
                issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                paid_at TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        ''')
        
        # Settings Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL,
                setting_value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("✅ All tables created successfully")
    
    def _insert_garage_info(self, cursor, garage_id, garage_data):
        """Insert garage owner information"""
        cursor.execute('''
            INSERT INTO garage_info (
                garage_id, garage_name, owner_name, email, phone, currency
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            garage_id,
            garage_data['garage_name'],
            garage_data['owner_name'],
            garage_data['email'],
            garage_data.get('phone', ''),
            garage_data.get('currency', 'AED')
        ))
        
        # Insert owner as first user
        password_hash = self._hash_password(garage_data['password'])
        cursor.execute('''
            INSERT INTO users (email, password_hash, name, role)
            VALUES (?, ?, ?, ?)
        ''', (
            garage_data['email'],
            password_hash,
            garage_data['owner_name'],
            'owner'
        ))
        
        print(f"✅ Garage info inserted for: {garage_data['garage_name']}")
    
    def _insert_trial_info(self, cursor, garage_id, trial_days):
        """Insert trial information"""
        trial_start = datetime.now()
        trial_end = trial_start + timedelta(days=trial_days)
        
        cursor.execute('''
            INSERT INTO trial_info (
                garage_id, trial_start_date, trial_end_date, trial_days
            ) VALUES (?, ?, ?, ?)
        ''', (
            garage_id,
            trial_start.isoformat(),
            trial_end.isoformat(),
            trial_days
        ))
        
        print(f"✅ Trial info inserted: {trial_days} days")
    
    def _hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def get_garage_connection(self, garage_id):
        """Get database connection for a specific garage"""
        db_path = self.get_database_path(garage_id)
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database not found for garage: {garage_id}")
        return sqlite3.connect(db_path)
    
    def verify_login(self, email, password):
        """
        Verify login credentials and return garage_id
        Searches through all databases to find the user
        """
        password_hash = self._hash_password(password)
        
        # List all database files
        if not os.path.exists(self.base_path):
            return None
        
        for filename in os.listdir(self.base_path):
            if filename.startswith('garage_') and filename.endswith('.db'):
                db_path = os.path.join(self.base_path, filename)
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Check if user exists with correct password
                    cursor.execute('''
                        SELECT u.id, u.name, u.role, g.garage_id, g.garage_name
                        FROM users u
                        JOIN garage_info g ON 1=1
                        WHERE u.email = ? AND u.password_hash = ? AND u.is_active = 1
                    ''', (email, password_hash))
                    
                    result = cursor.fetchone()
                    conn.close()
                    
                    if result:
                        return {
                            'user_id': result[0],
                            'name': result[1],
                            'role': result[2],
                            'garage_id': result[3],
                            'garage_name': result[4],
                            'email': email
                        }
                except Exception as e:
                    print(f"Error checking database {filename}: {e}")
                    continue
        
        return None
    
    def get_trial_status(self, garage_id):
        """Get trial status for a garage"""
        try:
            conn = self.get_garage_connection(garage_id)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT trial_start_date, trial_end_date, trial_days, is_active
                FROM trial_info
                WHERE garage_id = ?
            ''', (garage_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                trial_end = datetime.fromisoformat(result[1])
                days_remaining = (trial_end - datetime.now()).days
                
                return {
                    'trial_start_date': result[0],
                    'trial_end_date': result[1],
                    'trial_days': result[2],
                    'is_active': result[3],
                    'days_remaining': max(0, days_remaining),
                    'is_expired': days_remaining <= 0
                }
            
            return None
        except Exception as e:
            print(f"Error getting trial status: {e}")
            return None
    
    def list_all_garages(self):
        """List all registered garages (for admin purposes)"""
        garages = []
        
        if not os.path.exists(self.base_path):
            return garages
        
        for filename in os.listdir(self.base_path):
            if filename.startswith('garage_') and filename.endswith('.db'):
                db_path = os.path.join(self.base_path, filename)
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        SELECT garage_id, garage_name, owner_name, email, created_at
                        FROM garage_info
                    ''')
                    
                    result = cursor.fetchone()
                    if result:
                        garages.append({
                            'garage_id': result[0],
                            'garage_name': result[1],
                            'owner_name': result[2],
                            'email': result[3],
                            'created_at': result[4],
                            'database_file': filename
                        })
                    
                    conn.close()
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        
        return garages


# Example usage
if __name__ == '__main__':
    # Initialize database manager
    db_manager = DatabaseManager()
    
    # Example: Create a new garage database
    test_garage = {
        'garage_name': 'Test Garage',
        'owner_name': 'John Doe',
        'email': 'john@testgarage.com',
        'phone': '+971501234567',
        'password': 'secure123',
        'trial_days': 14
    }
    
    result = db_manager.create_garage_database(test_garage)
    print(f"\nGarage created:")
    print(f"  Garage ID: {result['garage_id']}")
    print(f"  Database: {result['database_name']}")
    print(f"  Path: {result['database_path']}")
    
    # List all garages
    print("\nAll registered garages:")
    for garage in db_manager.list_all_garages():
        print(f"  - {garage['garage_name']} ({garage['email']})")
