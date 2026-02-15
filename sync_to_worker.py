#!/usr/bin/env python3
"""
Script to sync links from local JSON to Cloudflare Worker KV storage
Run this after creating/updating links in Streamlit
"""

import json
import requests
import sys

# Configuration
WORKER_URL = "https://saikiranb.com/api/sync"  # Your custom domain
LINKS_FILE = "links.json"

def sync_links():
    """Sync local links to Cloudflare Worker"""
    try:
        # Load local links
        with open(LINKS_FILE, 'r') as f:
            links = json.load(f)

        print(f"📤 Syncing {len(links)} links to Cloudflare Worker...")

        # Send to worker
        response = requests.post(WORKER_URL, json=links)

        if response.status_code == 200:
            print("✅ Successfully synced links to Cloudflare Worker!")
            print(f"   Total links: {len(links)}")
        else:
            print(f"❌ Error syncing: {response.status_code}")
            print(f"   Response: {response.text}")
            sys.exit(1)

    except FileNotFoundError:
        print(f"❌ Error: {LINKS_FILE} not found")
        print("   Create some links in Streamlit first!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    sync_links()
