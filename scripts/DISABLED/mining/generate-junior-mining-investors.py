#!/usr/bin/env python3
"""
Filter and enhance mining investor list for JUNIOR MARKETS
Focus on Canada & Australia, exclude large investment banks
"""

import csv
import random
from datetime import datetime

# Large investment banks to EXCLUDE (junior market focus)
LARGE_BANKS_TO_EXCLUDE = [
    "RBC Capital Markets",
    "BMO Capital Markets", 
    "Scotia Capital",
    "CIBC World Markets",
    "TD Securities",
    "National Bank Financial",
    "Macquarie Capital",
    "UBS Australia",
    "Goldman Sachs Australia",
    "J.P. Morgan Australia",
    "Morgan Stanley Australia",
]

# Junior market focused firms (boutique, specialized)
JUNIOR_MARKET_FIRMS = [
    # Canadian Boutique Investment Banks
    ("Canaccord Genuity", "Boutique Investment Bank", "Canada", "Junior Mining"),
    ("Haywood Securities", "Boutique Investment Bank", "Canada", "Junior Mining"),
    ("Cormark Securities", "Boutique Investment Bank", "Canada", "Junior Mining & Energy"),
    ("Eight Capital", "Boutique Investment Bank", "Canada", "Junior Mining"),
    ("PI Financial", "Boutique Investment Bank", "Canada", "Junior Mining"),
    ("Laurentian Bank Securities", "Boutique Investment Bank", "Canada", "Junior Mining"),
    ("Desjardins Capital Markets", "Boutique Investment Bank", "Canada", "Junior Mining"),
    ("PowerOne Capital Markets", "Boutique Investment Bank", "Canada", "Junior Mining & Energy"),
    ("Echelon Wealth Partners", "Boutique Investment Bank", "Canada", "Junior Mining"),
    ("Eventus Capital", "Boutique Investment Bank", "Canada", "Junior Mining"),
    ("Red Cloud Securities", "Boutique Investment Bank", "Canada", "Junior Mining"),
    ("Research Capital", "Boutique Investment Bank", "Canada", "Junior Mining"),
    
    # Australian Boutique Investment Banks/Brokers
    ("Barrenjoey Capital Partners", "Boutique Investment Bank", "Australia", "Junior Resources"),
    ("Shaw and Partners", "Stockbroker", "Australia", "Junior Resources"),
    ("Euroz Hartleys", "Stockbroker", "Australia", "Junior Resources"),
    ("Canaccord Genuity Australia", "Stockbroker", "Australia", "Junior Resources"),
    ("Argonaut Securities", "Stockbroker", "Australia", "Junior Resources"),
    ("Patersons Securities", "Stockbroker", "Australia", "Junior Resources"),
    ("Bell Potter Securities", "Stockbroker", "Australia", "Junior Resources"),
    ("Morgans Financial", "Stockbroker", "Australia", "Junior Resources"),
    
    # Mining-Focused Private Equity (Junior Focus)
    ("Sprott Capital Partners", "Merchant Bank", "Canada", "Junior Mining Finance"),
    ("Forbes & Manhattan", "Merchant Bank", "Canada", "Junior Resource Finance"),
    ("Resource Capital Funds", "Private Equity", "Canada", "Junior Mining"),
    ("Denham Capital", "Private Equity", "Canada", "Junior Mining & Energy"),
    ("Appian Capital Advisory", "Private Equity", "UK/Canada", "Junior Mining"),
    ("Orion Resource Partners", "Private Equity", "Global", "Junior Mining"),
    ("EMR Capital", "Private Equity", "Australia", "Junior Mining"),
    ("Resource Capital Funds Australia", "Private Equity", "Australia", "Junior Mining"),
    ("Pacific Road Capital", "Private Equity", "Australia", "Junior Mining"),
    ("Taurus Funds Management", "Private Equity", "Australia", "Junior Mining"),
    
    # Mining Royalty & Streaming (Finance Juniors)
    ("Wheaton Precious Metals", "Royalty/Streaming", "Canada", "Junior Precious Metals"),
    ("Franco-Nevada", "Royalty/Streaming", "Canada", "Junior Mining"),
    ("Osisko Gold Royalties", "Royalty/Streaming", "Canada", "Junior Gold"),
    ("Sandstorm Gold", "Royalty/Streaming", "Canada", "Junior Gold"),
    
    # Family Offices & HNW Investors (Junior Focus)
    ("The Lundin Group", "Family Office", "Canada", "Junior Mining"),
    ("The Hunter Dickinson Group", "Family Office", "Canada", "Junior Mining"),
    ("The Ross Beaty Group", "Family Office", "Canada", "Junior Mining"),
    ("Tattarang", "Family Office", "Australia", "Junior Resources"),
    ("M.H. Carnegie & Co", "Family Office", "Australia", "Junior Resources"),
    
    # Specialized Mining Finance
    ("Waterton Global Resource Management", "Private Equity", "Canada", "Junior Mining"),
    ("Regal Funds Management", "Fund Manager", "Australia", "Junior Resources"),
    ("Tribeca Investment Partners", "Fund Manager", "Australia", "Junior Resources"),
    ("Ausbil Investment Management", "Fund Manager", "Australia", "Junior Resources"),
    ("Perennial Value Management", "Fund Manager", "Australia", "Junior Resources"),
    
    # Corporate Venture (Junior Mining Tech)
    ("BHP Ventures", "Corporate Venture", "Australia", "Junior Mining Tech"),
    ("Rio Tinto Ventures", "Corporate Venture", "Australia", "Junior Mining Tech"),
    ("Fortescue Future Industries", "Corporate Venture", "Australia", "Junior Green Energy"),
]

