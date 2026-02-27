#!/usr/bin/env python3
import sys

try:
    import openai
    print("✅ openai module is available")
    print(f"openai version: {openai.__version__ if hasattr(openai, '__version__') else 'unknown'}")
except ImportError as e:
    print("❌ openai module is NOT available")
    print(f"Error: {e}")
    print("\nTo install openai, run:")
    print("python3 -m pip install --break-system-packages openai")
    
try:
    import pandas
    print("✅ pandas module is available")
    print(f"pandas version: {pandas.__version__}")
except ImportError as e:
    print("❌ pandas module is NOT available")
    print(f"Error: {e}")
    print("\nTo install pandas, run:")
    print("python3 -m pip install --break-system-packages pandas")

print(f"\nPython executable: {sys.executable}")
print(f"Python version: {sys.version}")