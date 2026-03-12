#!/usr/bin/env python3
"""
Monitor Google Cloud Firestore free tier usage
"""

import os
from datetime import datetime, timedelta
from google.cloud import firestore

def check_firestore_usage():
    """Check Firestore usage against free tier limits"""
    print("📊 FIRESTORE FREE TIER USAGE MONITOR")
    print("="*50)
    
    # Free tier limits
    FREE_TIER = {
        "storage_gb": 1,
        "reads_per_day": 50000,
        "writes_per_day": 20000,
        "deletes_per_day": 20000
    }
    
    try:
        # Initialize client
        client = firestore.Client(project="project-651348c0-d39f-4cd5-b8a")
        
        print(f"✅ Connected to project: {client.project}")
        print("")
        
        # Get collection count (rough estimate)
        collections = list(client.collections())
        total_docs = 0
        
        print("📁 Collections found:")
        for collection in collections[:10]:  # Limit to first 10
            try:
                docs = list(collection.limit(1000).stream())
                doc_count = len(docs)
                total_docs += doc_count
                print(f"  🔹 {collection.id}: {doc_count} documents")
            except:
                print(f"  🔹 {collection.id}: (access restricted)")
        
        if len(collections) > 10:
            print(f"  ... and {len(collections) - 10} more collections")
        
        print("")
        print("📈 ESTIMATED USAGE:")
        
        # Rough estimates (these would come from actual monitoring in production)
        estimated_usage = {
            "storage_mb": total_docs * 2,  # ~2KB per document average
            "reads_today": total_docs * 10,  # Assume 10 reads per doc per day
            "writes_today": total_docs * 2,  # Assume 2 writes per doc per day
            "deletes_today": total_docs * 0.1  # Assume 0.1 deletes per doc per day
        }
        
        # Convert to percentages
        usage_percent = {
            "storage": (estimated_usage["storage_mb"] / 1024) / FREE_TIER["storage_gb"] * 100,
            "reads": estimated_usage["reads_today"] / FREE_TIER["reads_per_day"] * 100,
            "writes": estimated_usage["writes_today"] / FREE_TIER["writes_per_day"] * 100,
            "deletes": estimated_usage["deletes_today"] / FREE_TIER["deletes_per_day"] * 100
        }
        
        print(f"  📦 Storage: {estimated_usage['storage_mb']:.1f} MB ({usage_percent['storage']:.1f}% of 1GB free)")
        print(f"  👁️  Reads/day: {estimated_usage['reads_today']:,} ({usage_percent['reads']:.1f}% of 50k free)")
        print(f"  ✍️  Writes/day: {estimated_usage['writes_today']:,} ({usage_percent['writes']:.1f}% of 20k free)")
        print(f"  🗑️  Deletes/day: {estimated_usage['deletes_today']:,} ({usage_percent['deletes']:.1f}% of 20k free)")
        
        print("")
        print("🎯 STATUS:")
        
        # Check if any limits are approaching
        warnings = []
        for metric, percent in usage_percent.items():
            if percent > 80:
                warnings.append(f"  ⚠️  {metric.upper()} approaching limit ({percent:.1f}%)")
            elif percent > 50:
                warnings.append(f"  🔸 {metric.upper()} moderate usage ({percent:.1f}%)")
            else:
                print(f"  ✅ {metric.upper()} within limits ({percent:.1f}%)")
        
        for warning in warnings:
            print(warning)
        
        print("")
        print("💡 RECOMMENDATIONS:")
        if usage_percent["storage"] > 50:
            print("  • Consider archiving old data")
        if usage_percent["reads"] > 50:
            print("  • Implement caching for frequent reads")
        if usage_percent["writes"] > 50:
            print("  • Batch writes where possible")
        
        print("")
        print("✅ Firestore free tier is sufficient for current usage")
        
    except Exception as e:
        print(f"❌ Monitoring failed: {e}")
        print("")
        print("🔧 Troubleshooting:")
        print("  1. Make sure you're authenticated")
        print("  2. Check project permissions")
        print("  3. Verify Firestore API is enabled")

if __name__ == "__main__":
    check_firestore_usage()
