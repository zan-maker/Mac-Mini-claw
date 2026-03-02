#!/usr/bin/env python3
"""
Defense Sector Outreach Report - 2026-03-02
AgentMail API Failure - Documenting intended outreach
"""

import json
from datetime import datetime
from pathlib import Path

# Defense Companies (Top 10)
defense_companies = [
    {"name": "Shield AI", "sector": "AI & Autonomous Systems", "email": "contact@shield.ai", "priority": "HIGH"},
    {"name": "Anduril Industries", "sector": "Autonomous Systems & Counter-Drone", "email": "contact@anduril.com", "priority": "HIGH"},
    {"name": "Skydio", "sector": "Autonomous Drones", "email": "contact@skydio.com", "priority": "HIGH"},
    {"name": "Chaos Industries", "sector": "Defense Manufacturing", "email": "contact@chaosindustries.com", "priority": "HIGH"},
    {"name": "Epirus", "sector": "Counter-Drone (C-UAS)", "email": "contact@epirusinc.com", "priority": "HIGH"},
    {"name": "Onebrief", "sector": "Defense Data Analytics / ISR", "email": "contact@onebrief.com", "priority": "MEDIUM"},
    {"name": "Hidden Level", "sector": "Counter-Drone / Surveillance", "email": "contact@hiddenlevel.com", "priority": "MEDIUM"},
    {"name": "Rebellion Defense", "sector": "AI & Defense Software", "email": "contact@rebelliondefense.com", "priority": "MEDIUM"},
    {"name": "Palantir Technologies", "sector": "Defense Data Analytics", "email": "partnerships@palantir.com", "priority": "MEDIUM"},
    {"name": "Astranis", "sector": "Space-Based Defense", "email": "contact@astranis.com", "priority": "MEDIUM"}
]

# PE/VC Investors (Top 5)
investors = [
    {"name": "General Catalyst", "email": "india@generalcatalyst.com", "priority": "HIGH"},
    {"name": "Lightspeed Venture Partners", "email": "india@lightspeedvp.com", "priority": "HIGH"},
    {"name": "Accel Partners", "email": "india@accel.com", "priority": "HIGH"},
    {"name": "BEENEXT", "email": "contact@beenext.com", "priority": "HIGH"},
    {"name": "Vertex Ventures", "email": "contact@vertexventures.com", "priority": "MEDIUM"}
]

def create_discord_report():
    """Create Discord-friendly report"""
    
    report = []
    report.append("🚨 **Defense Sector Outreach - 2026-03-02**")
    report.append("")
    report.append("❌ **STATUS: AgentMail API Failure**")
    report.append("")
    report.append("**Issue:** AgentMail API returning 403 Forbidden on all endpoints")
    report.append("**Impact:** Unable to send 15 planned outreach emails")
    report.append("")
    report.append("**Intended Outreach:**")
    report.append(f"• **10 Defense Companies** (US/UK/EU)")
    report.append(f"• **5 PE/VC Funds** (Asia/India)")
    report.append(f"• **Total:** 15 emails")
    report.append("")
    report.append("**Top Companies Ready to Contact:**")
    for i, company in enumerate(defense_companies[:5], 1):
        report.append(f"{i}. {company['name']} ({company['sector']})")
    report.append("")
    report.append("**Top Investors Ready to Contact:**")
    for i, investor in enumerate(investors[:3], 1):
        report.append(f"{i}. {investor['name']}")
    report.append("")
    report.append("**Email Templates Ready:**")
    report.append("• Defense Companies: Strategic Partnership outreach")
    report.append("• Investors: Drone Technology Platform opportunity")
    report.append("")
    report.append("**From:** Zander@agentmail.to")
    report.append("**CC:** sam@impactquadrant.info")
    report.append("")
    report.append("**Action Required:**")
    report.append("1. Check AgentMail API status")
    report.append("2. Verify API key validity")
    report.append("3. Test with alternative email method (Gmail SMTP)")
    report.append("4. Resume outreach once fixed")
    report.append("")
    report.append(f"**Report Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
    
    return "\n".join(report)

def main():
    """Main execution"""
    
    print("=" * 60)
    print("DEFENSE SECTOR OUTREACH - API FAILURE REPORT")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create Discord report
    discord_report = create_discord_report()
    print(discord_report)
    
    # Save full results
    results = {
        "timestamp": datetime.now().isoformat(),
        "status": "FAILED",
        "error": "AgentMail API 403 Forbidden",
        "intended_recipients": {
            "companies": defense_companies,
            "investors": investors
        },
        "summary": {
            "total_intended": 15,
            "companies_intended": 10,
            "investors_intended": 5,
            "emails_sent": 0,
            "emails_failed": 15
        }
    }
    
    results_file = Path("defense-leads/outreach-results-2026-03-02.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print()
    print("=" * 60)
    print(f"📁 Results saved to: {results_file}")
    
    # Save Discord report
    discord_file = Path("defense-leads/discord-report-2026-03-02.md")
    with open(discord_file, 'w') as f:
        f.write(discord_report)
    
    print(f"📝 Discord report saved to: {discord_file}")
    
    return discord_report

if __name__ == "__main__":
    main()
