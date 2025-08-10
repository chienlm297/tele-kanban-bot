#!/usr/bin/env python3
"""
Simple Flask app for Railway health check
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint cho Railway"""
    return jsonify({
        'status': 'healthy', 
        'timestamp': '2024-01-01',
        'environment': os.getenv('RAILWAY_ENVIRONMENT', 'development'),
        'port': os.getenv('PORT', '5000')
    })

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Tele Kanban Bot is running!',
        'health_check': '/health',
        'environment': os.getenv('RAILWAY_ENVIRONMENT', 'development')
    })

@app.route('/api/stats')
def api_stats():
    """Simple stats endpoint"""
    return jsonify({
        'total': 0,
        'pending': 0,
        'completed': 0,
        'status': 'service_starting'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = '0.0.0.0'
    
    print(f"🚀 Khởi động simple app trên {host}:{port}")
    print(f"🌍 Environment: {os.getenv('RAILWAY_ENVIRONMENT', 'development')}")
    
    app.run(host=host, port=port, debug=False)
