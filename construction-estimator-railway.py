#!/usr/bin/env python3
"""
Construction Estimator API for Railway Deployment
Simplified version for Railway hosting
"""

from flask import Flask, jsonify, request, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

PORT = int(os.environ.get('PORT', 5000))

# Construction cost database
CONSTRUCTION_COSTS = {
    'deck': {
        'material_per_sqft': 15.00,
        'labor_per_sqft': 12.00,
        'description': 'Wood deck construction'
    },
    'drywall': {
        'material_per_sqft': 1.50,
        'labor_per_sqft': 2.50,
        'description': 'Drywall installation'
    },
    'bathroom': {
        'material_per_sqft': 75.00,
        'labor_per_sqft': 50.00,
        'description': 'Bathroom renovation'
    },
    'kitchen': {
        'material_per_sqft': 150.00,
        'labor_per_sqft': 75.00,
        'description': 'Kitchen remodeling'
    },
    'roof': {
        'material_per_sqft': 4.50,
        'labor_per_sqft': 3.50,
        'description': 'Roof replacement'
    }
}

def calculate_estimate(project_type, width, length):
    """Calculate construction estimate"""
    if project_type not in CONSTRUCTION_COSTS:
        return None
    
    area = width * length
    costs = CONSTRUCTION_COSTS[project_type]
    
    material_cost = area * costs['material_per_sqft']
    labor_cost = area * costs['labor_per_sqft']
    total_cost = material_cost + labor_cost
    
    return {
        'project': project_type,
        'area_sqft': area,
        'width': width,
        'length': length,
        'material_cost': f"${material_cost:,.2f}",
        'labor_cost': f"${labor_cost:,.2f}",
        'total_cost': f"${total_cost:,.2f}",
        'description': costs['description'],
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

@app.route('/')
def serve_frontend():
    """Serve the frontend HTML"""
    return send_from_directory('.', 'construction-frontend.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Construction Estimator API',
        'version': '2.0.0',
        'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'production'),
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })

@app.route('/api')
def api_info():
    """API information"""
    return jsonify({
        'api': 'Construction Estimator API',
        'version': '2.0.0',
        'deployment': 'Railway',
        'endpoints': {
            '/': 'Frontend interface',
            '/api': 'API information',
            '/estimate': 'Generate estimate (POST)',
            '/health': 'Health check',
            '/quick/<project_type>/<size>': 'Quick estimate'
        }
    })

@app.route('/quick/<project_type>/<size>')
def quick_estimate(project_type, size):
    """Quick estimate endpoint (e.g., /quick/deck/20x12)"""
    try:
        # Parse size (e.g., "20x12")
        if 'x' in size:
            width, length = map(float, size.split('x'))
        else:
            # Assume square
            width = length = float(size)
        
        estimate = calculate_estimate(project_type, width, length)
        if estimate:
            return jsonify(estimate)
        else:
            return jsonify({'error': 'Invalid project type'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid size format. Use WxL or single number'}), 400

@app.route('/estimate', methods=['POST'])
def detailed_estimate():
    """Detailed estimate with AI suggestions"""
    try:
        data = request.get_json()
        project_type = data.get('project_type', '').lower()
        width = float(data.get('width', 0))
        length = float(data.get('length', 0))
        
        if project_type not in CONSTRUCTION_COSTS:
            return jsonify({'error': 'Invalid project type'}), 400
        
        estimate = calculate_estimate(project_type, width, length)
        
        # Add AI suggestions (static for Railway)
        ai_suggestions = [
            f"Consider using pressure-treated lumber for {project_type} durability.",
            f"Add 10-15% to budget for unexpected expenses.",
            f"Check local building permits before starting {project_type}.",
            f"Consider seasonal pricing - materials may be cheaper in winter."
        ]
        
        estimate['ai_suggestions'] = ai_suggestions
        estimate['ai_provider'] = 'static'
        
        return jsonify(estimate)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

if __name__ == '__main__':
    print(f"🚀 Starting Construction Estimator API on port {PORT}")
    print(f"🌍 Frontend: Available at /")
    print(f"🔧 API: Available at /api")
    print(f"🏗️ Project types: {', '.join(CONSTRUCTION_COSTS.keys())}")
    app.run(host='0.0.0.0', port=PORT, debug=False)