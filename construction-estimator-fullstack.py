#!/usr/bin/env python3
"""
Construction Estimator Full-Stack for Railway
Serves both API endpoints AND HTML frontend
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime, timezone
import requests

app = Flask(__name__, static_folder='.', static_url_path='')

@app.after_request
def allow_iframe(response):
    response.headers["X-Frame-Options"] = "ALLOWALL"
    return response


# Configuration
USE_OLLAMA = os.environ.get('USE_OLLAMA', 'false').lower() == 'true'
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434/v1/chat/completions')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
PORT = int(os.environ.get('PORT', 5000))

# Material cost database
MATERIAL_COSTS = {
    "deck": {
        "pressure_treated": 8.50,
        "composite": 12.00,
        "cedar": 10.50,
        "labor": 15.00
    },
    "drywall": {
        "sheet": 12.00,
        "tape_mud": 0.25,
        "labor": 2.50
    },
    "bathroom": {
        "vanity": 800.00,
        "toilet": 350.00,
        "shower": 1200.00,
        "tile": 5.00,
        "labor": 45.00
    },
    "kitchen": {
        "cabinets": 5000.00,
        "countertop": 60.00,
        "appliances": 3000.00,
        "labor": 50.00
    },
    "roof": {
        "shingles": 120.00,
        "underlayment": 50.00,
        "labor": 200.00
    }
}

def get_ai_suggestions(project_type, dimensions):
    """Get AI suggestions based on available providers"""
    prompt = f"""You are a construction estimator AI. Provide suggestions for a {project_type} project.

Project details:
- Type: {project_type}
- Dimensions: {dimensions}

Provide 3-5 practical suggestions including:
1. Material recommendations
2. Cost-saving tips
3. Timeline considerations
4. Common pitfalls to avoid
5. Quality vs budget tradeoffs

Format as a clear, actionable list."""
    
    # Try Ollama first if enabled
    if USE_OLLAMA:
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": "gemma:2b",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            }, timeout=10)
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except:
            pass  # Fall through to OpenAI or static suggestions
    
    # Try OpenAI if API key is available
    if OPENAI_API_KEY:
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except:
            pass  # Fall through to static suggestions
    
    # Static fallback suggestions
    static_suggestions = {
        "deck": """1. Use pressure-treated lumber for structural components to prevent rot
2. Consider composite decking for low maintenance and longer lifespan
3. Space deck boards 1/8" apart for drainage and expansion
4. Use galvanized or stainless steel fasteners to prevent rust stains
5. Include proper ventilation under the deck to prevent moisture buildup""",
        
        "drywall": """1. Use 5/8" drywall for ceilings to prevent sagging
2. Apply joint compound in thin layers, sanding between coats
3. Use corner beads for crisp, durable corners
4. Prime before painting to ensure even paint absorption
5. Consider moisture-resistant drywall for bathrooms and kitchens""",
        
        "bathroom": """1. Install a waterproof membrane behind shower tiles
2. Use exhaust fan with timer to prevent moisture damage
3. Consider heated floors for comfort and resale value
4. Install grab bars during construction for future accessibility
5. Use large-format tiles to minimize grout lines and cleaning""",
        
        "kitchen": """1. Install under-cabinet lighting for task illumination
2. Consider soft-close drawers and cabinets for durability
3. Use quartz countertops for durability and low maintenance
4. Install a pot filler above the stove for convenience
5. Include a dedicated appliance circuit for heavy-duty appliances""",
        
        "roof": """1. Install ice and water shield in valleys and eaves
