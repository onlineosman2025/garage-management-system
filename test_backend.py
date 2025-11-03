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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting test backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
