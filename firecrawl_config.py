# Firecrawl Configuration
import os

FIRECRAWL_API_KEY = "fc-3ba22d7b419a490da37f7fb0255ef581"

# Set environment variable
os.environ["FIRECRAWL_API_KEY"] = FIRECRAWL_API_KEY

print(f"✅ Firecrawl configured with API key: {FIRECRAWL_API_KEY[:10]}...")
