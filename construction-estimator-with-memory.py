#!/usr/bin/env python3
"""
Construction Estimator with Agent Memory Integration
Enhanced version with memory retention for smarter estimates
"""

from flask import Flask, request, jsonify
import requests
import json
import sqlite3
import os
from datetime import datetime, timezone

app = Flask(__name__)

# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"

# Memory database
MEMORY_DB = "/Users/cubiczan/.openclaw/workspace/agent_memory.db"

def init_memory_db():
    """Initialize memory database if not exists"""
    if not os.path.exists(MEMORY_DB):
        conn = sqlite3.connect(MEMORY_DB)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS construction_projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                project_type TEXT NOT NULL,
                dimensions TEXT NOT NULL,
                estimate REAL NOT NULL,
                customer_name TEXT,
                customer_email TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_email TEXT NOT NULL,
                preference_key TEXT NOT NULL,
                preference_value TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print(f"✅ Memory database initialized: {MEMORY_DB}")

def store_project_memory(project_id, project_type, dimensions, estimate, customer_name=None, customer_email=None):
    """Store construction project in memory"""
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO construction_projects 
        (project_id, project_type, dimensions, estimate, customer_name, customer_email)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (project_id, project_type, json.dumps(dimensions), estimate, customer_name, customer_email))
    
    # Also store as agent memory for learning
    cursor.execute('''
        INSERT INTO agent_memories (agent_id, category, content)
        VALUES (?, ?, ?)
    ''', ('construction-estimator', 'projects', 
          f"Project: {project_type}, Dimensions: {dimensions}, Estimate: ${estimate:,.2f}"))
    
    conn.commit()
    conn.close()
    return True

def get_customer_preferences(customer_email):
    """Get customer preferences from memory"""
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT preference_key, preference_value 
        FROM customer_preferences 
        WHERE customer_email = ?
        ORDER BY timestamp DESC
        LIMIT 10
    ''', (customer_email,))
    
    preferences = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return preferences

def store_customer_preference(customer_email, key, value):
    """Store customer preference in memory"""
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO customer_preferences (customer_email, preference_key, preference_value)
        VALUES (?, ?, ?)
    ''', (customer_email, key, value))
    
    conn.commit()
    conn.close()
    return True

