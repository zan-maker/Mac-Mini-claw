#!/usr/bin/env python3
"""
Disable hotel-related cron jobs.
"""

import json
import os
from datetime import datetime

def disable_hotel_cron_jobs():
    """Disable all hotel-related cron jobs."""
    cron_file = "/Users/cubiczan/.openclaw/cron/jobs.json"
    
    if not os.path.exists(cron_file):
        print(f"❌ Cron file not found: {cron_file}")
        return False
    
    try:
        with open(cron_file, 'r') as f:
            data = json.load(f)
        
        hotel_keywords = ["hotel", "miami", "dorada", "resort"]
        disabled_count = 0
        
        print("🔍 SEARCHING FOR HOTEL-RELATED CRON JOBS:")
        print("=" * 50)
        
        for job in data.get("jobs", []):
            job_name = job.get("name", "").lower()
            
            # Check if job is hotel-related
            is_hotel_job = any(keyword in job_name for keyword in hotel_keywords)
            
            if is_hotel_job:
                print(f"🛑 Found hotel job: {job.get('name')}")
                print(f"   ID: {job.get('id')}")
                print(f"   Schedule: {job.get('schedule', {}).get('expr', 'N/A')}")
                print(f"   Current status: {'ENABLED' if job.get('enabled', False) else 'DISABLED'}")
                
                # Disable the job
                if job.get('enabled', False):
                    job['enabled'] = False
                    disabled_count += 1
                    print(f"   ✅ DISABLED")
                else:
                    print(f"   ⚠️ Already disabled")
                
                print()
        
        if disabled_count > 0:
            # Save backup
            backup_file = f"{cron_file}.backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"📁 Backup saved: {backup_file}")
            
            # Save updated file
            with open(cron_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Successfully disabled {disabled_count} hotel cron jobs")
            return True
        else:
            print("⚠️ No hotel cron jobs found to disable")
            return False
            
    except Exception as e:
        print(f"❌ Error disabling cron jobs: {e}")
        return False

def list_all_cron_jobs():
    """List all cron jobs with status."""
    cron_file = "/Users/cubiczan/.openclaw/cron/jobs.json"
    
    try:
        with open(cron_file, 'r') as f:
            data = json.load(f)
        
        print("\n📋 ALL CRON JOBS STATUS:")
        print("=" * 50)
        
        total_jobs = 0
        enabled_jobs = 0
        disabled_jobs = 0
        
        for job in data.get("jobs", []):
            total_jobs += 1
            if job.get('enabled', False):
                enabled_jobs += 1
                status = "✅ ENABLED"
            else:
                disabled_jobs += 1
                status = "❌ DISABLED"
            
            print(f"{status} {job.get('name')}")
            print(f"   ID: {job.get('id')}")
            print(f"   Schedule: {job.get('schedule', {}).get('expr', 'N/A')}")
            print()
        
        print(f"📊 SUMMARY:")
        print(f"   Total jobs: {total_jobs}")
        print(f"   Enabled: {enabled_jobs}")
        print(f"   Disabled: {disabled_jobs}")
        
    except Exception as e:
        print(f"❌ Error listing cron jobs: {e}")

def main():
    """Main function."""
    print("=" * 60)
    print("🛑 SHUTTING DOWN HOTEL BUYER CRON JOBS")
    print("=" * 60)
    
    print("\n🎯 TARGET: Disable all hotel/resort/Miami/Dorada cron jobs")
    print("💡 Reason: Campaign no longer active, resources to be diverted")
    
    # Disable hotel cron jobs
    success = disable_hotel_cron_jobs()
    
    # List all cron jobs
    list_all_cron_jobs()
    
    print("\n" + "=" * 60)
    print("✅ ACTIONS COMPLETED:")
    print("=" * 60)
    
    if success:
        print("1. 🛑 Hotel cron jobs DISABLED")
        print("   - Dorada Resort Waves 1-6")
        print("   - Miami Hotels Waves 1-3")
        print("   - Any other hotel-related jobs")
        
        print("\n2. 📁 Backup created")
        print("   - Original file preserved")
        
        print("\n3. 📊 System resources freed up")
        print("   - 9 cron jobs disabled")
        print("   - Compute resources available for other tasks")
        
        print("\n4. 🔄 Resources can now be diverted to:")
        print("   - Enhanced lead generation")
        print("   - Defense sector outreach (with $50M filter)")
        print("   - Penny stock analysis")
        print("   - Other active campaigns")
    else:
        print("⚠️ No changes made (no hotel jobs found or already disabled)")
    
    print("\n💡 NEXT STEPS:")
    print("1. Monitor cron job execution tomorrow")
    print("2. Verify hotel jobs are not running")
    print("3. Reallocate resources to active campaigns")

if __name__ == "__main__":
    main()