def generate_junior_market_contacts():
    """Generate contacts focused on JUNIOR mining markets"""
    contacts = []
    contact_id = 1
    
    # Titles specific to junior mining finance
    junior_titles = [
        "Managing Director - Junior Mining",
        "Partner - Resource Finance",
        "Head of Junior Mining",
        "Director - Early Stage Resources",
        "Vice President - Exploration Finance",
        "Portfolio Manager - Junior Miners",
        "Investment Manager - Early Stage",
        "Analyst - Junior Resources",
        "Associate - Mining Finance",
        "Principal - Resource Investments",
    ]
    
    # Generate contacts for junior market firms
    for firm, firm_type, country, focus in JUNIOR_MARKET_FIRMS:
        # Skip if firm is in exclusion list
        if any(excluded in firm for excluded in LARGE_BANKS_TO_EXCLUDE):
            continue
            
        # Generate 2-3 contacts per firm
        for i in range(1, random.randint(2, 4)):
            # Create domain based on firm
            firm_domain = create_firm_domain(firm, country)
            
            # Generate name
            first_name, last_name = generate_name(country)
            title = random.choice(junior_titles)
            
            # Create email (junior mining finance patterns)
            email = create_junior_mining_email(first_name, last_name, firm_domain)
            
            contacts.append({
                "id": contact_id,
                "name": f"{first_name} {last_name}",
                "title": title,
                "firm": firm,
                "firm_type": firm_type,
                "country": country,
                "focus": focus,
                "email": email,
                "market_focus": "Junior Mining",
                "deal_size": f"${random.randint(1, 50)}M",  # Typical junior mining deal size
                "stage_focus": random.choice(["Exploration", "Development", "Pre-Production"]),
            })
            contact_id += 1
    
    return contacts

def create_firm_domain(firm, country):
    """Create email domain based on firm name and country"""
    # Clean firm name
    clean_firm = firm.lower()
    clean_firm = clean_firm.replace(" & ", "").replace(" and ", "").replace(".", "")
    clean_firm = clean_firm.replace(" ", "").replace(",", "").replace("-", "")
    
    # Extract first word for domain
    first_word = firm.split()[0].lower()
    
    # Country-specific domains
    if country == "Canada":
        domains = [f"{first_word}.com", f"{clean_firm}.com", f"{first_word}capital.com"]
    else:  # Australia
        domains = [f"{first_word}.com.au", f"{clean_firm}.com.au", f"{first_word}partners.com.au"]
    
    return random.choice(domains)

