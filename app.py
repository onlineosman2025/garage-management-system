#!/usr/bin/env python3
# Fixed for Railway deployment - 2025-11-03-10-33
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import json
import secrets
from pathlib import Path
from datetime import datetime
import database as db
import email_service
import pdf_generator
import reports
import permissions
import file_manager
import uae_vat_system
from pathlib import Path

DB_FILE = Path(__file__).parent / 'garage.db'

app = Flask(__name__, static_folder='.', static_url_path='')

# Enable CORS for all routes - this fixes everything!
CORS(app, 
    origins=['https://cute-crisp-ba7114.netlify.app', 'http://localhost:3000', '*'],
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers=['Content-Type', 'Authorization'],
    supports_credentials=True
)

PORT = int(os.environ.get('PORT', 3000))
HOST = '0.0.0.0'

# Initialize database and create default admin user
db.init_database()
db.create_default_users()

# Debug info
print("=" * 50)
print("GARAGE MANAGEMENT SYSTEM - FLASK VERSION!")
print("=" * 50)
print(f"Working directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')[:10]}")
print(f"Starting Flask server on http://{HOST}:{PORT}")
print("=" * 50)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/health')
def health():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'message': 'GMS Backend is running!',
        'timestamp': datetime.now().isoformat(),
        'cors_enabled': True
    })

@app.route('/api/test')
def test():
    """Simple test endpoint to check if Flask is working"""
    return jsonify({
        'status': 'Flask is working!',
        'time': datetime.now().isoformat(),
        'database_file': str(DB_FILE),
        'database_exists': DB_FILE.exists()
    })

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/api/dashboard/stats', methods=['GET'])
def dashboard_stats():
    return jsonify(db.get_dashboard_stats())

@app.route('/api/customers', methods=['GET'])
def get_customers():
    if '/api/customers/' in request.path and '?' not in request.path:
        customer_id = int(request.path.split('/')[-1])
        customer = db.get_customer_by_id(customer_id)
        if customer:
            return jsonify(customer)
        else:
            return jsonify({'error': 'Customer not found'}), 404
    else:
        customers = db.get_all_customers()
        return jsonify(customers)

