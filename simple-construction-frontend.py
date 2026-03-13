#!/usr/bin/env python3
"""
Simple Construction Estimator Frontend for Railway
Just serves the HTML frontend
"""

from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

PORT = int(os.environ.get('PORT', 5000))

# Serve frontend at root
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'construction-frontend.html')

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    print(f"🚀 Starting Simple Construction Frontend on port {PORT}")
    print(f"🌍 Frontend: Available at /")
    print(f"📁 Serving from: {os.getcwd()}")
    app.run(host='0.0.0.0', port=PORT, debug=False)