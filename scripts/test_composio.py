#!/usr/bin/env python3
"""Composio connection test utility."""
import os
import sys

def main():
    print("Testing Composio connection...")
    
    api_key = os.getenv("COMPOSIO_API_KEY")
    if not api_key:
        print("ERROR: COMPOSIO_API_KEY not set")
        return 1
    
    print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
    
    try:
        from composio import Composio
        c = Composio(api_key=api_key)
        accounts = c.list_connected_accounts() if hasattr(c, 'list_connected_accounts') else []
        print(f"Connected accounts: {len(accounts) if accounts else 0}")
        
        if accounts:
            for acc in accounts[:5]:
                app = getattr(acc, 'app', str(acc))
                print(f"  - {app}")
        
        print("\n✓ Composio connection working")
        return 0
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())