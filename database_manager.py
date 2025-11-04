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
    
    def get_garage_users(self, garage_id):
        """
        Get all users from a specific garage database
        """
        db_path = os.path.join(self.base_path, f'garage_{garage_id}.db')
        
        if not os.path.exists(db_path):
            return []
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, email, role, phone, is_active, created_at, last_login
                FROM users
                ORDER BY created_at DESC
            ''')
            
            users = []
            for row in cursor.fetchall():
                users.append({
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'role': row[3],
                    'phone': row[4],
                    'is_active': row[5],
                    'created_at': row[6],
                    'last_login': row[7]
                })
            
            conn.close()
            return users
        except Exception as e:
            print(f"Error getting users for garage {garage_id}: {e}")
            return []
    
    def update_user_password(self, garage_id, user_id, new_password):
        """Update user password in garage database"""
        db_path = os.path.join(self.base_path, f'garage_{garage_id}.db')
        
        if not os.path.exists(db_path):
            return False
        
        try:
            import hashlib
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users 
                SET password_hash = ?
                WHERE id = ?
            ''', (password_hash, user_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
    
    def suspend_garage(self, garage_id, reason):
        """Suspend a garage"""
        db_path = os.path.join(self.base_path, f'garage_{garage_id}.db')
        
        if not os.path.exists(db_path):
            return False
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if columns exist, if not add them
            cursor.execute("PRAGMA table_info(garage_info)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'suspension_reason' not in columns:
                cursor.execute('ALTER TABLE garage_info ADD COLUMN suspension_reason TEXT')
            if 'suspended_at' not in columns:
                cursor.execute('ALTER TABLE garage_info ADD COLUMN suspended_at TEXT')
            
            cursor.execute('''
                UPDATE garage_info 
                SET is_active = 0, suspension_reason = ?, suspended_at = ?
                WHERE garage_id = ?
            ''', (reason, datetime.now().isoformat(), garage_id))
            
            conn.commit()
            conn.close()
            print(f"✅ Garage {garage_id} suspended. Reason: {reason}")
            return True
        except Exception as e:
            print(f"Error suspending garage: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def activate_garage(self, garage_id):
        """Activate a garage"""
        db_path = os.path.join(self.base_path, f'garage_{garage_id}.db')
        
        if not os.path.exists(db_path):
            return False
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE garage_info 
                SET is_active = 1, suspension_reason = NULL, suspended_at = NULL
                WHERE garage_id = ?
            ''', (garage_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error activating garage: {e}")
            return False
    
    def extend_trial(self, garage_id, days):
        """Extend trial period for a garage"""
        db_path = os.path.join(self.base_path, f'garage_{garage_id}.db')
        
        if not os.path.exists(db_path):
            print(f"Error: Database not found for garage {garage_id}")
            return False
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if trial_end_date column exists, if not add it
            cursor.execute("PRAGMA table_info(garage_info)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'trial_end_date' not in columns:
                # Add trial_end_date column
                cursor.execute('ALTER TABLE garage_info ADD COLUMN trial_end_date TEXT')
                # Set default trial end date (14 days from now)
                default_end = (datetime.now() + timedelta(days=14)).isoformat()
                cursor.execute('UPDATE garage_info SET trial_end_date = ?', (default_end,))
                conn.commit()
            
            # Get current trial end date
            cursor.execute('SELECT trial_end_date FROM garage_info WHERE garage_id = ?', (garage_id,))
            result = cursor.fetchone()
            
            if result and result[0]:
                try:
                    current_end = datetime.fromisoformat(result[0])
                except:
                    # If date is invalid, use current date
                    current_end = datetime.now()
            else:
                # If no trial end date, use current date
                current_end = datetime.now()
            
            new_end = current_end + timedelta(days=days)
            
            cursor.execute('''
                UPDATE garage_info 
                SET trial_end_date = ?
                WHERE garage_id = ?
            ''', (new_end.isoformat(), garage_id))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Trial extended for {garage_id}: {days} days added. New end: {new_end.isoformat()}")
            return True
        except Exception as e:
            print(f"Error extending trial for {garage_id}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def update_garage_info(self, garage_id, data):
        """Update garage information"""
        db_path = os.path.join(self.base_path, f'garage_{garage_id}.db')
        
        if not os.path.exists(db_path):
            return False
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Build update query dynamically
            updates = []
            values = []
            
            if 'garage_name' in data:
                updates.append('garage_name = ?')
                values.append(data['garage_name'])
            if 'owner_name' in data:
                updates.append('owner_name = ?')
                values.append(data['owner_name'])
            if 'email' in data:
                updates.append('email = ?')
                values.append(data['email'])
            if 'phone' in data:
                updates.append('phone = ?')
                values.append(data['phone'])
            
            if updates:
                values.append(garage_id)
                query = f"UPDATE garage_info SET {', '.join(updates)} WHERE garage_id = ?"
                cursor.execute(query, values)
                conn.commit()
            
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating garage info: {e}")
            return False
    
    def update_user_info(self, garage_id, user_id, data):
        """Update user information in garage database"""
        db_path = os.path.join(self.base_path, f'garage_{garage_id}.db')
        
        if not os.path.exists(db_path):
            return False
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Build update query dynamically
            updates = []
            values = []
            
            if 'name' in data:
                updates.append('name = ?')
                values.append(data['name'])
            if 'email' in data:
                updates.append('email = ?')
                values.append(data['email'])
            if 'role' in data:
                updates.append('role = ?')
                values.append(data['role'])
            if 'phone' in data:
                updates.append('phone = ?')
                values.append(data['phone'])
            
            if updates:
                values.append(user_id)
                query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, values)
                conn.commit()
            
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user info: {e}")
            return False
    
    def create_user_in_garage(self, garage_id, user_data):
        """Create a new user in a specific garage database"""
        db_path = os.path.join(self.base_path, f'garage_{garage_id}.db')
        
        if not os.path.exists(db_path):
            return False
        
        try:
            import hashlib
            password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (name, email, password_hash, role, phone, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, 1, ?)
            ''', (
                user_data['name'],
                user_data['email'],
                password_hash,
                user_data['role'],
                user_data.get('phone', ''),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def save_payment(self, payment_data):
        """Save payment record"""
        garage_id = payment_data['garage_id']
        db_path = self.get_database_path(garage_id)
        
        print(f"💾 Saving payment for garage_id: {garage_id}")
        print(f"💾 Database path: {db_path}")
        print(f"💾 Database exists: {os.path.exists(db_path)}")
        
        if not os.path.exists(db_path):
            print(f"❌ Database not found for garage: {garage_id}")
            print(f"❌ Expected path: {db_path}")
            # List available databases
            if os.path.exists(self.base_path):
                available = os.listdir(self.base_path)
                print(f"📁 Available databases: {available}")
            return False
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if payments table exists, if not create it
            cursor.execute("PRAGMA table_info(payments)")
            if not cursor.fetchall():
                cursor.execute('''
                    CREATE TABLE payments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        payment_method TEXT NOT NULL,
                        payment_id TEXT,
                        reference_number TEXT,
                        plan TEXT NOT NULL,
                        amount REAL NOT NULL,
                        total REAL NOT NULL,
                        status TEXT NOT NULL,
                        receipt_filename TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        verified_at TIMESTAMP
                    )
                ''')
            
            # Insert payment record
            cursor.execute('''
                INSERT INTO payments (
                    payment_method, payment_id, reference_number, plan, 
                    amount, total, status, receipt_filename
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                payment_data['payment_method'],
                payment_data.get('payment_id'),
                payment_data.get('reference_number'),
                payment_data['plan'],
                payment_data['amount'],
                payment_data['total'],
                payment_data['status'],
                payment_data.get('receipt_filename')
            ))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Payment saved: {garage_id} - {payment_data['plan']}")
            return True
            
        except Exception as e:
            print(f"Error saving payment: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def upgrade_account(self, garage_id, plan):
        """Upgrade account from trial to paid"""
        db_path = self.get_database_path(garage_id)
        
        if not os.path.exists(db_path):
            print(f"Database not found for garage: {garage_id}")
            return False
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Update trial_info table
            cursor.execute('''
                UPDATE trial_info 
                SET is_active = 0,
                    upgraded_at = ?,
                    subscription_plan = ?
                WHERE garage_id = ?
            ''', (datetime.now().isoformat(), plan, garage_id))
            
            # Check if subscription table exists, if not create it
            cursor.execute("PRAGMA table_info(subscription)")
            if not cursor.fetchall():
                cursor.execute('''
                    CREATE TABLE subscription (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        plan TEXT NOT NULL,
                        status TEXT DEFAULT 'active',
                        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP,
                        auto_renew BOOLEAN DEFAULT 1
                    )
                ''')
            
            # Insert subscription record
            cursor.execute('''
                INSERT INTO subscription (plan, status)
                VALUES (?, 'active')
            ''', (plan,))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Account upgraded: {garage_id} to {plan}")
            return True
            
        except Exception as e:
            print(f"Error upgrading account: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_payment_by_reference(self, reference_number):
        """Get payment details by reference number"""
        # Search all garage databases for the payment
        for garage_id in self._get_all_garage_ids():
            db_path = self.get_database_path(garage_id)
            
            if not os.path.exists(db_path):
                continue
            
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM payments 
                    WHERE reference_number = ?
                ''', (reference_number,))
                
                row = cursor.fetchone()
                conn.close()
                
                if row:
                    return {
                        'id': row[0],
                        'garage_id': garage_id,
                        'payment_method': row[1],
                        'payment_id': row[2],
                        'reference_number': row[3],
                        'plan': row[4],
                        'amount': row[5],
                        'total': row[6],
                        'status': row[7],
                        'receipt_filename': row[8],
                        'created_at': row[9],
                        'verified_at': row[10] if len(row) > 10 else None
                    }
            except:
                pass
        
        return None
    
    def update_payment_status(self, reference_number, status):
        """Update payment status"""
        # Search all garage databases for the payment
        for garage_id in self._get_all_garage_ids():
            db_path = self.get_database_path(garage_id)
            
            if not os.path.exists(db_path):
                continue
            
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE payments 
                    SET status = ?,
                        verified_at = ?
                    WHERE reference_number = ?
                ''', (status, datetime.now().isoformat(), reference_number))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    conn.close()
                    print(f"✅ Payment status updated: {reference_number} -> {status}")
                    return True
                
                conn.close()
            except:
                pass
        
        return False
    
    def get_all_pending_payments(self):
        """Get all pending cash payments across all garages"""
        pending_payments = []
        
        for garage_id in self._get_all_garage_ids():
            db_path = self.get_database_path(garage_id)
            
            if not os.path.exists(db_path):
                continue
            
            try:
                conn = sqlite3.connect(db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Check if payments table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='payments'")
                if not cursor.fetchone():
                    conn.close()
                    continue
                
                # Get garage info
                cursor.execute('SELECT garage_name, owner_name, email, phone FROM garage_info WHERE garage_id = ?', (garage_id,))
                garage_info = cursor.fetchone()
                
                # Get pending payments
                cursor.execute('''
                    SELECT * FROM payments 
                    WHERE status = 'pending' 
                    ORDER BY created_at DESC
                ''')
                
                payments = cursor.fetchall()
                
                for payment in payments:
                    pending_payments.append({
                        'garage_id': garage_id,
                        'garage_name': garage_info['garage_name'] if garage_info else 'Unknown',
                        'owner_name': garage_info['owner_name'] if garage_info else 'Unknown',
                        'email': garage_info['email'] if garage_info else 'Unknown',
                        'phone': garage_info['phone'] if garage_info else 'Unknown',
                        'payment_id': payment['id'],
                        'reference_number': payment['reference_number'],
                        'plan': payment['plan'],
                        'amount': payment['amount'],
                        'total': payment['total'],
                        'receipt_filename': payment['receipt_filename'],
                        'created_at': payment['created_at'],
                        'status': payment['status']
                    })
                
                conn.close()
            except Exception as e:
                print(f"Error getting pending payments for {garage_id}: {e}")
                continue
        
        return pending_payments
    
    def _get_all_garage_ids(self):
        """Get list of all garage IDs"""
        garage_ids = []
        for filename in os.listdir(self.base_path):
            if filename.startswith('garage_') and filename.endswith('.db'):
                garage_id = filename.replace('garage_', '').replace('.db', '')
                garage_ids.append(garage_id)
        return garage_ids


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
