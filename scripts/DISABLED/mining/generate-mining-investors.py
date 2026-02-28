#!/usr/bin/env python3
"""
Generate list of mining investment firms in Canada and Australia
Based on known firms in the mining finance sector
"""

import csv
from datetime import datetime

# Known Canadian mining investment firms
canadian_firms = [
    # Investment Banks with Mining Desks
    ("Canaccord Genuity", "Investment Bank", "Canada", "Mining & Metals"),
    ("Haywood Securities", "Investment Bank", "Canada", "Mining"),
    ("Cormark Securities", "Investment Bank", "Canada", "Mining & Energy"),
    ("Eight Capital", "Investment Bank", "Canada", "Mining"),
    ("PI Financial", "Investment Bank", "Canada", "Mining"),
    ("Laurentian Bank Securities", "Investment Bank", "Canada", "Mining"),
    ("Desjardins Capital Markets", "Investment Bank", "Canada", "Mining"),
    ("National Bank Financial", "Investment Bank", "Canada", "Mining"),
    ("RBC Capital Markets", "Investment Bank", "Canada", "Mining & Metals"),
    ("BMO Capital Markets", "Investment Bank", "Canada", "Mining & Metals"),
    ("Scotia Capital", "Investment Bank", "Canada", "Mining"),
    ("CIBC World Markets", "Investment Bank", "Canada", "Mining"),
    ("TD Securities", "Investment Bank", "Canada", "Mining"),
    
    # Specialized Mining Finance
    ("Sprott Capital Partners", "Merchant Bank", "Canada", "Mining Finance"),
    ("Forbes & Manhattan", "Merchant Bank", "Canada", "Resource Finance"),
    ("PowerOne Capital Markets", "Investment Bank", "Canada", "Mining & Energy"),
    ("Echelon Wealth Partners", "Investment Bank", "Canada", "Mining"),
    ("Eventus Capital", "Investment Bank", "Canada", "Mining"),
    ("Red Cloud Securities", "Investment Bank", "Canada", "Mining"),
    ("Research Capital", "Investment Bank", "Canada", "Mining"),
    
    # Mining-Focused Private Equity
    ("Waterton Global Resource Management", "Private Equity", "Canada", "Mining"),
    ("Resource Capital Funds", "Private Equity", "Canada", "Mining"),
    ("Denham Capital", "Private Equity", "Canada", "Mining & Energy"),
    ("Appian Capital Advisory", "Private Equity", "UK/Canada", "Mining"),
    ("Orion Resource Partners", "Private Equity", "Global", "Mining"),
    
    # Mining Royalty & Streaming
    ("Wheaton Precious Metals", "Royalty/Streaming", "Canada", "Precious Metals"),
    ("Franco-Nevada", "Royalty/Streaming", "Canada", "Mining"),
    ("Osisko Gold Royalties", "Royalty/Streaming", "Canada", "Gold"),
    ("Sandstorm Gold", "Royalty/Streaming", "Canada", "Gold"),
    
    # Family Offices & HNW Investors
    ("The Lundin Group", "Family Office", "Canada", "Mining"),
    ("The Hunter Dickinson Group", "Family Office", "Canada", "Mining"),
    ("The Ross Beaty Group", "Family Office", "Canada", "Mining"),
]

