#!/usr/bin/env python3
"""
API Key Security Audit Script
Checks for exposed API keys in files and git history
"""

import os
import re
import json
from pathlib import Path

class SecurityAudit:
    """Security audit for API keys and secrets"""
    
    # Common API key patterns
    API_KEY_PATTERNS = {
        "brevo": r"xkeysib-[a-f0-9]{64,}",
        "openrouter": r"sk-or-v1-[a-f0-9]{64,}",
        "firebase": r"AIzaSy[A-Za-z0-9_-]{33}",
        "cloudinary_url": r"cloudinary://[^@]+@[^/\s]+",
        "cloudinary_key": r"\d{12,}",
        "generic_api_key": r"(?i)(api[_-]?key|secret|token)[\s:=]+['\"]([^'\"]{20,})['\"]",
        "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        "aws": r"AKIA[0-9A-Z]{16}",
        "stripe": r"(?:sk|pk)_(?:test|live)_[0-9a-zA-Z]{24,}",
        "github": r"ghp_[0-9a-zA-Z]{36}",
        "slack": r"xox[bprs]-[0-9a-zA-Z]{10,48}"
    }
    
    @staticmethod
    def scan_file(file_path: str) -> dict:
        """Scan a file for API keys"""
        results = {
            "file": file_path,
            "issues": [],
            "secure": True
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            for key_type, pattern in SecurityAudit.API_KEY_PATTERNS.items():
                matches = re.finditer(pattern, content)
                for match in matches:
                    # Get context (50 chars before and after)
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 50)
                    context = content[start:end]
                    
                    # Mask the key in context
                    masked_context = context.replace(match.group(), "***MASKED***")
                    
                    results["issues"].append({
                        "type": key_type,
                        "line": content[:match.start()].count('\n') + 1,
                        "context": masked_context,
                        "severity": "HIGH" if key_type in ["brevo", "openrouter", "aws", "stripe"] else "MEDIUM"
                    })
            
            if results["issues"]:
                results["secure"] = False
                
        except Exception as e:
            results["error"] = str(e)
            
        return results
    
    @staticmethod
    def scan_directory(directory: str, extensions: list = None) -> dict:
        """Scan a directory for API keys"""
        if extensions is None:
            extensions = ['.py', '.js', '.json', '.env', '.yaml', '.yml', '.txt', '.md']
        
        results = {
            "directory": directory,
            "files_scanned": 0,
            "issues_found": 0,
            "insecure_files": [],
            "secure_files": []
        }
        
        for root, dirs, files in os.walk(directory):
            # Skip virtual environments and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.venv']]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    file_result = SecurityAudit.scan_file(file_path)
                    
                    results["files_scanned"] += 1
                    
                    if not file_result.get("secure", True):
                        results["issues_found"] += len(file_result["issues"])
                        results["insecure_files"].append(file_result)
                    else:
                        results["secure_files"].append(file_path)
        
        return results
    
    @staticmethod
    def generate_report(scan_results: dict) -> str:
        """Generate a security audit report"""
        report = []
        report.append("🔒 API KEY SECURITY AUDIT REPORT")
        report.append("="*50)
        report.append(f"Directory: {scan_results['directory']}")
        report.append(f"Files scanned: {scan_results['files_scanned']}")
        report.append(f"Issues found: {scan_results['issues_found']}")
        report.append(f"Secure files: {len(scan_results['secure_files'])}")
        report.append(f"Insecure files: {len(scan_results['insecure_files'])}")
        report.append("")
        
        if scan_results["issues_found"] > 0:
            report.append("⚠️  SECURITY ISSUES FOUND:")
            report.append("")
            
            for file_result in scan_results["insecure_files"]:
                report.append(f"📁 {file_result['file']}")
                for issue in file_result["issues"]:
                    report.append(f"   • [{issue['severity']}] {issue['type']} at line {issue['line']}")
                    report.append(f"     Context: {issue['context']}")
                report.append("")
            
            report.append("🔧 RECOMMENDED ACTIONS:")
            report.append("   1. Move API keys to environment variables")
            report.append("   2. Update .gitignore to exclude config files with keys")
            report.append("   3. Rotate exposed API keys immediately")
            report.append("   4. Use the secure configuration loader")
            
        else:
            report.append("✅ NO SECURITY ISSUES FOUND")
            report.append("All API keys are properly secured")
        
        return "\n".join(report)

# Run security audit
if __name__ == "__main__":
    print("🔒 RUNNING API KEY SECURITY AUDIT")
    print("="*50)
    
    workspace_dir = "/Users/cubiczan/.openclaw/workspace"
    
    # Scan config directory first (highest risk)
    print("\n📁 Scanning config directory...")
    config_results = SecurityAudit.scan_directory(
        os.path.join(workspace_dir, "config"),
        extensions=['.json', '.env', '.yaml', '.yml', '.txt']
    )
    
    print(SecurityAudit.generate_report(config_results))
    
    # Scan scripts directory
    print("\n📁 Scanning scripts directory...")
    scripts_results = SecurityAudit.scan_directory(
        os.path.join(workspace_dir, "scripts"),
        extensions=['.py', '.sh', '.js']
    )
    
    print(SecurityAudit.generate_report(scripts_results))
    
    # Overall summary
    print("\n" + "="*50)
    print("📊 SECURITY AUDIT SUMMARY")
    print("="*50)
    
    total_issues = config_results["issues_found"] + scripts_results["issues_found"]
    
    if total_issues > 0:
        print(f"❌ {total_issues} SECURITY ISSUES NEED ATTENTION")
        print("")
        print("🚨 URGENT ACTIONS REQUIRED:")
        print("   1. Check the files listed above")
        print("   2. Move API keys to environment variables")
        print("   3. Rotate any exposed keys")
        print("   4. Update git history if keys were committed")
    else:
        print("✅ SECURITY AUDIT PASSED")
        print("No exposed API keys found")