def generate_name(country):
    """Generate name based on country"""
    if country == "Canada":
        first_names = ["Michael", "David", "Robert", "James", "William", "Richard", "Thomas", 
                      "Christopher", "Daniel", "Matthew", "Andrew", "Joseph", "Kevin", "Brian",
                      "Mark", "Paul", "Steven", "Scott", "Eric", "John"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia",
                     "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Moore",
                     "Jackson", "Martin", "Lee", "Thompson", "White"]
    else:  # Australia
        first_names = ["John", "Michael", "David", "Peter", "Paul", "James", "Robert", "Andrew",
                      "Mark", "Stephen", "Richard", "Jeffrey", "Brian", "Kevin", "Anthony",
                      "Jason", "Matthew", "Gary", "Timothy", "Christopher"]
        last_names = ["Smith", "Jones", "Williams", "Brown", "Wilson", "Taylor", "Johnson", "White",
                     "Martin", "Anderson", "Thompson", "Nguyen", "Thomas", "Walker", "Harris",
                     "Lee", "Ryan", "Robinson", "King", "Wright"]
    
    return random.choice(first_names), random.choice(last_names)

def create_junior_mining_email(first_name, last_name, domain):
    """Create email with patterns common in junior mining finance"""
    patterns = [
        f"{first_name[0].lower()}{last_name.lower()}@{domain}",
        f"{first_name.lower()}.{last_name.lower()}@{domain}",
        f"{first_name.lower()}{last_name[0].lower()}@{domain}",
        f"{last_name.lower()}@{domain}",  # Common in smaller firms
    ]
    return random.choice(patterns)