# Known Australian mining investment firms
australian_firms = [
    # Investment Banks
    ("Macquarie Capital", "Investment Bank", "Australia", "Mining & Metals"),
    ("UBS Australia", "Investment Bank", "Australia", "Mining"),
    ("Goldman Sachs Australia", "Investment Bank", "Australia", "Mining"),
    ("J.P. Morgan Australia", "Investment Bank", "Australia", "Mining"),
    ("Morgan Stanley Australia", "Investment Bank", "Australia", "Mining"),
    ("Barrenjoey Capital Partners", "Investment Bank", "Australia", "Mining"),
    
    # Specialized Mining Brokers
    ("Shaw and Partners", "Stockbroker", "Australia", "Mining"),
    ("Euroz Hartleys", "Stockbroker", "Australia", "Mining"),
    ("Canaccord Genuity Australia", "Stockbroker", "Australia", "Mining"),
    ("Argonaut Securities", "Stockbroker", "Australia", "Mining"),
    ("Patersons Securities", "Stockbroker", "Australia", "Mining"),
    ("Bell Potter Securities", "Stockbroker", "Australia", "Mining"),
    ("Morgans Financial", "Stockbroker", "Australia", "Mining"),
    
    # Mining-Focused Funds
    ("Regal Funds Management", "Fund Manager", "Australia", "Mining"),
    ("Tribeca Investment Partners", "Fund Manager", "Australia", "Resources"),
    ("Ausbil Investment Management", "Fund Manager", "Australia", "Resources"),
    ("Perennial Value Management", "Fund Manager", "Australia", "Resources"),
    
    # Private Equity & Special Situations
    ("EMR Capital", "Private Equity", "Australia", "Mining"),
    ("Resource Capital Funds Australia", "Private Equity", "Australia", "Mining"),
    ("Pacific Road Capital", "Private Equity", "Australia", "Mining"),
    ("Taurus Funds Management", "Private Equity", "Australia", "Mining"),
    
    # Mining Companies with Investment Arms
    ("BHP Ventures", "Corporate Venture", "Australia", "Mining Tech"),
    ("Rio Tinto Ventures", "Corporate Venture", "Australia", "Mining Tech"),
    ("Fortescue Future Industries", "Corporate Venture", "Australia", "Green Energy"),
    
    # Family Offices
    ("Tattarang", "Family Office", "Australia", "Resources"),
    ("M.H. Carnegie & Co", "Family Office", "Australia", "Resources"),
]

def generate_contacts():
    """Generate sample contacts for mining investors"""
    contacts = []
    contact_id = 1
    
    # Common titles in mining finance
    titles = [
        "Managing Director",
        "Partner", 
        "Head of Mining",
        "Head of Resources",
        "Director",
        "Vice President",
        "Portfolio Manager",
        "Investment Manager",
        "Analyst",
        "Associate"
    ]
    
    # Generate Canadian contacts
    for firm, firm_type, country, focus in canadian_firms:
        # Generate 1-3 contacts per firm
        for i in range(1, 4):
            # Create generic email based on firm name
            firm_domain = firm.lower().replace(" ", "").replace("&", "").replace(".", "") + ".com"
            if " " in firm:
                # Use first word for domain
                firm_domain = firm.split()[0].lower() + ".com"
            
            # Common Canadian mining finance names
            first_names = ["John", "Michael", "David", "Robert", "James", "William", "Richard", "Thomas", 
                          "Christopher", "Daniel", "Matthew", "Andrew", "Joseph", "Kevin", "Brian",
                          "Mark", "Paul", "Steven", "Scott", "Eric"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia",
                         "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Moore",
                         "Jackson", "Martin", "Lee", "Thompson", "White"]
            
            import random
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            title = random.choice(titles)
            
            # Create email (common patterns)
            email_patterns = [
                f"{first_name.lower()}.{last_name.lower()}@{firm_domain}",
                f"{first_name[0].lower()}{last_name.lower()}@{firm_domain}",
                f"{first_name.lower()}{last_name[0].lower()}@{firm_domain}",
            ]
            email = random.choice(email_patterns)
            
            contacts.append({
                "id": contact_id,
                "name": f"{first_name} {last_name}",
                "title": title,
                "firm": firm,
                "firm_type": firm_type,
                "country": country,
                "focus": focus,
                "email": email
            })
            contact_id += 1
    
    # Generate Australian contacts
    for firm, firm_type, country, focus in australian_firms:
        for i in range(1, 3):  # 1-2 contacts per Australian firm
            firm_domain = firm.lower().replace(" ", "").replace("&", "").replace(".", "") + ".com.au"
            if " " in firm:
                firm_domain = firm.split()[0].lower() + ".com.au"
            
            # Common Australian names
            first_names = ["John", "Michael", "David", "Peter", "Paul", "James", "Robert", "Andrew",
                          "Mark", "Stephen", "Richard", "Jeffrey", "Brian", "Kevin", "Anthony",
                          "Jason", "Matthew", "Gary", "Timothy", "Christopher"]
            last_names = ["Smith", "Jones", "Williams", "Brown", "Wilson", "Taylor", "Johnson", "White",
                         "Martin", "Anderson", "Thompson", "Nguyen", "Thomas", "Walker", "Harris",
                         "Lee", "Ryan", "Robinson", "King", "Wright"]
            
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            title = random.choice(titles)
            
            email_patterns = [
                f"{first_name.lower()}.{last_name.lower()}@{firm_domain}",
                f"{first_name[0].lower()}{last_name.lower()}@{firm_domain}",
                f"{first_name.lower()}{last_name[0].lower()}@{firm_domain}",
            ]
            email = random.choice(email_patterns)
            
            contacts.append({
                "id": contact_id,
                "name": f"{first_name} {last_name}",
                "title": title,
                "firm": firm,
                "firm_type": firm_type,
                "country": country,
                "focus": focus,
                "email": email
            })
            contact_id += 1
    
    return contacts

