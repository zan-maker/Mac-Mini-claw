#!/usr/bin/env python3
"""
Run Scrapling-based expense reduction lead generation.
"""

import asyncio
import sys
import json
from datetime import datetime
from pathlib import Path

# Add Scrapling integration to path
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scrapling-integration')

try:
    from cron_integration import ScraplingCronIntegration
    
    async def main():
        print("=" * 60)
        print("🚀 Scrapling-First Expense Reduction Lead Generation")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Initialize Scrapling
        scrapling = ScraplingCronIntegration(stealth_mode=True)
        success = await scrapling.initialize()
        
        if success:
            print("✅ Scrapling initialized successfully\n")
            
            # Define search queries
            search_queries = [
                "manufacturing companies 50-200 employees",
                "technology companies 20-100 employees",
                "healthcare companies 30-150 employees",
                "professional services firms 25-75 employees",
                "financial services companies 40-120 employees"
            ]
            
            # Generate leads
            print(f"🔍 Generating leads with Scrapling...\n")
            leads = await scrapling.generate_expense_reduction_leads(
                search_queries=search_queries,
                limit=20
            )
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            if leads:
                print(f"\n✅ Scrapling generated {len(leads)} leads in {processing_time:.2f} seconds")
                
                # Save results
                output = {
                    "success": True,
                    "source": "scrapling",
                    "leads": leads,
                    "total_leads": len(leads),
                    "processing_time_seconds": processing_time,
                    "generated_at": start_time.isoformat()
                }
                
                print(json.dumps(output, indent=2))
                return output
            else:
                print(f"\n⚠️ Scrapling returned no leads after {processing_time:.2f} seconds")
                return {
                    "success": False,
                    "source": "scrapling",
                    "error": "No leads generated",
                    "processing_time_seconds": processing_time
                }
        else:
            print("❌ Scrapling initialization failed")
            return {
                "success": False,
                "source": "scrapling",
                "error": "Initialization failed"
            }
    
    # Run the async main function
    result = asyncio.run(main())
    
except ImportError as e:
    print(f"⚠️ Scrapling import failed: {e}")
    print(json.dumps({
        "success": False,
        "source": "scrapling",
        "error": f"Import failed: {str(e)}"
    }))
except Exception as e:
    print(f"❌ Scrapling error: {e}")
    print(json.dumps({
        "success": False,
        "source": "scrapling",
        "error": str(e)
    }))