2. Use proper ventilation to prevent ice dams and extend shingle life
3. Consider architectural shingles for better wind resistance
4. Install flashing around chimneys and vents to prevent leaks
5. Schedule installation during dry weather for best adhesion"""
    }
    
    return static_suggestions.get(project_type, "AI suggestions temporarily unavailable. Please contact support for construction advice.")

# Serve frontend HTML at root
@app.route('/')
def serve_frontend():
    """Serve the construction estimator frontend"""
    try:
        return send_from_directory('.', 'construction-frontend.html')
    except:
        # Fallback to API info if frontend not found
        return jsonify({
            "api": "Construction Estimator API",
            "version": "1.0.0",
            "deployment": "Railway Full-Stack",
            "frontend": "Available at /construction-frontend.html",
            "endpoints": {
                "/": "Frontend interface",
                "/api": "API information",
                "/health": "Health check",
                "/estimate": "Generate estimate (POST)",
                "/quick/<project_type>/<size>": "Quick estimate"
            }
        })

@app.route('/api')
def api_info():
    """API information endpoint"""
    return jsonify({
        "api": "Construction Estimator API",
        "version": "1.0.0",
        "deployment": "Railway Full-Stack",
        "ai_provider": "Ollama" if USE_OLLAMA else ("OpenAI" if OPENAI_API_KEY else "Static"),
        "endpoints": {
            "/": "Frontend interface",
            "/api": "API information",
            "/health": "Health check",
            "/estimate": "Generate estimate (POST)",
            "/quick/<project_type>/<size>": "Quick estimate"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    ai_status = "static"
    if USE_OLLAMA:
        ai_status = "ollama_configured"
    elif OPENAI_API_KEY:
        ai_status = "openai_configured"
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ai_provider": ai_status,
        "environment": os.environ.get('RAILWAY_ENVIRONMENT', 'production'),
        "frontend": "available"
    })

@app.route('/quick/<project_type>/<size>')
def quick_estimate(project_type, size):
    """Quick estimate without AI"""
    if project_type not in MATERIAL_COSTS:
        return jsonify({"error": f"Unknown project type: {project_type}"}), 400
    
    try:
        if 'x' in size:
            length, width = map(float, size.split('x'))
            area = length * width
        else:
            area = float(size)
    except:
        return jsonify({"error": "Invalid size format. Use '20x12' or '200'"}), 400
    
    # Calculate estimate
    costs = MATERIAL_COSTS[project_type]
    if project_type == "deck":
        material_cost = area * costs.get("composite", 12.00)
        labor_cost = area * costs["labor"]
        total = material_cost + labor_cost
    elif project_type == "drywall":
        sheets = area / 32
        material_cost = sheets * costs["sheet"] + area * costs["tape_mud"]
        labor_cost = area * costs["labor"]
        total = material_cost + labor_cost
    elif project_type == "roof":
        squares = area / 100
        material_cost = squares * (costs["shingles"] + costs["underlayment"])
        labor_cost = squares * costs["labor"]
        total = material_cost + labor_cost
    else:
        total = sum(cost for key, cost in costs.items() if key != "labor")
    
    return jsonify({
        "project": project_type.capitalize(),
        "project_type": project_type,
        "size": size,
        "quick_estimate": f"${total:,.2f}",
        "area_sqft": area if 'x' in size else None
    })

@app.route('/estimate', methods=['POST'])
def detailed_estimate():
    """Detailed estimate with AI suggestions"""
    data = request.json
    
    if not data or 'project_type' not in data:
        return jsonify({"error": "Missing project_type"}), 400
    
    project_type = data['project_type']
    dimensions = data.get('dimensions', {})
    
    if project_type not in MATERIAL_COSTS:
        return jsonify({"error": f"Unknown project type: {project_type}"}), 400
    
    # Calculate base estimate
    if project_type == "deck":
        length = dimensions.get('length', 20)
        width = dimensions.get('width', 12)
        area = length * width
        costs = MATERIAL_COSTS[project_type]
        material_cost = area * costs.get("composite", 12.00)
        labor_cost = area * costs["labor"]
        total = material_cost + labor_cost
    elif project_type == "drywall":
        area = dimensions.get('area', 200)
        costs = MATERIAL_COSTS[project_type]
        sheets = area / 32
        material_cost = sheets * costs["sheet"] + area * costs["tape_mud"]
        labor_cost = area * costs["labor"]
        total = material_cost + labor_cost
    elif project_type == "roof":
        area = dimensions.get('area', 1000)
        costs = MATERIAL_COSTS[project_type]
        squares = area / 100
        material_cost = squares * (costs["shingles"] + costs["underlayment"])
        labor_cost = squares * costs["labor"]
        total = material_cost + labor_cost
    else:
        costs = MATERIAL_COSTS[project_type]
        total = sum(cost for key, cost in costs.items() if key != "labor")
        area = None
    
    # Get AI suggestions
    ai_suggestions = get_ai_suggestions(project_type, dimensions)
    
    return jsonify({
        "project_type": project_type,
        "dimensions": dimensions,
        "total_estimate": f"${total:,.2f}",
        "ai_suggestions": ai_suggestions,
        "deployment": "railway-fullstack",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, images)"""
    return send_from_directory('.', path)

if __name__ == '__main__':
    print(f"🚀 Starting Construction Estimator Full-Stack on Railway...")
    print(f"🌐 Port: {PORT}")
    print(f"🤖 AI Provider: {'Ollama' if USE_OLLAMA else ('OpenAI' if OPENAI_API_KEY else 'Static')}")
    print(f"🏗️  Project Types: {', '.join(MATERIAL_COSTS.keys())}")
    print(f"🌍 Frontend: Available at root (/)")
    app.run(host='0.0.0.0', port=PORT)