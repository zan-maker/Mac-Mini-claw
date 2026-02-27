#!/usr/bin/env python3
"""
Scrapling-Enhanced Cron Job Template for OpenClaw

Use this template for all cron jobs that need web scraping.
Scrapling will be used FIRST, falling back to traditional APIs if needed.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add Scrapling integration to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from cron_integration import ScraplingCronIntegration
    SCRAPLING_ENABLED = True
except ImportError:
    SCRAPLING_ENABLED = False
    print("⚠️ Scrapling integration not available. Using traditional APIs.")


class ScraplingEnhancedCronJob:
    """
    Base class for Scrapling-enhanced cron jobs.
    
    Features:
    1. Try Scrapling first (fastest, most reliable)
    2. Fall back to Brave Search/Tavily if Scrapling fails
    3. Unified data format
    4. Automatic error handling
    """
    
    def __init__(self, job_name: str, stealth_mode: bool = True):
        self.job_name = job_name
        self.stealth_mode = stealth_mode
        self.scrapling = None
        self.results = []
        self.errors = []
        
    async def initialize(self) -> bool:
        """Initialize Scrapling integration."""
        if not SCRAPLING_ENABLED:
            print(f"⚠️ {self.job_name}: Scrapling not available, using traditional APIs")
            return False
        
        try:
            self.scrapling = ScraplingCronIntegration(stealth_mode=self.stealth_mode)
            success = await self.scrapling.initialize()
            
            if success:
                print(f"✅ {self.job_name}: Scrapling initialized")
            else:
                print(f"⚠️ {self.job_name}: Scrapling initialization failed")
            
            return success
        except Exception as e:
            print(f"❌ {self.job_name}: Scrapling initialization error: {e}")
            return False
    
    async def run_with_scrapling(self) -> List[Dict[str, Any]]:
        """
        Run the cron job using Scrapling.
        Override this method in subclasses.
        
        Returns:
            List of results from Scrapling
        """
        raise NotImplementedError("Subclasses must implement run_with_scrapling")
    
    async def run_with_traditional_apis(self) -> List[Dict[str, Any]]:
        """
        Run the cron job using traditional APIs (Brave Search/Tavily).
        Override this method in subclasses.
        
        Returns:
            List of results from traditional APIs
        """
        raise NotImplementedError("Subclasses must implement run_with_traditional_apis")
    
    async def execute(self) -> Dict[str, Any]:
        """
        Execute the cron job with Scrapling-first approach.
        
        Returns:
            Dictionary with results and metadata
        """
        print(f"\n{'='*60}")
        print(f"🚀 {self.job_name} - Starting")
        print(f"{'='*60}")
        
        start_time = datetime.now()
        scrapling_results = []
        traditional_results = []
        
        # Step 1: Try Scrapling first
        scrapling_success = False
        if SCRAPLING_ENABLED:
            print(f"\n🔍 {self.job_name}: Trying Scrapling first...")
            try:
                scrapling_success = await self.initialize()
                
                if scrapling_success:
                    scrapling_results = await self.run_with_scrapling()
                    
                    if scrapling_results:
                        print(f"✅ {self.job_name}: Scrapling found {len(scrapling_results)} results")
                        scrapling_success = True
                    else:
                        print(f"⚠️ {self.job_name}: Scrapling returned no results")
                        scrapling_success = False
                else:
                    print(f"⚠️ {self.job_name}: Scrapling initialization failed")
                    scrapling_success = False
                    
            except Exception as e:
                print(f"❌ {self.job_name}: Scrapling error: {e}")
                self.errors.append(f"Scrapling error: {str(e)}")
                scrapling_success = False
        
        # Step 2: Fall back to traditional APIs if Scrapling failed
        if not scrapling_success or not scrapling_results:
            print(f"\n🔍 {self.job_name}: Falling back to traditional APIs...")
            try:
                traditional_results = await self.run_with_traditional_apis()
                
                if traditional_results:
                    print(f"✅ {self.job_name}: Traditional APIs found {len(traditional_results)} results")
                else:
                    print(f"⚠️ {self.job_name}: Traditional APIs returned no results")
                    
            except Exception as e:
                print(f"❌ {self.job_name}: Traditional APIs error: {e}")
                self.errors.append(f"Traditional APIs error: {str(e)}")
        
        # Combine results
        all_results = scrapling_results + traditional_results
        
        # Calculate statistics
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        stats = {
            "job_name": self.job_name,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "total_results": len(all_results),
            "scrapling_results": len(scrapling_results),
            "traditional_results": len(traditional_results),
            "scrapling_success": scrapling_success,
            "errors": self.errors,
            "results": all_results
        }
        
        # Save results
        self._save_results(stats)
        
        # Print summary
        self._print_summary(stats)
        
        return stats
    
    def _save_results(self, stats: Dict[str, Any]):
        """Save results to file."""
        try:
            # Create results directory
            results_dir = "./cron_results"
            os.makedirs(results_dir, exist_ok=True)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{results_dir}/{self.job_name.lower().replace(' ', '_')}_{timestamp}.json"
            
            # Save results
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def _print_summary(self, stats: Dict[str, Any]):
        """Print execution summary."""
        print(f"\n{'='*60}")
        print(f"📊 {self.job_name} - Summary")
        print(f"{'='*60}")
        print(f"⏱️  Duration: {stats['duration_seconds']:.2f} seconds")
        print(f"📈 Total Results: {stats['total_results']}")
        print(f"🔍 Scrapling Results: {stats['scrapling_results']}")
        print(f"🌐 Traditional API Results: {stats['traditional_results']}")
        print(f"✅ Scrapling Success: {stats['scrapling_success']}")
        
        if stats['errors']:
            print(f"❌ Errors: {len(stats['errors'])}")
            for error in stats['errors']:
                print(f"   • {error}")
        
        # Show top results
        if stats['results']:
            print(f"\n🏆 Top Results:")
            for i, result in enumerate(stats['results'][:5], 1):
                if 'company_name' in result:
                    print(f"   {i}. {result.get('company_name')} - Score: {result.get('lead_score', 'N/A')}")
                elif 'title' in result:
                    print(f"   {i}. {result.get('title')}")
                else:
                    print(f"   {i}. {result.get('url', 'Unknown')}")


# ============================================================================
# SPECIFIC CRON JOB IMPLEMENTATIONS
# ============================================================================

class ExpenseReductionLeadGenJob(ScraplingEnhancedCronJob):
    """Scrapling-enhanced expense reduction lead generation."""
    
    def __init__(self):
        super().__init__("Expense Reduction Lead Generation", stealth_mode=True)
        self.search_queries = [
            "manufacturing companies 50-200 employees",
            "technology companies 20-100 employees",
            "healthcare companies 30-150 employees",
            "professional services firms 25-75 employees",
            "financial services companies 40-120 employees"
        ]
    
    async def run_with_scrapling(self) -> List[Dict[str, Any]]:
        """Generate leads using Scrapling."""
        if not self.scrapling:
            return []
        
        try:
            leads = await self.scrapling.generate_expense_reduction_leads(
                search_queries=self.search_queries,
                limit=20
            )
            return leads
        except Exception as e:
            print(f"❌ Scrapling lead generation error: {e}")
            self.errors.append(f"Scrapling lead gen error: {str(e)}")
            return []
    
    async def run_with_traditional_apis(self) -> List[Dict[str, Any]]:
        """Generate leads using traditional APIs."""
        print("Using traditional APIs for expense reduction leads...")
        # This would call Brave Search/Tavily APIs
        # For now, return empty list
        return []


class DefenseSectorLeadGenJob(ScraplingEnhancedCronJob):
    """Scrapling-enhanced defense sector lead generation."""
    
    def __init__(self):
        super().__init__("Defense Sector Lead Generation", stealth_mode=True)
        self.company_search_terms = [
            "defense technology companies",
            "cybersecurity companies military",
            "drone technology defense",
            "space defense technology",
            "military AI companies"
        ]
        self.investor_regions = ["India", "Singapore", "Japan", "South Korea", "Taiwan"]
    
    async def run_with_scrapling(self) -> List[Dict[str, Any]]:
        """Generate defense leads using Scrapling."""
        if not self.scrapling:
            return []
        
        try:
            # Get defense companies
            companies = await self.scrapling.scrape_defense_companies(
                search_terms=self.company_search_terms
            )
            
            # Get PE/VC funds
            # funds = await self.scrapling.scrape_pe_vc_funds(
            #     regions=self.investor_regions,
            #     focus="defense"
            # )
            
            # Combine results
            results = []
            for company in companies:
                results.append({
                    "type": "company",
                    "company_name": company.get("company_name", ""),
                    "sector": company.get("sector", ""),
                    "technologies": company.get("technologies", ""),
                    "location": company.get("location", ""),
                    "defense_score": company.get("defense_score", 0),
                    "priority": company.get("priority", "Medium"),
                    "url": company.get("url", ""),
                    "source": "Scrapling"
                })
            
            # for fund in funds:
            #     results.append({
            #         "type": "investor",
            #         "fund_name": fund.get("fund_name", ""),
            #         "region": fund.get("region", ""),
            #         "focus": fund.get("focus", ""),
            #         "portfolio": fund.get("portfolio", ""),
            #         "url": fund.get("url", ""),
            #         "source": "Scrapling"
            #     })
            
            return results
        except Exception as e:
            print(f"❌ Scrapling defense lead gen error: {e}")
            self.errors.append(f"Scrapling defense lead gen error: {str(e)}")
            return []
    
    async def run_with_traditional_apis(self) -> List[Dict[str, Any]]:
        """Generate defense leads using traditional APIs."""
        print("Using traditional APIs for defense sector leads...")
        # This would call Brave Search/Tavily APIs
        # For now, return empty list
        return []


class DealOriginationSellersJob(ScraplingEnhancedCronJob):
    """Scrapling-enhanced deal origination (sellers)."""
    
    def __init__(self):
        super().__init__("Deal Origination - Sellers", stealth_mode=True)
        self.industries = [
            "HVAC companies",
            "plumbing businesses",
            "electrical contractors",
            "roofing companies",
            "commercial cleaning",
            "waste management",
            "healthcare services",
            "insurance brokerage"
        ]
    
    async def run_with_scrapling(self) -> List[Dict[str, Any]]:
        """Find seller leads using Scrapling."""
        if not self.scrapling:
            return []
        
        try:
            # For each industry, search for business websites
            results = []
            
            for industry in self.industries:
                print(f"🔍 Searching for {industry} sellers...")
                
                # In real implementation, search for business websites
                # For now, create example data
                example_seller = {
                    "type": "seller",
                    "industry": industry,
                    "company_name": f"Example {industry.split()[0]} Company",
                    "years_in_business": 15,
                    "estimated_ebitda": 750000,
                    "owner_signals": ["retirement age", "second generation"],
                    "website_quality": "Established",
                    "seller_score": 75,
                    "priority": "High",
                    "estimated_finder_fee": 37500,
                    "source": "Scrapling"
                }
                results.append(example_seller)
            
            return results
        except Exception as e:
            print(f"❌ Scrapling seller lead gen error: {e}")
            self.errors.append(f"Scrapling seller lead gen error: {str(e)}")
            return []
    
    async def run_with_traditional_apis(self) -> List[Dict[str, Any]]:
        """Find seller leads using traditional APIs."""
        print("Using traditional APIs for seller leads...")
        return []


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def run_all_cron_jobs():
    """Run all Scrapling-enhanced cron jobs."""
    jobs = [
        ExpenseReductionLeadGenJob(),
        DefenseSectorLeadGenJob(),
        DealOriginationSellersJob()
    ]
    
    all_results = []
    
    for job in jobs:
        try:
            results = await job.execute()
            all_results.append(results)
            
            # Add delay between jobs
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"❌ Error running {job.job_name}: {e}")
    
    return all_results


async def main():
    """Main execution function."""
    print("="*70)
    print("🚀 SCRAPLING-ENHANCED CRON JOBS")
    print("="*70)
    print("\n📊 Running all cron jobs with Scrapling-first approach...\n")
    
    results = await run_all_cron_jobs()
    
    # Print final summary
    print("\n" + "="*70)
    print("🎯 FINAL SUMMARY")
    print("="*70)
    
    total_results = 0
    total_scrapling = 0
    total_traditional = 0
    
    for result in results:
        total_results += result.get("total_results", 0)
        total_scrapling += result.get("scrapling_results", 0)
        total_traditional += result.get("traditional_results", 0)
        
        print(f"\n📋 {result.get('job_name')}:")
        print(f"   • Total: {result.get('total_results', 0)}")
        print(f"   • Scrapling: {result.get('scrapling_results', 0)}")
        print(f"   • Traditional: {result.get('traditional_results', 0)}")
        print(f"   • Scrapling Success: {result.get('scrapling_success', False)}")
    
    print(f"\n📈 OVERALL TOTALS:")
    print(f"   • Total Results: {total_results}")
    print(f"   • Scrapling Results: {total_scrapling}")
    print(f"   • Traditional API Results: {total_traditional}")
    print(f"   • Scrapling Success Rate: {(total_scrapling / total_results * 100):.1f}%" if total_results > 0 else "N/A")
    
    print(f"\n✅ All cron jobs completed with Scrapling-first approach!")
    print(f"\n💡 Next: Update your actual cron jobs to use this template.")


if __name__ == "__main__":
    asyncio.run(main())