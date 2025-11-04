#!/usr/bin/env python3
"""Check available login accounts in the database"""
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / 'garage.db'

def check_users():
    """Display all users in the database"""
    if not DB_FILE.exists():
        print(f"Database not found at: {DB_FILE}")
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT id, email, name, role, is_active, created_at, last_login 
            FROM users
        ''')
        users = cursor.fetchall()
        
        if not users:
            print("No users found in the database")
            print("\nTo create a default admin user, run:")
            print("  python -c \"from database import init_database, create_default_users; init_database(); create_default_users()\"")
        else:
            print(f"\nFound {len(users)} login account(s) in the database:\n")
            print(f"{'ID':<5} {'Email':<30} {'Name':<25} {'Role':<15} {'Active':<10} {'Last Login':<20}")
            print("-" * 115)
            
            for user in users:
                user_id, email, name, role, is_active, created_at, last_login = user
                active_status = "Yes" if is_active else "No"
                last_login_str = last_login if last_login else "Never"
                
                print(f"{user_id:<5} {email:<30} {name:<25} {role:<15} {active_status:<10} {last_login_str:<20}")
            
            print("\n" + "="*115)
            print("\nLogin Credentials:")
            for user in users:
                if user[4]:  # is_active
                    print(f"   - Email: {user[1]}")
                    print(f"     Role: {user[3]}")
                    print()
    
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        print("The users table may not exist. Initialize the database first.")
    finally:
        conn.close()

if __name__ == '__main__':
    check_users()
