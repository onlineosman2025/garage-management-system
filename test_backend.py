#!/usr/bin/env python3
"""
Minimal Railway backend test - isolates the deployment issue
"""
from flask import Flask, jsonify
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
    if request.method == 'OPTIONS':
        return '', 200
    
    return jsonify({
        'success': True,
        'token': 'test-token-123',
        'user': {
            'id': 1,
            'email': 'owner@garage.com',
            'name': 'Garage Owner'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting test backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
