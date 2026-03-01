#!/usr/bin/env python3

import os
import sys
import requests
from datetime import datetime
from requests_oauthlib import OAuth1

def main():
    print("X API OAuth1 Test")
    print("="*50)

    consumer_key = os.getenv("X_CONSUMER_KEY")
    consumer_secret = os.getenv("X_CONSUMER_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_SECRET")

    if not all([consumer_key, consumer_secret, access_token, access_secret]):
        print("❌ Missing OAuth credentials in environment variables.")
        sys.exit(1)

    auth = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_secret
    )

    url = "https://api.twitter.com/2/tweets"
    payload = {
        "text": f"OAuth1 test post at {datetime.now().strftime('%H:%M:%S')} 🚀"
    }

    response = requests.post(url, auth=auth, json=payload)

    if response.status_code == 201:
        data = response.json()
        tweet_id = data.get("data", {}).get("id")
        print("✅ Tweet posted successfully!")
        print(f"https://twitter.com/user/status/{tweet_id}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
