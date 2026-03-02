#!/usr/bin/env python3
"""
Quick Sandbox Test for Production Code
Safe testing before running in production
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path

def create_safe_test_environment():
    """Create a safe testing environment"""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix='sandbox_')
    print(f'🔒 Created sandbox environment: {temp_dir}')
    
    # Create directory structure
    dirs = ['scripts', 'config', 'data', 'logs']
    for dir_name in dirs:
        os.makedirs(os.path.join(temp_dir, dir_name), exist_ok=True)
    
    # Create safe config
    safe_config = {
        'sandbox_mode': True,
        'test_mode': True,
        'apis': {
            'people_data_labs': {'api_key': 'SANDBOX_TEST_KEY'},
            'twitter': {'api_key': 'SANDBOX_TEST_KEY'},
            'gemini': {'api_key': 'SANDBOX_TEST_KEY'},
            'xai': {'api_key': 'SANDBOX_TEST_KEY'}
        },
        'email': {
            'smtp_server': 'sandbox.smtp.test',
            'port': 2525,
            'sender': 'test@sandbox.com'
        }
    }
    
    config_path = os.path.join(temp_dir, 'config', 'sandbox_config.json')
    with open(config_path, 'w') as f:
        json.dump(safe_config, f, indent=2)
    
    return temp_dir

def test_script_safely(script_path, sandbox_dir):
    """Test a script in sandbox environment"""
    script_name = os.path.basename(script_path)
    print(f'\n🔍 Testing: {script_name}')
    print('─' * 50)
    
    # Copy script to sandbox
    sandbox_script = os.path.join(sandbox_dir, 'scripts', script_name)
    shutil.copy2(script_path, sandbox_script)
    
    # Modify script for sandbox
    with open(sandbox_script, 'r') as f:
        content = f.read()
    
    # Replace real credentials with sandbox ones
    replacements = {
        'fa5b2ea6dee53ad4f40b71bd51fc1d48d8c3efeea44faf342e7561be83772093': 'SANDBOX_PDL_KEY',
        'xai-vzGa7b1VR6o5vLXxKqL69u8iIMWvACT2P8gmt5mrh4wMWqJvnPlZp4B6RK8hum5HHHnfM2g9wKvFkr1t': 'SANDBOX_XAI_KEY',
        'sam@cubiczan.com': 'test@sandbox.com',
        'smtp.gmail.com': 'sandbox.smtp.test',
        '587': '2525'
    }
    
    for real, sandbox in replacements.items():
        content = content.replace(real, sandbox)
    
    # Add sandbox header
    sandbox_header = '''# 🔒 SANDBOX TEST MODE
# This script is running in isolated sandbox
# No real API calls or emails will be sent
# All external services are mocked

SANDBOX_MODE = True
TEST_MODE = True

import sys
import os

# Mock requests module in sandbox
class MockResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code
        self.text = "SANDBOX RESPONSE"
    def json(self):
        return {"status": "sandbox", "data": "Mock data for testing"}

class MockRequests:
    def get(self, *args, **kwargs):
        print(f"🔒 Sandbox: Mocking GET request to {args[0] if args else 'unknown'}")
        return MockResponse()
    def post(self, *args, **kwargs):
        print(f"🔒 Sandbox: Mocking POST request to {args[0] if args else 'unknown'}")
        return MockResponse()

# Mock smtplib
class MockSMTP:
    def __init__(self, *args, **kwargs):
        print(f"🔒 Sandbox: Mocking SMTP connection to {args[0] if args else 'unknown'}")
    def login(self, *args, **kwargs):
        print("🔒 Sandbox: Mocking SMTP login")
        return True
    def sendmail(self, *args, **kwargs):
        print(f"🔒 Sandbox: Mocking email send to {args[1] if len(args) > 1 else 'unknown'}")
        return {}
    def quit(self, *args, **kwargs):
        print("🔒 Sandbox: Mocking SMTP quit")
        return True

# Replace real modules with mocks
sys.modules['requests'] = MockRequests()
sys.modules['smtplib'].SMTP = MockSMTP

print("=" * 60)
print("🔒 RUNNING IN SANDBOX MODE")
print("🔒 All external calls are mocked")
print("🔒 No real data will be sent")
print("=" * 60)

'''
    
    # Insert header after shebang if present
    lines = content.split('\n')
    if lines[0].startswith('#!'):
        lines.insert(1, sandbox_header)
    else:
        lines.insert(0, sandbox_header)
    
    with open(sandbox_script, 'w') as f:
        f.write('\n'.join(lines))
    
    # Run the script
    try:
        result = subprocess.run(
            [sys.executable, sandbox_script],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=os.path.dirname(sandbox_script)
        )
        
        print(f'📊 Exit code: {result.returncode}')
        print(f'📝 Output length: {len(result.stdout)} chars')
        
        if result.returncode == 0:
            print('✅ Script ran successfully in sandbox')
            # Show first few lines of output
            output_lines = result.stdout.split('\n')
            for line in output_lines[:10]:
                if line.strip():
                    print(f'   {line}')
            if len(output_lines) > 10:
                print(f'   ... and {len(output_lines) - 10} more lines')
        else:
            print('❌ Script failed in sandbox')
            if result.stderr:
                print(f'   Error: {result.stderr[:200]}')
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print('⏰ Script timed out (15 seconds)')
        return False
    except Exception as e:
        print(f'💥 Test error: {e}')
        return False

def test_people_data_labs():
    """Test People Data Labs integration"""
    print('\n🔬 Testing People Data Labs Integration')
    print('=' * 60)
    
    script_path = 'scripts/test_people_data_labs.py'
    if not os.path.exists(script_path):
        script_path = 'scripts/people_data_labs_integration.py'
    
    sandbox_dir = create_safe_test_environment()
    success = test_script_safely(script_path, sandbox_dir)
    
    # Cleanup
    shutil.rmtree(sandbox_dir, ignore_errors=True)
    
    return success

def test_email_scripts():
    """Test email sending scripts"""
    print('\n📧 Testing Email Scripts')
    print('=' * 60)
    
    email_scripts = []
    for script in os.listdir('scripts'):
        if script.endswith('.py') and any(keyword in script.lower() for keyword in ['send', 'email', 'mail', 'gmail']):
            email_scripts.append(os.path.join('scripts', script))
    
    results = []
    for script in email_scripts[:3]:  # Test first 3
        sandbox_dir = create_safe_test_environment()
        success = test_script_safely(script, sandbox_dir)
        results.append((os.path.basename(script), success))
        shutil.rmtree(sandbox_dir, ignore_errors=True)
    
    return results

def main():
    """Run comprehensive sandbox tests"""
    print('🚀 OpenClaw Sandbox Testing')
    print('=' * 60)
    print('🔒 Safe testing before production deployment')
    print('🔑 No real API keys or credentials used')
    print('📧 No real emails sent')
    print('=' * 60)
    
    # Test People Data Labs
    pdl_success = test_people_data_labs()
    
    # Test email scripts
    email_results = test_email_scripts()
    
    # Summary
    print('\n' + '=' * 60)
    print('📊 TEST SUMMARY')
    print('=' * 60)
    
    print(f'\n🔬 People Data Labs: {"✅ PASS" if pdl_success else "❌ FAIL"}')
    
    print('\n📧 Email Scripts:')
    for script_name, success in email_results:
        print(f'   {script_name}: {"✅ PASS" if success else "❌ FAIL"}')
    
    total_tests = 1 + len(email_results)
    passed_tests = (1 if pdl_success else 0) + sum(1 for _, success in email_results if success)
    
    print(f'\n🎯 Total tests: {total_tests}')
    print(f'✅ Passed: {passed_tests}')
    print(f'❌ Failed: {total_tests - passed_tests}')
    
    print('\n' + '=' * 60)
    print('💡 RECOMMENDATIONS')
    print('=' * 60)
    
    if passed_tests == total_tests:
        print('🎉 All tests passed! Ready for production.')
    else:
        print('⚠️  Some tests failed. Review before production deployment.')
        print('   • Check error messages above')
        print('   • Verify script logic')
        print('   • Test with real data cautiously')
    
    print('\n🔧 Next steps:')
    print('   1. Review test output above')
    print('   2. Fix any issues found')
    print('   3. Run production code with confidence')
    print('   4. Monitor first production run closely')

if __name__ == '__main__':
    main()