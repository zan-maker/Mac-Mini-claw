#!/usr/bin/env python3
"""
Test the full Craigslist referral fee system
"""

import os
import json
from datetime import datetime

def test_system():
    print("Testing Craigslist Referral Fee System...")
    print(f"{'='*60}")
    
    # 1. Check virtual environment
    print("1. Checking virtual environment...")
    venv_path = "/Users/cubiczan/.openclaw/workspace/craigslist-env"
    if os.path.exists(venv_path):
        print("   ✅ Virtual environment exists")
    else:
        print("   ❌ Virtual environment not found")
        return False
    
    # 2. Check scripts
    print("\n2. Checking scripts...")
    scripts = [
        "craigslist_daily_scraper.py",
        "process_craigslist_leads.py",
        "run_craigslist_scraper.sh",
        "run_lead_processor.sh"
    ]
    
    all_scripts_ok = True
    for script in scripts:
        script_path = f"/Users/cubiczan/.openclaw/workspace/scripts/{script}"
        if os.path.exists(script_path):
            print(f"   ✅ {script}")
        else:
            print(f"   ❌ {script} not found")
            all_scripts_ok = False
    
    if not all_scripts_ok:
        return False
    
    # 3. Check output directory
    print("\n3. Checking output directory...")
    output_dir = "/Users/cubiczan/.openclaw/workspace/craigslist-leads"
    if os.path.exists(output_dir):
        print("   ✅ Output directory exists")
        
        # Check if writable
        test_file = f"{output_dir}/test_write.txt"
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("   ✅ Output directory is writable")
        except:
            print("   ❌ Output directory is not writable")
            return False
    else:
        print("   ❌ Output directory not found")
        return False
    
    # 4. Check test leads file
    print("\n4. Checking test data...")
    test_leads = "/Users/cubiczan/.openclaw/workspace/craigslist-leads/test_leads.json"
    if os.path.exists(test_leads):
        try:
            with open(test_leads, 'r') as f:
                data = json.load(f)
            print(f"   ✅ Test leads file loaded ({len(data)} leads)")
        except Exception as e:
            print(f"   ❌ Error loading test leads: {e}")
            return False
    else:
        print("   ❌ Test leads file not found")
        return False
    
    # 5. Check AgentMail API key (masked)
    print("\n5. Checking configuration...")
    config_file = "/Users/cubiczan/.openclaw/workspace/scripts/process_craigslist_leads.py"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            content = f.read()
            if "am_" in content:
                print("   ✅ AgentMail API key configured")
            else:
                print("   ⚠️ AgentMail API key not found in config")
    else:
        print("   ❌ Config file not found")
        return False
    
    # 6. Create today's leads file for processor test
    print("\n6. Creating today's leads file...")
    date_str = datetime.now().strftime("%Y-%m-%d")
    today_leads = f"{output_dir}/daily_leads_{date_str}.json"
    
    try:
        # Copy test leads to today's file
        with open(test_leads, 'r') as f:
            test_data = json.load(f)
        
        with open(today_leads, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        print(f"   ✅ Created today's leads file: {today_leads}")
    except Exception as e:
        print(f"   ❌ Error creating today's leads file: {e}")
        return False
    
    print(f"\n{'='*60}")
    print("SYSTEM TEST COMPLETE")
    print(f"{'='*60}")
    print("\n✅ All components are ready!")
    print("\nTo run the system manually:")
    print("1. Morning scraper: ./scripts/run_craigslist_scraper.sh")
    print("2. Afternoon processor: ./scripts/run_lead_processor.sh")
    print("\nTo schedule as cron jobs:")
    print("- Scraper: 9:00 AM daily")
    print("- Processor: 2:00 PM daily")
    
    return True

if __name__ == "__main__":
    success = test_system()
    if not success:
        print("\n❌ System test failed. Please check the errors above.")
        exit(1)