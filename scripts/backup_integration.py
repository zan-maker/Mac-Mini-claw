#!/usr/bin/env python3
"""
Backup Integration for AI Agents
Provides JSON API for managing backups
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from pathlib import Path

class BackupManager:
    """Manage backups via best-backup for AI agents"""
    
    def __init__(self):
        self.env = {
            'BBACKUP_OUTPUT': 'json',
            'BBACKUP_NO_INTERACTIVE': '1'
        }
        self.config_path = Path.home() / '.config' / 'bbackup' / 'config.yaml'
        self.log_dir = Path.home() / 'backups' / 'openclaw' / 'logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def _run_command(self, cmd, description=""):
        """Run command and return JSON result"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env={**os.environ, **self.env}
            )
            
            if result.returncode == 0:
                try:
                    return {
                        'success': True,
                        'data': json.loads(result.stdout),
                        'description': description
                    }
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'data': {'output': result.stdout},
                        'description': description
                    }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'description': description,
                    'returncode': result.returncode
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'description': description
            }
    
    def run_backup(self, backup_set="workspace", incremental=True, remote="local"):
        """Run backup for specific set"""
        cmd = [
            'bbackup', 'backup',
            '--backup-set', backup_set,
            '--remote', remote,
            '--input-json', json.dumps({'incremental': incremental})
        ]
        
        return self._run_command(cmd, f"Backup of {backup_set} to {remote}")
    
    def list_backups(self, remote="local"):
        """List available backups"""
        cmd = ['bbackup', 'list-backups', '--remote', remote]
        return self._run_command(cmd, f"List backups from {remote}")
    
    def health_check(self):
        """Check backup system health"""
        cmd = ['bbman', 'health']
        return self._run_command(cmd, "System health check")
    
    def get_status(self):
        """Get backup system status"""
        cmd = ['bbman', 'status']
        return self._run_command(cmd, "System status")
    
    def cleanup(self, yes=False):
        """Clean up old backups"""
        cmd = ['bbackup', 'cleanup']
        if yes:
            cmd.append('--yes')
        return self._run_command(cmd, "Cleanup old backups")
    
    def discover_skills(self):
        """Discover available backup skills"""
        cmd = ['bbackup', 'skills']
        return self._run_command(cmd, "Discover backup skills")
    
    def restore_backup(self, backup_path, target_set="workspace", destination=None):
        """Restore from backup"""
        cmd = ['bbackup', 'restore', '--backup-path', backup_path]
        
        if target_set == "filesystem" and destination:
            cmd.extend(['--filesystem', 'workspace', '--filesystem-destination', destination])
        else:
            cmd.extend(['--backup-set', target_set])
        
        return self._run_command(cmd, f"Restore {target_set} from {backup_path}")
    
    def full_system_check(self):
        """Run comprehensive system check"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'checks': []
        }
        
        # Health check
        health = self.health_check()
        results['checks'].append({
            'name': 'health',
            'success': health['success'],
            'data': health.get('data', {})
        })
        
        # Status check
        status = self.get_status()
        results['checks'].append({
            'name': 'status',
            'success': status['success'],
            'data': status.get('data', {})
        })
        
        # List recent backups
        backups = self.list_backups()
        results['checks'].append({
            'name': 'backups',
            'success': backups['success'],
            'data': backups.get('data', {})
        })
        
        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            results['disk_space'] = {
                'total_gb': total // (2**30),
                'used_gb': used // (2**30),
                'free_gb': free // (2**30),
                'percent_used': (used / total) * 100
            }
        except Exception as e:
            results['disk_space_error'] = str(e)
        
        # Check if system is healthy
        results['overall_healthy'] = all(check['success'] for check in results['checks'])
        
        return {
            'success': True,
            'data': results,
            'description': 'Full system check completed'
        }

def main():
    """Command-line interface for backup management"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Backup Management for AI Agents')
    parser.add_argument('--action', choices=['backup', 'restore', 'health', 'status', 'list', 'cleanup', 'skills', 'full-check'],
                       default='health', help='Action to perform')
    parser.add_argument('--set', default='workspace', help='Backup set to use')
    parser.add_argument('--remote', default='local', help='Remote storage to use')
    parser.add_argument('--backup-path', help='Path to backup for restore')
    parser.add_argument('--destination', help='Destination for restore')
    
    args = parser.parse_args()
    
    manager = BackupManager()
    
    if args.action == 'backup':
        result = manager.run_backup(args.set, remote=args.remote)
    elif args.action == 'restore':
        if not args.backup_path:
            print(json.dumps({'error': 'Backup path required for restore'}, indent=2))
            sys.exit(1)
        result = manager.restore_backup(args.backup_path, args.set, args.destination)
    elif args.action == 'health':
        result = manager.health_check()
    elif args.action == 'status':
        result = manager.get_status()
    elif args.action == 'list':
        result = manager.list_backups(args.remote)
    elif args.action == 'cleanup':
        result = manager.cleanup(yes=True)
    elif args.action == 'skills':
        result = manager.discover_skills()
    elif args.action == 'full-check':
        result = manager.full_system_check()
    else:
        result = {'error': f'Unknown action: {args.action}'}
    
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result.get('success', False) else 1)

if __name__ == '__main__':
    main()
