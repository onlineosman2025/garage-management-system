#!/usr/bin/env python3
"""
Minimal Railway backend test - isolates the deployment issue
Updated: 2025-11-03-13-12-FORCE-DEPLOY
Multi-Tenant Database Support Added
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from database_manager import DatabaseManager

# Initialize database manager
db_manager = DatabaseManager()

app = Flask(__name__)

# Maximum permissive CORS for testing
CORS(app, 
    origins="*",
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True
)

@app.route('/')
def home():
    return jsonify({
        'status': 'Railway test backend is running!',
        'message': 'This is a minimal test to isolate deployment issues'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Test backend working!',
        'cors_enabled': True
    })

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    try:
        if request.method == 'OPTIONS':
            return '', 200
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        print(f"🔐 Login attempt: {email}")
        
        # Verify login credentials across all garage databases
        user_info = db_manager.verify_login(email, password)
        
        if user_info:
            # Get trial status for this garage
            trial_status = db_manager.get_trial_status(user_info['garage_id'])
            
            print(f"✅ Login successful: {user_info['name']} ({user_info['garage_name']})")
            print(f"📁 Database: garage_{user_info['garage_id']}.db")
            
            return jsonify({
                'success': True,
                'access_token': f"token_{user_info['garage_id']}_{user_info['user_id']}",
                'user': {
                    'id': user_info['user_id'],
                    'email': user_info['email'],
                    'name': user_info['name'],
                    'role': user_info['role']
                },
                'garage': {
                    'id': user_info['garage_id'],
                    'name': user_info['garage_name'],
                    'currency': 'AED'
                },
                'trial': trial_status
            })
        else:
            print(f"❌ Login failed: Invalid credentials for {email}")
            return jsonify({'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/stats', methods=['GET', 'OPTIONS'])
def dashboard_stats():
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        print("Dashboard stats requested")
        
        # Return mock dashboard data
        return jsonify({
            'total_revenue': 150000,
            'total_jobs': 245,
            'total_customers': 89,
            'active_vehicles': 12,
            'pending_jobs': 8,
            'completed_jobs': 237,
            'monthly_revenue': 25000
        })
    except Exception as e:
        print(f"Dashboard stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs', methods=['GET', 'OPTIONS'])
def get_jobs():
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        print("Jobs requested")
        
        # Return mock jobs data
        return jsonify([
            {
                'id': 1,
                'customer_name': 'John Doe',
                'vehicle_make': 'Toyota',
                'vehicle_model': 'Camry',
                'status': 'pending',
                'created_date': '2025-11-01'
            },
            {
                'id': 2,
                'customer_name': 'Jane Smith',
                'vehicle_make': 'Honda',
                'vehicle_model': 'Civic',
                'status': 'in_progress',
                'created_date': '2025-11-02'
            }
        ])
    except Exception as e:
        print(f"Jobs error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers', methods=['GET', 'OPTIONS'])
def get_customers():
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        print("Customers requested")
        
        # Return mock customers data
        return jsonify([
            {
                'id': 1,
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '+971501234567'
            },
            {
                'id': 2,
                'name': 'Jane Smith',
                'email': 'jane@example.com',
                'phone': '+971507654321'
            }
        ])
    except Exception as e:
        print(f"Customers error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/vehicles', methods=['GET', 'OPTIONS'])
def get_vehicles():
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        print("Vehicles requested")
        
        # Return mock vehicles data
        return jsonify([
            {
                'id': 1,
                'make': 'Toyota',
                'model': 'Camry',
                'year': 2020,
                'license_plate': 'ABC123'
            },
            {
                'id': 2,
                'make': 'Honda',
                'model': 'Civic',
                'year': 2021,
                'license_plate': 'XYZ789'
            }
        ])
    except Exception as e:
        print(f"Vehicles error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/services', methods=['GET', 'OPTIONS'])
def get_services():
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        print("Services requested")
        
        # Return mock services data
        return jsonify([
            {
                'id': 1,
                'name': 'Oil Change',
                'price': 150,
                'duration': 30
            },
            {
                'id': 2,
                'name': 'Brake Inspection',
                'price': 200,
                'duration': 45
            }
        ])
    except Exception as e:
        print(f"Services error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['GET', 'OPTIONS'])
def get_settings():
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        print("Settings requested")
        
        # Return mock settings data
        return jsonify({
            'garage_name': 'Test Garage',
            'currency': 'AED',
            'email': 'owner@garage.com',
            'phone': '+97123456789',
            'address': 'Dubai, UAE',
            'tax_rate': 5.0,
            'invoice_prefix': 'INV',
            'low_stock_threshold': 10
        })
    except Exception as e:
        print(f"Settings error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/revenue', methods=['GET', 'OPTIONS'])
def get_revenue():
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        print("Revenue data requested")
        
        # Return mock revenue data
        return jsonify({
            'monthly_data': [
                {'month': 'Jan', 'revenue': 12000},
                {'month': 'Feb', 'revenue': 15000},
                {'month': 'Mar', 'revenue': 18000},
                {'month': 'Apr', 'revenue': 22000},
                {'month': 'May', 'revenue': 25000},
                {'month': 'Jun', 'revenue': 28000}
            ],
            'total_revenue': 120000,
            'growth_rate': 15.5
        })
    except Exception as e:
        print(f"Revenue error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/activities', methods=['GET', 'OPTIONS'])
def get_activities():
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        print("Activities data requested")
        
        # Return mock activities data
        return jsonify([
            {
                'id': 1,
                'type': 'job_created',
                'description': 'New job created for John Doe',
                'timestamp': '2025-11-03T10:30:00Z'
            },
            {
                'id': 2,
                'type': 'payment_received',
                'description': 'Payment received: AED 500',
                'timestamp': '2025-11-03T09:15:00Z'
            }
        ])
    except Exception as e:
        print(f"Activities error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/config', methods=['GET', 'OPTIONS'])
def get_email_config():
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        print("Email config requested")
        
        # Return mock email config
        return jsonify({
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_user': 'your-email@gmail.com',
            'smtp_password': 'your-app-password',
            'from_email': 'your-email@gmail.com',
            'from_name': 'Test Garage'
        })
    except Exception as e:
        print(f"Email config error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    try:
        if request.method == 'OPTIONS':
            return '', 200
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        # Extract registration data
        garage_name = data.get('garage_name')
        owner_name = data.get('owner_name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        trial_days = data.get('trial_days', 14)
        
        # Validate required fields
        if not all([garage_name, owner_name, email, password]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        print(f"🆕 New registration: {email} - {garage_name}")
        
        # Create separate database for this garage
        garage_data = {
            'garage_name': garage_name,
            'owner_name': owner_name,
            'email': email,
            'phone': phone,
            'password': password,
            'trial_days': trial_days
        }
        
        result = db_manager.create_garage_database(garage_data)
        
        # Get trial status
        trial_status = db_manager.get_trial_status(result['garage_id'])
        
        print(f"✅ Database created: {result['database_name']}")
        print(f"📁 Location: databases/{result['database_name']}")
        
        # Return success response with trial info
        return jsonify({
            'success': True,
            'message': 'Registration successful - Your own database created!',
            'user': {
                'id': 1,
                'email': email,
                'name': owner_name,
                'role': 'owner'
            },
            'garage': {
                'id': result['garage_id'],
                'name': garage_name,
                'phone': phone,
                'database': result['database_name']
            },
            'trial': trial_status
        })
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting test backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
