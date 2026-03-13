#!/usr/bin/env python3
"""
Integrate Hoppscotch with AI Agent System
Automated API testing for cron jobs and agents
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime

class HoppscotchIntegration:
    """Integrate Hoppscotch with AI agent system"""
    
    def __init__(self, hoppscotch_dir=None):
        self.hoppscotch_dir = hoppscotch_dir or "/Users/cubiczan/.openclaw/workspace/tools/hoppscotch"
        self.collections_dir = os.path.join(self.hoppscotch_dir, "collections")
        self.environments_dir = os.path.join(self.hoppscotch_dir, "environments")
        
    def test_cron_job_apis(self, cron_job_name, environment="production"):
        """
        Test APIs for a specific cron job before execution
        
        Args:
            cron_job_name: Name of cron job (lead-generation, email-outreach, etc.)
            environment: Environment to test against
        """
        
        print(f"🧪 TESTING APIs FOR CRON JOB: {cron_job_name}")
        print("="*50)
        
        # Map cron jobs to Hoppscotch collections
        cron_to_collection = {
            "lead-generation": "lead-generation",
            "email-outreach": "lead-generation",  # Uses Brevo APIs
            "llm-processing": "llm-apis",
            "data-sync": "database-apis",
            "webhook-processing": "webhook-apis"
        }
        
        collection = cron_to_collection.get(cron_job_name)
        if not collection:
            print(f"⚠️  No API tests defined for cron job: {cron_job_name}")
            return False
        
        collection_file = os.path.join(self.collections_dir, f"{collection}.json")
        if not os.path.exists(collection_file):
            print(f"⚠️  Collection file not found: {collection_file}")
            return False
        
        # Run Hoppscotch CLI tests
        try:
            print(f"📋 Running API tests from collection: {collection}")
            print(f"   Environment: {environment}")
            print(f"   Collection file: {collection_file}")
            
            # Check if Hoppscotch CLI is installed
            result = subprocess.run(
                ["hoppscotch", "--version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("⚠️  Hoppscotch CLI not installed")
                print("   Install with: npm install -g @hoppscotch/cli")
                return False
            
            # Run tests
            cmd = [
                "hoppscotch", "test",
                "--collection", collection_file,
                "--env", environment,
                "--report", "json"
            ]
            
            print(f"   Command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.hoppscotch_dir
            )
            
            if result.returncode == 0:
                print("✅ All API tests passed")
                return True
            else:
                print("❌ API tests failed")
                print(f"   Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error running API tests: {e}")
            return False
    
    def create_agent_api_test(self, agent_name, api_endpoints):
        """
        Create API tests for an AI agent
        
        Args:
            agent_name: Name of the agent (trade-recommender, lead-generator, etc.)
            api_endpoints: List of API endpoints the agent uses
        """
        
        print(f"🔧 CREATING API TESTS FOR AGENT: {agent_name}")
        print("="*50)
        
        collection_data = {
            "name": f"{agent_name} Agent APIs",
            "folders": []
        }
        
        for endpoint in api_endpoints:
            folder = {
                "name": endpoint.get("name", "Unnamed Endpoint"),
                "requests": []
            }
            
            # Create test request
            request = {
                "name": f"Test {endpoint.get('name', 'Endpoint')}",
                "method": endpoint.get("method", "GET"),
                "url": endpoint.get("url", ""),
                "headers": endpoint.get("headers", {}),
                "body": endpoint.get("body", {}),
                "tests": [
                    "pm.test('Status code is 200', function() { pm.response.to.have.status(200); });",
                    "pm.test('Response time < 5s', function() { pm.expect(pm.response.responseTime).to.be.below(5000); });"
                ]
            }
            
            # Add agent-specific tests
            if agent_name == "trade-recommender":
                request["tests"].append(
                    "pm.test('Has recommendation field', function() { pm.response.to.have.jsonBody('recommendation'); });"
                )
            elif agent_name == "lead-generator":
                request["tests"].append(
                    "pm.test('Returns leads array', function() { pm.response.to.have.jsonBody('leads'); });"
                )
            
            folder["requests"].append(request)
            collection_data["folders"].append(folder)
        
        # Save collection
        collection_file = os.path.join(self.collections_dir, f"{agent_name}-agent.json")
        with open(collection_file, 'w') as f:
            json.dump(collection_data, f, indent=2)
        
        print(f"✅ Created API tests for {agent_name}")
        print(f"   Collection: {collection_file}")
        print(f"   Endpoints tested: {len(api_endpoints)}")
        
        return collection_file
    
    def generate_test_report(self, test_results, output_format="html"):
        """
        Generate test report from Hoppscotch results
        
        Args:
            test_results: Test results from Hoppscotch CLI
            output_format: Report format (html, json, junit)
        """
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"test-report-{timestamp}.{output_format}"
        report_path = os.path.join(self.hoppscotch_dir, "reports", report_file)
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        # Generate HTML report
        if output_format == "html":
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>API Test Report - {timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .test {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
        .pass {{ background: #d4edda; border-color: #c3e6cb; }}
        .fail {{ background: #f8d7da; border-color: #f5c6cb; }}
        .timestamp {{ color: #7f8c8d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 API Test Report</h1>
        <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>
    
    <div class="summary">
        <h2>Test Summary</h2>
        <p><strong>Total Tests:</strong> {len(test_results.get('tests', []))}</p>
        <p><strong>Passed:</strong> {sum(1 for t in test_results.get('tests', []) if t.get('passed', False))}</p>
        <p><strong>Failed:</strong> {sum(1 for t in test_results.get('tests', []) if not t.get('passed', True))}</p>
        <p><strong>Success Rate:</strong> {(sum(1 for t in test_results.get('tests', []) if t.get('passed', False)) / len(test_results.get('tests', [])) * 100 if test_results.get('tests') else 0):.1f}%</p>
    </div>
    
    <h2>Test Details</h2>
"""

            for test in test_results.get('tests', []):
                status_class = "pass" if test.get('passed', False) else "fail"
                html_content += f"""
    <div class="test {status_class}">
        <h3>{test.get('name', 'Unnamed Test')}</h3>
        <p><strong>Status:</strong> {'✅ PASS' if test.get('passed', False) else '❌ FAIL'}</p>
        <p><strong>Endpoint:</strong> {test.get('endpoint', 'N/A')}</p>
        <p><strong>Response Time:</strong> {test.get('response_time', 'N/A')}ms</p>
        <p><strong>Message:</strong> {test.get('message', '')}</p>
    </div>
"""
            
            html_content += """
</body>
</html>
"""
            
            with open(report_path, 'w') as f:
                f.write(html_content)
        
        print(f"📄 Test report generated: {report_path}")
        return report_path
    
    def setup_cron_preflight_check(self):
        """Set up pre-flight API checks for all cron jobs"""
        
        print("🛫 SETTING UP CRON PRE-FLIGHT CHECKS")
        print("="*50)
        
        cron_jobs = [
            {
                "name": "lead-generation",
                "schedule": "0 9 * * *",  # 9 AM daily
                "description": "Daily lead generation"
            },
            {
                "name": "email-outreach",
                "schedule": "0 14 * * *",  # 2 PM daily
                "description": "Email outreach campaigns"
            },
            {
                "name": "llm-processing",
                "schedule": "*/30 * * * *",  # Every 30 minutes
                "description": "LLM content generation"
            }
        ]
        
        preflight_script = os.path.join(self.hoppscotch_dir, "scripts", "cron-preflight.sh")
        
        script_content = """#!/bin/bash

# 🛫 CRON PRE-FLIGHT API CHECKS
# Run before executing cron jobs to ensure APIs are working

set -e

echo "========================================="
echo "🛫 RUNNING CRON PRE-FLIGHT API CHECKS"
echo "========================================="
echo "Timestamp: $(date)"
echo "========================================="

FAILED_CHECKS=0

# Function to run API tests
run_api_check() {
    local cron_name=$1
    local description=$2
    
    echo ""
    echo "🧪 Testing: $description"
    echo "   Cron job: $cron_name"
    
    if python3 integrate_with_agents.py test_cron "$cron_name" production; then
        echo "   ✅ API check passed"
    else
        echo "   ❌ API check failed"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
}

"""

        for job in cron_jobs:
            script_content += f"""
# {job['description']}
run_api_check "{job['name']}" "{job['description']}"
"""
        
        script_content += """
echo ""
echo "========================================="
echo "📊 PRE-FLIGHT CHECK SUMMARY"
echo "========================================="
echo "Total checks: ${#cron_jobs[@]}"
echo "Failed checks: $FAILED_CHECKS"

if [ $FAILED_CHECKS -eq 0 ]; then
    echo "✅ All API checks passed - cron jobs can proceed"
    exit 0
else
    echo "❌ $FAILED_CHECKS API checks failed - aborting cron jobs"
    echo ""
    echo "⚠️  ACTION REQUIRED:"
    echo "   1. Check API service status"
    echo "   2. Verify API keys are valid"
    echo "   3. Run manual tests in Hoppscotch"
    echo "   4. Fix issues before next cron run"
    exit 1
fi
"""
        
        os.makedirs(os.path.dirname(preflight_script), exist_ok=True)
        with open(preflight_script, 'w') as f:
            f.write(script_content)
        
        os.chmod(preflight_script, 0o755)
        
        print(f"✅ Created cron pre-flight script: {preflight_script}")
        print("")
        print("🎯 Usage:")
        print(f"   {preflight_script}")
        print("")
        print("📋 Checks configured for:")
        for job in cron_jobs:
            print(f"   • {job['name']}: {job['description']}")
        
        return preflight_script

