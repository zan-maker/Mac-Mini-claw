# Supabase Setup - Leads Table

**Project:** https://utsqbuwkwsidvqvrodtf.supabase.co
**Dashboard:** https://supabase.com/dashboard

---

## Step 1: Create Leads Table

Go to: **SQL Editor** in Supabase Dashboard

Run this SQL:

```sql
-- Create leads table
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Contact info
  company_name TEXT,
  contact_name TEXT,
  email TEXT,
  phone TEXT,
  
  -- Qualification
  employee_count INTEGER,
  industry TEXT,
  challenge TEXT,
  
  -- Source tracking
  source TEXT DEFAULT 'unknown',
  campaign TEXT,
  
  -- Scoring
  qualification_score INTEGER DEFAULT 0,
  status TEXT DEFAULT 'new',
  
  -- Calculated fields
  estimated_savings INTEGER,
  potential_deal_value INTEGER
);

-- Enable Row Level Security
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- Allow public inserts (for forms)
CREATE POLICY "Allow public inserts" ON leads
  FOR INSERT TO anon
  WITH CHECK (true);

-- Allow public reads (optional - remove if you want private data)
CREATE POLICY "Allow public reads" ON leads
  FOR SELECT TO anon
  USING (true);

-- Create index on email for lookups
CREATE INDEX idx_leads_email ON leads(email);

-- Create index on created_at for sorting
CREATE INDEX idx_leads_created ON leads(created_at DESC);
```

---

## Step 2: Get Service Role Key

For full API access, get the service role key:

1. Go to: **Settings** → **API**
2. Copy: **service_role** key (secret)
3. Keep this secure - it has full database access

---

## Step 3: Test Connection

After creating the table:

```bash
# Insert a test lead
curl -X POST "https://utsqbuwkwsidvqvrodtf.supabase.co/rest/v1/leads" \
  -H "apikey: sb_publishable_H7oSoGx02K5ic0MlodC_ng_8DApe4FN" \
  -H "Authorization: Bearer sb_publishable_H7oSoGx02K5ic0MlodC_ng_8DApe4FN" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"company_name":"Test Company","email":"test@example.com","employee_count":100}'

# Get all leads
curl -s "https://utsqbuwkwsidvqvrodtf.supabase.co/rest/v1/leads" \
  -H "apikey: sb_publishable_H7oSoGx02K5ic0MlodC_ng_8DApe4FN" \
  -H "Authorization: Bearer sb_publishable_H7oSoGx02K5ic0MlodC_ng_8DApe4FN"
```

---

## Credentials

| Item | Value |
|------|-------|
| Project URL | `https://utsqbuwkwsidvqvrodtf.supabase.co` |
| Anon Key | `sb_publishable_H7oSoGx02K5ic0MlodC_ng_8DApe4FN` |
| Service Role | Get from dashboard (Settings → API) |

---

## Next Steps

1. ✅ Create account
2. 📋 Run SQL to create leads table
3. 📋 Get service role key
4. 📋 Test insert/select
5. 📋 Connect to n8n workflow

---

*Created: 2026-02-16*
