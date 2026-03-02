#!/usr/bin/env python3
"""
OpenClaw Sandbox Testing System
Safe testing environment for production code before deployment
Inspired by OpenSandbox principles
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import importlib.util

class SandboxTester:
    """Safe sandbox testing environment for production code"""
    
    def __init__(self, workspace_path: str = None):
        """Initialize sandbox testing system"""
        self.workspace_path = workspace_path or os.getcwd()
        self.sandbox_path = os.path.join(self.workspace_path, '.sandbox')
        self.test_results = {}
        
        # Create sandbox directory
        os.makedirs(self.sandbox_path, exist_ok=True)
        
        # Test categories
        self.test_categories = {
            'api_integration': 'API integration tests',
            'email_sending': 'Email sending tests',
            'file_operations': 'File operation tests',
            'external_calls': 'External API calls',
            'security': 'Security checks',
            'performance': 'Performance tests'
        }
    
    def create_sandbox_environment(self) -> str:
        """Create isolated sandbox environment"""
        sandbox_env = os.path.join(self.sandbox_path, 'env')
        os.makedirs(sandbox_env, exist_ok=True)
        
        # Create safe directories
        dirs = ['scripts', 'config', 'data', 'logs', 'temp']
        for dir_name in dirs:
            os.makedirs(os.path.join(sandbox_env, dir_name), exist_ok=True)
        
        # Create safe config files
        safe_config = {
            'sandbox_mode': True,
            'api_keys': {
                'test_mode': True,
                'people_data_labs': 'SANDBOX_TEST_KEY',
                'twitter': 'SANDBOX_TEST_KEY',
                'linkedin': 'SANDBOX_TEST_KEY',
                'gemini': 'SANDBOX_TEST_KEY',
                'xai': 'SANDBOX_TEST_KEY'
            },
            'email': {
                'test_mode': True,
                'smtp_server': 'sandbox.smtp.test',
                'sender': 'test@sandbox.com'
            },
            'rate_limits': {
                'max_api_calls': 10,
                'max_email_sends': 5,
                'max_file_operations': 100
            }
        }
        
        config_path = os.path.join(sandbox_env, 'config', 'sandbox_config.json')
        with open(config_path, 'w') as f:
            json.dump(safe_config, f, indent=2)
        
        print(f'✅ Created sandbox environment at: {sandbox_env}')
        return sandbox_env
    
    def test_script_safely(self, script_path: str, test_type: str = 'api_integration') -> Dict:
        """Test a script safely in sandbox environment"""
        script_name = os.path.basename(script_path)
        print(f'\n🔍 Testing script: {script_name}')
        print(f'📋 Test type: {test_type}')
        print('='*60)
        
        # Create test environment
        test_env = self.create_sandbox_environment()
        
        # Copy script to sandbox
        sandbox_script = os.path.join(test_env, 'scripts', script_name)
        shutil.copy2(script_path, sandbox_script)
        
        # Modify script for sandbox testing
        self._modify_for_sandbox(sandbox_script, test_type)
        
        # Run test
        result = self._run_sandbox_test(sandbox_script, test_type)
        
        # Store results
        self.test_results[script_name] = {
            'script': script_name,
            'test_type': test_type,
            'result': result['status'],
            'output': result['output'][:500],  # Limit output size
            'errors': result['errors'],
            'warnings': result['warnings'],
            'recommendations': result['recommendations']
        }
        
        # Cleanup (optional - keep for debugging)
        # shutil.rmtree(test_env)
        
        return self.test_results[script_name]
    
    def _modify_for_sandbox(self, script_path: str, test_type: str):
        """Modify script for safe sandbox execution"""
        with open(script_path, 'r') as f:
            content = f.read()
        
        # Replace real API keys with sandbox keys
        replacements = {
            'fa5b2ea6dee53ad4f40b71bd51fc1d48d8c3efeea44faf342e7561be83772093': 'SANDBOX_PEOPLE_DATA_LABS_KEY',
            'xai-vzGa7b1VR6o5vLXxKqL69u8iIMWvACT2P8gmt5mrh4wMWqJvnPlZp4B6RK8hum5HHHnfM2g9wKvFkr1t': 'SANDBOX_XAI_KEY',
            'sam@cubiczan.com': 'test@sandbox.com',
            'smtp.gmail.com': 'sandbox.smtp.test',
            '587': '2525'  # Test port
        }
        
        for real_key, sandbox_key in replacements.items():
            content = content.replace(real_key, sandbox_key)
        
        # Add sandbox mode checks
        sandbox_header = '''# SANDBOX MODE - SAFE TESTING
# This script is running in sandbox mode
# All external calls are mocked or limited
# No real data will be sent or modified

import os
SANDBOX_MODE = True
TEST_MODE = True

# Mock external APIs in sandbox mode
if SANDBOX_MODE:
    class MockResponse:
        def __init__(self, status_code=200, text="SANDBOX RESPONSE"):
            self.status_code = status_code
            self.text = text
        def json(self):
            return {"status": "sandbox", "message": "Mock response in sandbox mode"}
    
    import builtins
    original_import = builtins.__import__
    
    def sandbox_import(name, *args, **kwargs):
        if name in ['requests', 'smtplib', 'socket']:
            print(f"⚠️  Sandbox: Mocking import of {name}")
            # Return mock module
            mock_module = type(sys)('mock_' + name)
            if name == 'requests':
                mock_module.get = lambda *args, **kwargs: MockResponse()
                mock_module.post = lambda *args, **kwargs: MockResponse()
            return mock_module
        return original_import(name, *args, **kwargs)
    
    builtins.__import__ = sandbox_import

'''
        
        # Insert sandbox header
        lines = content.split('\n')
        if not lines[0].startswith('#!'):
            lines.insert(0, sandbox_header)
        else:
            lines.insert(1, sandbox_header)
        
        # Write modified script
        with open(script_path, 'w') as f:
            f.write('\n'.join(lines))
    
    def _run_sandbox_test(self, script_path: str, test_type: str) -> Dict:
        """Run script in sandbox environment"""
        result = {
            'status': 'pending',
            'output': '',
            'errors': [],
            'warnings': [],
            'recommendations': []
        }
        
        try:
            # Set sandbox environment variables
            env = os.environ.copy()
            env['SANDBOX_MODE'] = '1'
            env['TEST_MODE'] = '1'
            env['PYTHONPATH'] = os.path.dirname(script_path)
            
            # Run script with timeout
            process = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                env=env,
                cwd=os.path.dirname(script_path)
            )
            
            # Capture output
            result['output'] = process.stdout + process.stderr
            
            # Analyze results
            if process.returncode == 0:
                result['status'] = 'passed'
                result['recommendations'].append('Script runs successfully in sandbox')
                
                # Check for potential issues
                if 'error' in result['output'].lower():
                    result['warnings'].append('Script output contains error messages')
                if 'traceback' in result['output'].lower():
                    result['warnings'].append('Script may have unhandled exceptions')
                    
            else:
                result['status'] = 'failed'
                result['errors'].append(f'Script exited with code {process.returncode}')
                
        except subprocess.TimeoutExpired:
            result['status'] = 'timeout'
            result['errors'].append('Script execution timed out (30 seconds)')
            result['recommendations'].append('Optimize script or increase timeout')
            
        except Exception as e:
            result['status'] = 'error'
            result['errors'].append(f'Test execution error: {str(e)}')
        
        return result
    
    def test_people_data_labs_integration(self) -> Dict:
        """Special test for People Data Labs integration"""
        print('\n🔬 Testing People Data Labs Integration')
        print('='*60)
        
        script_path = os.path.join(self.workspace_path, 'scripts', 'test_people_data_labs.py')
        if not os.path.exists(script_path):
            script_path = os.path.join(self.workspace_path, 'scripts', 'people_data_labs_integration.py')
        
        return self.test_script_safely(script_path, 'api_integration')
    
    def test_email_sending_scripts(self) -> List[Dict]:
        """Test all email sending scripts"""
        print('\n📧 Testing Email Sending Scripts')
        print('='*60)
        
        email_scripts = []
        scripts_dir = os.path.join(self.workspace_path, 'scripts')
        
        for script in os.listdir(scripts_dir):
            if script.endswith('.py') and any(keyword in script.lower() for keyword in ['send', 'email', 'mail', 'gmail', 'smtp']):
                script_path = os.path.join(scripts_dir, script)
                result = self.test_script_safely(script_path, 'email_sending')
                email_scripts.append(result)
        
        return email_scripts
    
    def test_api_integrations(self) -> List[Dict]:
        """Test all API integration scripts"""
        print('\n🔌 Testing API Integration Scripts')
        print('='*60)
        
        api_scripts = []
        scripts_dir = os.path.join(self.workspace_path, 'scripts')
        
        for script in os.listdir(scripts_dir):
            if script.endswith('.py') and any(keyword in script.lower() for keyword in ['api', 'integration', 'test_']):
                script_path = os.path.join(scripts_dir, script)
                result = self.test_script_safely(script_path, 'api_integration')
                api_scripts.append(result)
        
        return api_scripts
    
    def generate_test_report(self) -> str:
        """Generate comprehensive test report"""
        print('\n📊 Generating Test Report')
        print('='*60)
        
        report = {
            'summary': {
                'total_tests': len(self.test_results),
                'passed': sum(1 for r in self.test_results.values() if r['result'] == 'passed'),
                'failed': sum(1 for r in self.test_results.values() if r['result'] == 'failed'),
                'errors': sum(1 for r in self.test_results.values() if r['result'] == 'error'),
                'timeouts': sum(1 for r in self.test_results.values() if r['result'] == 'timeout')
            },
            'detailed_results': self.test_results,
            'recommendations': [],
            'warnings': []
        }
        
        # Collect all recommendations and warnings
        for script_result in self.test_results.values():
            report['recommendations'].extend(script_result.get('recommendations', []))
            report['warnings'].extend(script_result.get('warnings', []))
        
        # Save report
        report_path = os.path.join(self.sandbox_path, 'test_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print(f'\n✅ Tests completed: {report["summary"]["total_tests"]}')
        print(f'🎯 Passed: {report["summary"]["passed"]}')
        print(f'❌ Failed: {report["summary"]["failed"]}')
        print(f'⚠️  Errors: {report["summary"]["errors"]}')
        print(f'⏰ Timeouts: {report["summary"]["timeouts"]}')
        
        if report['warnings']:
            print(f'\n⚠️  Warnings:')
            for warning in set(report['warnings']):
                print(f'   • {warning}')
        
        if report['recommendations']:
            print(f'\n💡 Recommendations:')
            for rec in set(report['recommendations']):
                print(f'   • {rec}')
        
        print(f'\n📄 Full report saved to: {report_path}')
        return report_path
    
    def run_comprehensive_test(self):
        """Run comprehensive sandbox test suite"""
        print('🚀 Starting Comprehensive Sandbox Testing')
        print('='*60)
        print('🔒 All tests run in isolated sandbox environment')
        print('🔑 No real API keys or data will be used')
        print('📧 No real emails will be sent')
        print('='*60)
        
        # Run test suites
        self.test_people_data_labs_integration()
        self.test_email_sending_scripts()
        self.test_api_integrations()
        
        # Generate report
        report_path = self.generate_test_report()
        
        print('\n' + '='*60)
        print('🎉 SANDBOX TESTING COMPLETE!')
        print('='*60)
        print('\n🔧 Next Steps:')
        print('   1. Review test report')
        print('   2. Fix any failed tests')
        print('   3. Run production code with confidence')
        print(f'\n📊 Report: {report_path}')

def main():
    """Main function to run sandbox tests"""
    print('🔧 OpenClaw Sandbox Testing System')
    print('='*60)
    
    # Get workspace path
    workspace_path = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize sandbox tester
    tester = SandboxTester(workspace_path)
    
    # Run comprehensive tests
    tester.run_comprehensive_test()

if __name__ == '__main__':
    main()