def get_similar_projects(project_type, dimensions):
    """Find similar past projects from memory"""
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT project_type, dimensions, estimate, timestamp
        FROM construction_projects
        WHERE project_type = ?
        ORDER BY timestamp DESC
        LIMIT 5
    ''', (project_type,))
    
    similar = []
    for row in cursor.fetchall():
        similar.append({
            'project_type': row[0],
            'dimensions': json.loads(row[1]),
            'estimate': row[2],
            'timestamp': row[3]
        })
    
    conn.close()
    return similar

def get_ai_suggestions_with_memory(project_type, dimensions, customer_email=None):
    """Get AI suggestions enhanced with memory"""
    # Get similar projects from memory
    similar_projects = get_similar_projects(project_type, dimensions)
    
    # Get customer preferences if email provided
    preferences = {}
    if customer_email:
        preferences = get_customer_preferences(customer_email)
    
    # Build context from memory
    memory_context = ""
    if similar_projects:
        memory_context = "Similar past projects:\n"
        for i, proj in enumerate(similar_projects[:3], 1):
            memory_context += f"{i}. {proj['project_type']} ({proj['dimensions']}): ${proj['estimate']:,.2f}\n"
    
    if preferences:
        memory_context += "\nCustomer preferences:\n"
        for key, value in preferences.items():
            memory_context += f"- {key}: {value}\n"
    
    # Call Ollama with memory context
    prompt = f"""You are a construction estimator AI. Provide suggestions for a {project_type} project.

{memory_context}

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
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "gemma:2b",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }, timeout=30)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "AI suggestions temporarily unavailable. Please check Ollama service."
    except Exception as e:
        return f"AI service error: {str(e)}"

# Initialize memory database on startup
init_memory_db()

# Material cost database
MATERIAL_COSTS = {
    "deck": {
        "pressure_treated": 8.50,  # per sqft
        "composite": 12.00,
        "cedar": 10.50,
        "labor": 15.00  # per sqft
    },
    "drywall": {
        "sheet": 12.00,  # per sheet (4x8)
        "tape_mud": 0.25,  # per sqft
        "labor": 2.50  # per sqft
    },
    "bathroom": {
        "vanity": 800.00,
        "toilet": 350.00,
        "shower": 1200.00,
        "tile": 5.00,  # per sqft
        "labor": 45.00  # per hour
    },
    "kitchen": {
        "cabinets": 5000.00,
        "countertop": 60.00,  # per sqft
        "appliances": 3000.00,
        "labor": 50.00  # per hour
    },
    "roof": {
        "shingles": 120.00,  # per square (100 sqft)
        "underlayment": 50.00,  # per square
        "labor": 200.00  # per square
    }
}

@app.route('/')
def home():
    """Home page with API info"""
    return jsonify({
        "api": "Construction Estimator with Memory",
        "version": "2.0.0",
        "features": [
            "AI-powered estimates with Ollama",
            "Memory retention for smarter suggestions",
            "Customer preference learning",
            "Similar project matching"
        ],
        "endpoints": {
            "/": "API information",
            "/health": "Health check",
            "/estimate": "Generate estimate with memory (POST)",
            "/quick/<project_type>/<size>": "Quick estimate",
            "/projects": "List past projects",
            "/customer/<email>/preferences": "Get customer preferences"
        },
        "memory": "SQLite database with project history"
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    # Check Ollama connection
    ollama_status = "connected"
    try:
        response = requests.get("http://localhost:11434/v1/models", timeout=5)
        if response.status_code != 200:
            ollama_status = "disconnected"
    except:
        ollama_status = "disconnected"
    
    # Check memory database
    memory_status = "connected"
    try:
        conn = sqlite3.connect(MEMORY_DB)
        conn.close()
    except:
        memory_status = "disconnected"
    
    return jsonify({
        "status": "healthy",
        "ollama": ollama_status,
        "memory": memory_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route('/quick/<project_type>/<size>')
def quick_estimate(project_type, size):
    """Quick estimate without AI"""
    if project_type not in MATERIAL_COSTS:
        return jsonify({"error": f"Unknown project type: {project_type}"}), 400
    
    try:
        # Parse size (e.g., "20x12" or "200")
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
        sheets = area / 32  # 4x8 = 32 sqft per sheet
        material_cost = sheets * costs["sheet"] + area * costs["tape_mud"]
        labor_cost = area * costs["labor"]
        total = material_cost + labor_cost
    elif project_type == "roof":
        squares = area / 100
        material_cost = squares * (costs["shingles"] + costs["underlayment"])
        labor_cost = squares * costs["labor"]
        total = material_cost + labor_cost
    else:
        # Fixed cost projects
        total = sum(cost for key, cost in costs.items() if key != "labor")
    
    return jsonify({
        "project": project_type.capitalize(),
        "size": size,
        "quick_estimate": f"${total:,.2f}",
        "area_sqft": area if 'x' in size else None
    })

@app.route('/estimate', methods=['POST'])
def detailed_estimate():
    """Detailed estimate with AI suggestions and memory"""
    data = request.json
    
    if not data or 'project_type' not in data:
        return jsonify({"error": "Missing project_type"}), 400
    
    project_type = data['project_type']
    dimensions = data.get('dimensions', {})
    customer_email = data.get('customer_email')
    customer_name = data.get('customer_name')
    
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
        # Fixed cost projects
        costs = MATERIAL_COSTS[project_type]
        total = sum(cost for key, cost in costs.items() if key != "labor")
        area = None
    
    # Generate project ID
    project_id = f"{project_type}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    
    # Store in memory
    store_project_memory(project_id, project_type, dimensions, total, customer_name, customer_email)
    
    # Store customer preferences if provided
    if customer_email and 'preferences' in data:
        for key, value in data['preferences'].items():
            store_customer_preference(customer_email, key, value)
    
    # Get AI suggestions with memory
    ai_suggestions = get_ai_suggestions_with_memory(project_type, dimensions, customer_email)
    
    # Get similar projects for context
    similar_projects = get_similar_projects(project_type, dimensions)
    
    return jsonify({
        "project_id": project_id,
        "project_type": project_type,
        "dimensions": dimensions,
        "total_estimate": f"${total:,.2f}",
        "customer": {
            "name": customer_name,
            "email": customer_email
        } if customer_name or customer_email else None,
        "ai_suggestions": ai_suggestions,
        "memory_enhanced": True,
        "similar_projects_count": len(similar_projects),
        "similar_projects": similar_projects[:3] if similar_projects else [],
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route('/projects')
def list_projects():
    """List all stored construction projects"""
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT project_id, project_type, dimensions, estimate, customer_name, timestamp
        FROM construction_projects
        ORDER BY timestamp DESC
        LIMIT 20
    ''')
    
    projects = []
    for row in cursor.fetchall():
        projects.append({
            'project_id': row[0],
            'project_type': row[1],
            'dimensions': json.loads(row[2]),
            'estimate': row[3],
            'customer_name': row[4],
            'timestamp': row[5]
        })
    
    conn.close()
    
    return jsonify({
        "total_projects": len(projects),
        "projects": projects
    })

@app.route('/customer/<email>/preferences')
def get_preferences(email):
    """Get customer preferences"""
    preferences = get_customer_preferences(email)
    
    return jsonify({
        "customer_email": email,
        "preferences": preferences,
        "preference_count": len(preferences)
    })

if __name__ == '__main__':
    print("🚀 Starting Construction Estimator with Memory...")
    print(f"📊 Memory Database: {MEMORY_DB}")
    print("🌐 API: http://localhost:5001")
    print("🤖 AI: Ollama (gemma:2b)")
    print("💾 Features: Memory retention, customer preferences, similar project matching")
    app.run(host='0.0.0.0', port=5001, debug=True)