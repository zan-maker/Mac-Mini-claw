#!/usr/bin/env python3
"""
Skills Monitoring Dashboard
3-Day Skills Blitz Implementation Monitor
"""

import os
import json
import datetime
import subprocess
from pathlib import Path

class SkillsMonitor:
    """Monitor skills implementation and automation"""
    
    def __init__(self):
        self.workspace = "/Users/cubiczan/.openclaw/workspace"
        self.progress_file = os.path.join(self.workspace, "skills_progress.json")
        self.log_file = os.path.join(self.workspace, "skills_blitz.log")
        
    def load_progress(self):
        """Load implementation progress"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {}
    
    def get_log_tail(self, lines=50):
        """Get tail of log file"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                all_lines = f.readlines()
                return ''.join(all_lines[-lines:])
        return "No log file found"
    
    def check_cron_jobs(self):
        """Check active cron jobs"""
        try:
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                cron_jobs = [line for line in result.stdout.split('\n') if "skills" in line.lower() or "blitz" in line.lower() or "python3" in line]
                return cron_jobs
        except:
            pass
        return []
    
    def check_skill_status(self, skill_name):
        """Check if a skill is properly implemented"""
        skill_path = os.path.join(self.workspace, "skills", skill_name.replace(" ", "_").lower())
        
        status = {
            "directory_exists": os.path.exists(skill_path),
            "has_skill_md": os.path.exists(os.path.join(skill_path, "SKILL.md")),
            "has_readme": os.path.exists(os.path.join(skill_path, "README.md")),
            "file_count": len(list(Path(skill_path).rglob("*"))) if os.path.exists(skill_path) else 0
        }
        
        return status
    
    def generate_report(self):
        """Generate monitoring report"""
        progress = self.load_progress()
        
        # Count total planned skills
        total_planned = 0
        if os.path.exists(os.path.join(self.workspace, "3_DAY_SKILLS_BLITZ.py")):
            # Rough count from implementation plan
            total_planned = 10  # From our plan
        
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_skills_planned": total_planned,
            "completed_skills": len(progress.get("completed_skills", [])),
            "failed_skills": len(progress.get("failed_skills", [])),
            "current_day": progress.get("current_day", 1),
            "cron_jobs_active": len(self.check_cron_jobs()),
            "start_time": progress.get("start_time", "Not started"),
            "skills_details": []
        }
        
        # Add details for completed skills
        for skill in progress.get("completed_skills", []):
            skill_status = self.check_skill_status(skill.get("name", ""))
            report["skills_details"].append({
                "name": skill.get("name", ""),
                "day": skill.get("day", 0),
                "status": skill_status,
                "cron_schedule": skill.get("cron_schedule", "None"),
                "script": skill.get("script", "None")
            })
        
        return report
    
    def print_dashboard(self):
        """Print ASCII dashboard"""
        report = self.generate_report()
        
        print("="*80)
        print("🚀 SKILLS IMPLEMENTATION MONITORING DASHBOARD")
        print("="*80)
        print(f"📅 Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏰ Started: {report['start_time'][:19] if report['start_time'] != 'Not started' else 'Not started'}")
        print(f"📊 Current Day: {report['current_day']}/3")
        print(f"✅ Completed Skills: {report['completed_skills']}/{report['total_skills_planned']}")
        print(f"❌ Failed Skills: {report['failed_skills']}")
        print(f"⏰ Active Cron Jobs: {report['cron_jobs_active']}")
        print("="*80)
        
        # Progress bar
        progress_percent = min(100, (report['current_day'] - 1) * 33 + (report['completed_skills'] / max(1, report['total_skills_planned'])) * 33)
        bar_length = 50
        filled = int(bar_length * progress_percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"📈 Overall Progress: [{bar}] {progress_percent:.1f}%")
        print("="*80)
        
        # Skills details
        if report["skills_details"]:
            print("\n🔧 IMPLEMENTED SKILLS:")
            print("-"*80)
            for skill in report["skills_details"]:
                status_symbol = "✅" if skill["status"]["directory_exists"] else "❌"
                print(f"{status_symbol} {skill['name']}")
                print(f"   Day: {skill['day']} | Cron: {skill['cron_schedule']}")
                print(f"   Files: {skill['status']['file_count']} | SKILL.md: {'✅' if skill['status']['has_skill_md'] else '❌'}")
                print(f"   Script: {skill['script'].split('/')[-1] if skill['script'] != 'None' else 'None'}")
                print()
        
        # Recent log entries
        print("\n📝 RECENT ACTIVITY:")
        print("-"*80)
        log_tail = self.get_log_tail(10)
        for line in log_tail.split('\n')[-10:]:
            if line.strip():
                print(f"   {line}")
        
        # Cron jobs
        cron_jobs = self.check_cron_jobs()
        if cron_jobs:
            print("\n⏰ ACTIVE CRON JOBS:")
            print("-"*80)
            for job in cron_jobs[:5]:  # Show first 5
                if job.strip():
                    print(f"   {job}")
        
        print("\n" + "="*80)
        print("🎯 NEXT STEPS:")
        print("="*80)
        
        if report['current_day'] == 1:
            print("1. ✅ Day 1: Security & Data Foundation")
            print("2. 🔄 Day 2: Research & Content Creation (In Progress)")
            print("3. ⏳ Day 3: Automation & Workflow (Upcoming)")
        elif report['current_day'] == 2:
            print("1. ✅ Day 1: Security & Data Foundation (Complete)")
            print("2. ✅ Day 2: Research & Content Creation (Complete)")
            print("3. 🔄 Day 3: Automation & Workflow (In Progress)")
        elif report['current_day'] >= 3:
            print("1. ✅ Day 1: Security & Data Foundation (Complete)")
            print("2. ✅ Day 2: Research & Content Creation (Complete)")
            print("3. ✅ Day 3: Automation & Workflow (Complete)")
            print("\n🎉 ALL SKILLS IMPLEMENTED!")
        
        print("\n" + "="*80)
        print("📊 COMMANDS:")
        print("="*80)
        print("tail -f /Users/cubiczan/.openclaw/workspace/skills_blitz.log")
        print("crontab -l | grep skills")
        print("python3 /Users/cubiczan/.openclaw/workspace/3_DAY_SKILLS_BLITZ.py")
        print("="*80)

def main():
    """Main function"""
    monitor = SkillsMonitor()
    monitor.print_dashboard()
    
    # Save report to file
    report = monitor.generate_report()
    report_file = os.path.join(monitor.workspace, "logs", "skills_report.json")
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_file}")

if __name__ == "__main__":
    main()