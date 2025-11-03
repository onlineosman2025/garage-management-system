#!/usr/bin/env python3
"""
Railway deployment fix - Test script to verify backend works
"""
import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Aggressive CORS for debugging
CORS(app, 
    origins="*",
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True
)

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'python_version': sys.version,
        'environment': dict(os.environ)
    })

@app.route('/api/test')
def test():
    return jsonify({'message': 'Railway backend is working!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
