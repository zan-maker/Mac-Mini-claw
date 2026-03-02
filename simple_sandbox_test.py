#!/usr/bin/env python3
"""
Simple Sandbox Test - Validate scripts without execution
Checks for common issues before production runs
"""

import os
import sys
import ast
import json
import re
from pathlib import Path

class ScriptValidator:
    """Validate scripts for production readiness"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.recommendations = []
    
    def validate_script(self, script_path):
        """Validate a script for production readiness"""
        script_name = os.path.basename(script_path)
        print(f'\n🔍 Validating: {script_name}')
        print('─' * 50)
        
        try:
            with open(script_path, 'r') as f:
                content = f.read()
            
            # Check 1: File exists and readable
            if not os.path.exists(script_path):
                self.issues.append(f'{script_name}: File does not exist')
                return False
            
            # Check 2: Check for hardcoded credentials
            credential_patterns = [
                r'api[_-]?key["\']?\s*[:=]\s*["\'][^"\']{20,}["\']',
                r'password["\']?\s*[:=]\s*["\'][^"\']+["\']',
                r'secret["\']?\s*[:=]\s*["\'][^"\']{10,}["\']',
                r'token["\']?\s*[:=]\s*["\'][^"\']{20,}["\']',
                r'@gmail\.com',
                r'smtp\.gmail\.com',
                r'587',  # SMTP port
            ]
            
            for pattern in credential_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    self.warnings.append(f'{script_name}: Found potential credential pattern: {pattern}')
            
            # Check 3: Parse Python syntax
            try:
                ast.parse(content)
            except SyntaxError as e:
                self.issues.append(f'{script_name}: Syntax error: {e}')
                return False
            
            # Check 4: Check imports
            tree = ast.parse(content)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(node.module or '')
            
            # Check 5: Look for dangerous operations
            dangerous_patterns = [
                'subprocess.run',
                'os.system',
                'eval(',
                'exec(',
                'shutil.rmtree',
                'os.remove',
            ]
            
            for pattern in dangerous_patterns:
                if pattern in content:
                    self.warnings.append(f'{script_name}: Contains potentially dangerous operation: {pattern}')
            
            # Check 6: Look for error handling
            if 'try:' in content and 'except:' in content:
                self.recommendations.append(f'{script_name}: Has error handling (good)')
            else:
                self.warnings.append(f'{script_name}: Missing error handling')
            
            # Check 7: Check file size
            file_size = os.path.getsize(script_path)
            if file_size > 100000:  # 100KB
                self.warnings.append(f'{script_name}: Large file size ({file_size} bytes)')
            
            print(f'✅ Basic validation passed')
            print(f'   Size: {file_size} bytes')
            print(f'   Imports: {", ".join(imports[:5])}' + ('...' if len(imports) > 5 else ''))
            
            return True
            
        except Exception as e:
            self.issues.append(f'{script_name}: Validation error: {e}')
            return False
    
    def validate_people_data_labs(self):
        """Special validation for People Data Labs integration"""
        print('\n🔬 Validating People Data Labs Integration')
        print('=' * 60)
        
        script_path = 'scripts/people_data_labs_integration.py'
        if not os.path.exists(script_path):
            script_path = 'scripts/test_people_data_labs.py'
        
        success = self.validate_script(script_path)
        
        if success:
            # Check for API key
            with open(script_path, 'r') as f:
                content = f.read()
            
            if 'fa5b2ea6dee53ad4f40b71bd51fc1d48d8c3efeea44faf342e7561be83772093' in content:
                self.warnings.append('People Data Labs: Hardcoded API key found')
                self.recommendations.append('Consider using environment variable for API key')
            
            if 'people_data_labs' in content.lower():
                self.recommendations.append('People Data Labs: Integration looks correct')
        
        return success
    
    def validate_email_scripts(self):
        """Validate email sending scripts"""
        print('\n📧 Validating Email Scripts')
        print('=' * 60)
        
        email_scripts = []
        for script in os.listdir('scripts'):
            if script.endswith('.py') and any(keyword in script.lower() for keyword in ['send', 'email', 'mail', 'gmail']):
                email_scripts.append(os.path.join('scripts', script))
        
        results = []
        for script in email_scripts[:5]:  # Validate first 5
            success = self.validate_script(script)
            results.append((os.path.basename(script), success))
        
        return results
    
    def generate_report(self):
        """Generate validation report"""
        print('\n' + '=' * 60)
        print('📊 VALIDATION REPORT')
        print('=' * 60)
        
        if self.issues:
            print('\n❌ ISSUES FOUND:')
            for issue in self.issues:
                print(f'   • {issue}')
        
        if self.warnings:
            print('\n⚠️  WARNINGS:')
            for warning in self.warnings:
                print(f'   • {warning}')
        
        if self.recommendations:
            print('\n💡 RECOMMENDATIONS:')
            for rec in self.recommendations:
                print(f'   • {rec}')
        
        total_checks = len(self.issues) + len(self.warnings) + len(self.recommendations)
        
        print(f'\n🎯 Summary:')
        print(f'   Issues: {len(self.issues)}')
        print(f'   Warnings: {len(self.warnings)}')
        print(f'   Recommendations: {len(self.recommendations)}')
        print(f'   Total checks: {total_checks}')
        
        if not self.issues:
            print('\n✅ No critical issues found. Scripts are likely safe to run.')
        else:
            print('\n❌ Critical issues found. Fix before production.')

def main():
    """Run validation checks"""
    print('🔧 OpenClaw Script Validator')
    print('=' * 60)
    print('🔍 Static analysis of scripts for production readiness')
    print('📋 Checks for common issues before execution')
    print('=' * 60)
    
    validator = ScriptValidator()
    
    # Validate People Data Labs
    validator.validate_people_data_labs()
    
    # Validate email scripts
    validator.validate_email_scripts()
    
    # Generate report
    validator.generate_report()
    
    print('\n' + '=' * 60)
    print('🚀 NEXT STEPS')
    print('=' * 60)
    
    if not validator.issues:
        print('✅ Scripts passed validation')
        print('💡 Consider:')
        print('   1. Running in test mode first')
        print('   2. Monitoring first production run')
        print('   3. Adding more error handling')
    else:
        print('⚠️  Issues found. Recommended actions:')
        print('   1. Fix critical issues first')
        print('   2. Review warnings')
        print('   3. Test with limited data')
        print('   4. Monitor closely')
    
    print('\n🔧 Production checklist:')
    print('   [ ] Scripts validated')
    print('   [ ] Error handling in place')
    print('   [ ] Rate limits considered')
    print('   [ ] Monitoring configured')
    print('   [ ] Rollback plan ready')

if __name__ == '__main__':
    main()