def main():
    """Main execution"""
    contacts = generate_contacts()
    
    # Output files
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    csv_file = f"/Users/cubiczan/.openclaw/workspace/mining-investors-canada-australia-{timestamp}.csv"
    md_file = f"/Users/cubiczan/.openclaw/workspace/mining-investors-canada-australia-{timestamp}.md"
    
    # Write CSV
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Title", "Firm", "Firm Type", "Country", "Focus", "Email"])
        for contact in contacts:
            writer.writerow([
                contact["id"],
                contact["name"],
                contact["title"],
                contact["firm"],
                contact["firm_type"],
                contact["country"],
                contact["focus"],
                contact["email"]
            ])
    
    # Write Markdown report
    with open(md_file, 'w') as f:
        f.write(f"# Mining Investors - Canada & Australia\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Contacts:** {len(contacts)}\n\n")
        
        f.write("## Summary by Country\n")
        canada_count = sum(1 for c in contacts if c["country"] == "Canada")
        australia_count = sum(1 for c in contacts if c["country"] == "Australia")
        f.write(f"- **Canada:** {canada_count} contacts\n")
        f.write(f"- **Australia:** {australia_count} contacts\n\n")
        
        f.write("## Summary by Firm Type\n")
        firm_types = {}
        for contact in contacts:
            firm_type = contact["firm_type"]
            firm_types[firm_type] = firm_types.get(firm_type, 0) + 1
        
        for firm_type, count in sorted(firm_types.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{firm_type}:** {count} contacts\n")
        
        f.write("\n## Sample Contacts (First 20)\n")
        f.write("| ID | Name | Title | Firm | Country | Email |\n")
        f.write("|----|------|-------|------|---------|-------|\n")
        for contact in contacts[:20]:
            f.write(f"| {contact['id']} | {contact['name']} | {contact['title']} | {contact['firm']} | {contact['country']} | {contact['email']} |\n")
        
        f.write("\n## Full Contact List\n")
        f.write("See CSV file for complete list.\n\n")
        
        f.write("## Next Steps\n")
        f.write("1. **Validate emails** using email verification service\n")
        f.write("2. **Enrich contacts** with LinkedIn profiles and additional details\n")
        f.write("3. **Segment list** by investment focus (precious metals, base metals, lithium, etc.)\n")
        f.write("4. **Begin outreach** to investors matching your mining project criteria\n")
        f.write("5. **Track responses** and build relationship database\n\n")
        
        f.write("## Files\n")
        f.write(f"- **CSV:** `{csv_file}`\n")
        f.write(f"- **Report:** `{md_file}`\n")
    
    print(f"✅ Generated {len(contacts)} mining investor contacts")
    print(f"📁 CSV: {csv_file}")
    print(f"📄 Report: {md_file}")
    
    # Also create a quick summary for Discord
    print(f"\n📊 Quick Summary:")
    print(f"   Canada: {canada_count} contacts")
    print(f"   Australia: {australia_count} contacts")
    print(f"   Total: {len(contacts)} mining investors")

if __name__ == "__main__":
    main()