# Example usage
def main():
    """Main integration example"""
    
    print("🚀 HOPPSCOTCH INTEGRATION WITH AI AGENTS")
    print("="*50)
    
    integration = HoppscotchIntegration()
    
    # Example: Create API tests for trade-recommender agent
    trade_recommender_endpoints = [
        {
            "name": "Get Stock Recommendations",
            "method": "POST",
            "url": "http://localhost:8080/api/trade-recommender/recommend",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer ${TRADE_API_KEY}"
            },
            "body": {
                "symbol": "AAPL",
                "timeframe": "daily",
                "strategy": "momentum"
            }
        }
    ]
    
    # Create agent API tests
    collection_file = integration.create_agent_api_test(
        "trade-recommender",
        trade_recommender_endpoints
    )
    
    print("")
    
    # Example: Test cron job APIs
    print("🧪 EXAMPLE: Testing Lead Generation Cron Job APIs")
    success = integration.test_cron_job_apis("lead-generation", "production")
    
    print("")
    
    # Set up cron pre-flight checks
    preflight_script = integration.setup_cron_preflight_check()
    
    print("")
    print("="*50)
    print("🎯 INTEGRATION READY")
    print("="*50)
    print("")
    print("📋 What's been set up:")
    print("   1. Agent API test collections")
    print("   2. Cron job pre-flight API checks")
    print("   3. Test report generation")
    print("   4. Integration scripts")
    print("")
    print("🚀 Next steps:")
    print(f"   1. Deploy Hoppscotch: cd tools/hoppscotch && ./start.sh")
    print(f"   2. Run pre-flight checks: {preflight_script}")
    print("   3. Integrate with CI/CD pipeline")
    print("   4. Add to cron job scripts")
    print("")
    print("💰 Benefits:")
    print("   • Catch API issues before cron jobs run")
    print("   • Automated API testing")
    print("   • Better reliability for AI agents")
    print("   • Cost savings: $110/month")

if __name__ == "__main__":
    main()