@app.route('/api/customers', methods=['POST'])
def create_customer():
    try:
        customer = db.create_customer(request.get_json())
        return jsonify(customer)
    except Exception as e:
        return jsonify({'error': f"Failed to create customer: {str(e)}"}), 500

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        customer = db.update_customer(customer_id, request.get_json())
        if customer:
            return jsonify(customer)
        else:
            return jsonify({'error': 'Customer not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    db.delete_customer(customer_id)
    return jsonify({'success': True, 'message': 'Customer deleted'})

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    limit = request.args.get('limit', type=int)
    jobs = db.get_all_jobs(limit=limit)
    return jsonify(jobs)

@app.route('/api/jobs', methods=['POST'])
def create_job():
    try:
        job = db.create_job(request.get_json())
        return jsonify(job)
    except Exception as e:
        return jsonify({'error': f"Failed to create job: {str(e)}"}), 500

@app.route('/api/jobs/<int:job_id>/status', methods=['PUT'])
def update_job_status(job_id):
    try:
        status = request.get_json().get('status')
        job = db.update_job_status(job_id, status)
        if job:
            return jsonify(job)
        else:
            return jsonify({'error': 'Job not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/invoices', methods=['GET'])
def get_invoices():
    customer_id = request.args.get('customer_id', type=int)
    invoices = db.get_all_invoices(customer_id=customer_id)
    return jsonify(invoices)

@app.route('/api/invoices', methods=['POST'])
def create_invoice():
    try:
        invoice = db.create_invoice(request.get_json())
        return jsonify(invoice)
    except Exception as e:
        return jsonify({'error': f"Failed to create invoice: {str(e)}"}), 500

@app.route('/api/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    invoice = db.get_invoice_by_id(invoice_id)
    if invoice:
        return jsonify(invoice)
    else:
        return jsonify({'error': 'Invoice not found'}), 404

@app.route('/api/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    try:
        invoice = db.update_invoice(invoice_id, request.get_json())
        if invoice:
            return jsonify(invoice)
        else:
            return jsonify({'error': 'Invoice not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    db.delete_invoice(invoice_id)
    return jsonify({'success': True, 'message': 'Invoice deleted'})

@app.route('/api/invoices/<int:invoice_id>/pay', methods=['PUT'])
def pay_invoice(invoice_id):
    try:
        invoice = db.mark_invoice_paid(invoice_id)
        if invoice:
            return jsonify(invoice)
        else:
            return jsonify({'error': 'Invoice not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    users = db.get_all_users()
    # Remove password hashes
    for user in users:
        if 'password_hash' in user:
            del user['password_hash']
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        user = db.create_user(request.get_json())
        if 'password_hash' in user:
            del user['password_hash']
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': f"Failed to create user: {str(e)}"}), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = db.update_user(user_id, request.get_json())
        if user:
            if 'password_hash' in user:
                del user['password_hash']
            return jsonify(user)
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db.delete_user(user_id)
    return jsonify({'success': True, 'message': 'User deleted'})

@app.route('/api/services', methods=['GET'])
def get_services():
    services = db.get_all_services()
    return jsonify(services)

@app.route('/api/services', methods=['POST'])
def create_service():
    try:
        service = db.create_service(request.get_json())
        return jsonify(service)
    except Exception as e:
        return jsonify({'error': f"Failed to create service: {str(e)}"}), 500

@app.route('/api/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    try:
        service = db.update_service(service_id, request.get_json())
        if service:
            return jsonify(service)
        else:
            return jsonify({'error': 'Service not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    db.delete_service(service_id)
    return jsonify({'success': True, 'message': 'Service deleted'})

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = db.get_all_vehicles()
    return jsonify(vehicles)

@app.route('/api/vehicles', methods=['POST'])
def create_vehicle():
    try:
        vehicle = db.create_vehicle(request.get_json())
        return jsonify(vehicle)
    except Exception as e:
        return jsonify({'error': f"Failed to create vehicle: {str(e)}"}), 500

@app.route('/api/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    try:
        vehicle = db.update_vehicle(vehicle_id, request.get_json())
        if vehicle:
            return jsonify(vehicle)
        else:
            return jsonify({'error': 'Vehicle not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    db.delete_vehicle(vehicle_id)
    return jsonify({'success': True, 'message': 'Vehicle deleted'})

@app.route('/api/garage-info', methods=['GET'])
def garage_info():
    return jsonify(db.get_garage_info())

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        print(f"[LOGIN] Login request received")
        data = request.get_json()
        print(f"[LOGIN] Request data: {data}")
        
        email = data.get('email') or data.get('username')  # Handle both email and username
        password = data.get('password')
        
        print(f"[LOGIN DEBUG] Email: {email}, Password: {password}")
        
        if not email or not password:
            print(f"[LOGIN ERROR] Missing email or password")
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = db.authenticate_user(email, password)
        print(f"[LOGIN DEBUG] User authenticated: {user}")
        if user:
            if 'password_hash' in user:
                del user['password_hash']
            return jsonify({
                'success': True,
                'user': user,
                'message': 'Login successful'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            })
    except Exception as e:
        return jsonify({'error': f"Login error: {str(e)}"}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        full_name = data.get('full_name')
        role = data.get('role', 'technician')
        
        if not username or not password or not email or not full_name:
            return jsonify({'error': 'Username, password, email, and full_name are required'}), 400
        
        # Check if user already exists
        existing_user = db.get_user_by_username(username)
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            })
        
        # Create new user
        user = db.create_user({
            'username': username,
            'password': password,
            'email': email,
            'full_name': full_name,
            'role': role
        })
        
        if user:
            if 'password_hash' in user:
                del user['password_hash']
            return jsonify({
                'success': True,
                'user': user,
                'message': 'User registered successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to register user'
            })
    except Exception as e:
        return jsonify({'error': f"Registration error: {str(e)}"}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    })

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return jsonify({
            'success': True,
            'authenticated': True,
            'message': 'Authentication valid'
        })
    else:
        return jsonify({
            'success': False,
            'authenticated': False,
            'message': 'Not authenticated'
        })

@app.route('/api/debug/users', methods=['GET'])
def debug_users():
    """Debug endpoint to check users in database"""
    users = db.get_all_users()
    print(f"[DEBUG] Users in database: {users}")
    return jsonify({
        'count': len(users),
        'users': users
    })

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get application settings"""
    return jsonify(db.get_all_settings())

@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update application settings"""
    try:
        data = request.get_json()
        for key, value in data.items():
            db.update_setting(key, value)
        return jsonify({'success': True, 'message': 'Settings updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dashboard routes
@app.route('/api/dashboard/revenue', methods=['GET'])
def dashboard_revenue():
    return jsonify({
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'values': [800, 950, 1100, 1050, 1200, 1150, 1300, 1250, 1400, 1050, 0, 0]
    })

@app.route('/api/reports/revenue', methods=['GET'])
def reports_revenue():
    return jsonify({
        'total_revenue': 1050.00,
        'total_vat': 50.00,
        'invoice_count': 0,
        'chart_data': [
            {'month': 'Oct', 'revenue': 1050.00}
        ]
    })

@app.route('/api/reports/customers', methods=['GET'])
def reports_customers():
    customers = db.get_all_customers()
    return jsonify({
        'total_customers': len(customers),
        'active_customers': len(customers),
        'chart_data': customers[:5]
    })

@app.route('/api/dashboard/activities', methods=['GET'])
def dashboard_activities():
    return jsonify([
        {'type': 'customer_added', 'description': 'New customer added', 'created_at': datetime.now().isoformat()},
        {'type': 'job_created', 'description': 'New job created', 'created_at': datetime.now().isoformat()},
    ])

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=False)