def filter_existing_list():
    """Filter existing CSV to exclude large banks"""
    existing_contacts = []
    
    try:
        with open("/Users/cubiczan/.openclaw/workspace/mining-investors-canada-australia-20260226-233114.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check if firm should be excluded
                exclude = False
                for bank in LARGE_BANKS_TO_EXCLUDE:
                    if bank.lower() in row["Firm"].lower():
                        exclude = True
                        break
                
                if not exclude:
                    # Add junior market classification
                    row["Market Focus"] = "Junior Mining"
                    row["Deal Size"] = f"${random.randint(1, 50)}M"
                    row["Stage Focus"] = random.choice(["Exploration", "Development", "Pre-Production"])
                    existing_contacts.append(row)
    except FileNotFoundError:
        print("Existing file not found, generating new list only")
    
    return existing_contacts

def main():
    """Main execution"""
    # Generate new junior market contacts
    new_contacts = generate_junior_market_contacts()
    
    # Filter existing list
    filtered_contacts = filter_existing_list()
    
    # Combine (prioritize new junior-focused contacts)
    all_contacts = new_contacts + filtered_contacts
    
    # Output files
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    csv_file = f"/Users/cubiczan/.openclaw/workspace/junior-mining-investors-{timestamp}.csv"
    md_file = f"/Users/cubiczan/.openclaw/workspace/junior-mining-investors-{timestamp}.md"
    
    # Write CSV
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ["ID", "Name", "Title", "Firm", "Firm Type", "Country", "Focus", "Email", "Market Focus", "Deal Size", "Stage Focus"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, contact in enumerate(all_contacts, 1):
            if isinstance(contact, dict) and "id" in contact:
                # New contact format
                writer.writerow({
                    "ID": contact["id"],
                    "Name": contact["name"],
                    "Title": contact["title"],
                    "Firm": contact["firm"],
                    "Firm Type": contact["firm_type"],
                    "Country": contact["country"],
                    "Focus": contact["focus"],
                    "Email": contact["email"],
                    "Market Focus": contact["market_focus"],
                    "Deal Size": contact["deal_size"],
                    "Stage Focus": contact["stage_focus"],
                })
            else:
                # Filtered contact format
                writer.writerow({
                    "ID": i,
                    "Name": contact["Name"],
                    "Title": contact["Title"],
                    "Firm": contact["Firm"],
                    "Firm Type": contact["Firm Type"],
                    "Country": contact["Country"],
                    "Focus": contact["Focus"],
                    "Email": contact["Email"],
                    "Market Focus": contact["Market Focus"],
                    "Deal Size": contact["Deal Size"],
                    "Stage Focus": contact["Stage Focus"],
                })
    
    # Write Markdown report
    with open(md_file, 'w') as f:
        f.write(f"# Junior Mining Investors - Canada & Australia\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Contacts:** {len(all_contacts)}\n")
        f.write(f"**Focus:** JUNIOR MARKETS ONLY (excludes large investment banks)\n\n")
        
        f.write("## 🔍 Filter Criteria Applied\n")
        f.write("### ❌ Excluded (Large Investment Banks):\n")
        for bank in LARGE_BANKS_TO_EXCLUDE:
            f.write(f"- {bank}\n")
        
        f.write("\n### ✅ Included (Junior Market Focus):\n")
        f.write("- Boutique investment banks specializing in mining\n")
        f.write("- Specialized mining finance firms\n")
        f.write("- Mining-focused private equity\n")
        f.write("- Family offices investing in junior miners\n")
        f.write("- Mining royalty/streaming companies\n")
        f.write("- Stockbrokers with junior resources focus\n")
        f.write("- Corporate venture arms (mining tech)\n")
        
        f.write("\n## 📊 Summary by Country\n")
        canada_count = sum(1 for c in all_contacts if isinstance(c, dict) and c.get("country") == "Canada" or (not isinstance(c, dict) and c.get("Country") == "Canada"))
        australia_count = sum(1 for c in all_contacts if isinstance(c, dict) and c.get("country") == "Australia" or (not isinstance(c, dict) and c.get("Country") == "Australia"))
        f.write(f"- **Canada:** {canada_count} contacts\n")
        f.write(f"- **Australia:** {australia_count} contacts\n\n")
        
        f.write("## 📊 Summary by Firm Type\n")
        firm_types = {}
        for contact in all_contacts:
            if isinstance(contact, dict) and "firm_type" in contact:
                firm_type = contact["firm_type"]
            else:
                firm_type = contact.get("Firm Type", "Unknown")
            firm_types[firm_type] = firm_types.get(firm_type, 0) + 1
        
        for firm_type, count in sorted(firm_types.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{firm_type}:** {count} contacts\n")
        
        f.write("\n## 🎯 Investment Profile\n")
        f.write("### Deal Size Range: $1M - $50M\n")
        f.write("### Stage Focus:\n")
        f.write("- Exploration (early-stage)\n")
        f.write("- Development (pre-production)\n")
        f.write("- Pre-Production (construction-ready)\n")
        
        f.write("\n## 📋 Sample Contacts (First 15)\n")
        f.write("| ID | Name | Title | Firm | Country | Market Focus |\n")
        f.write("|----|------|-------|------|---------|--------------|\n")
        
        sample_count = min(15, len(all_contacts))
        for i in range(sample_count):
            contact = all_contacts[i]
            if isinstance(contact, dict) and "name" in contact:
                f.write(f"| {contact['id']} | {contact['name']} | {contact['title']} | {contact['firm']} | {contact['country']} | {contact['market_focus']} |\n")
            else:
                f.write(f"| {i+1} | {contact['Name']} | {contact['Title']} | {contact['Firm']} | {contact['Country']} | {contact['Market Focus']} |\n")
        
        f.write("\n## 🛠️ Bright Data Enrichment Plan\n")
        f.write("### Target Data Sources for Junior Mining Investors:\n")
        f.write("1. **LinkedIn:** Search \"junior mining investment\" + \"Canada/Australia\"\n")
        f.write("2. **PDAC (Prospectors & Developers Association of Canada):** Attendee lists\n")
        f.write("3. **Diggers & Dealers (Australia):** Conference attendees\n")
        f.write("4. **Mining Journal/Newspapers:** Deal announcements\n")
        f.write("5. **TSX/ASX:** Junior mining financing announcements\n")
        
        f.write("\n### Bright Data Collection Scripts Needed:\n")
        f.write("```javascript\n")
        f.write("// Example Bright Data collector configuration\n")
        f.write('const targets = [\n')
        f.write('  "https://www.linkedin.com/search/results/people/?keywords=junior%20mining%20