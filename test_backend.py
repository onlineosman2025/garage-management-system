#!/usr/bin/env python3
"""
Minimal Railway backend test - isolates the deployment issue
Updated: 2025-11-03-13-12-FORCE-DEPLOY
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

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
            
        email = data.get('email', 'unknown')
        password = data.get('password', 'unknown')
        
        print(f"Login attempt: {email}")
        
        # Accept any login for testing
        return jsonify({
            'success': True,
            'access_token': 'test-token-123',
            'user': {
                'id': 1,
                'email': email,
                'name': 'Garage Owner',
                'role': 'owner'
            },
            'garage': {
                'id': 1,
                'name': 'Test Garage',
                'currency': 'AED'
            }
        })
    except Exception as e:
        print(f"Login error: {str(e)}")
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting test backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
