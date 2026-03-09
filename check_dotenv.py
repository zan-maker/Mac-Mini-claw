#!/usr/bin/env python3
import sys
try:
    import dotenv
    print('✅ python-dotenv is installed')
    sys.exit(0)
except ImportError:
    print('❌ python-dotenv not installed')
    sys.exit(1)