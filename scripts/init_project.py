#!/usr/bin/env python3
"""Initialize the Content Generator Workforce project structure.

Creates all required directories and copies configuration templates.
"""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

DIRS = [
    "knowledge/brand",
    "knowledge/audience",
    "knowledge/content_rules",
    "knowledge/platform_rules",
    "knowledge/research",
    "agents/tiktok_agent",
    "agents/x_agent",
    "agents/linkedin_agent",
    "agents/reddit_agent",
    "agents/facebook_agent",
    "agents/article_writer/knowledge",
    "agents/article_writer/prompts",
    "agents/article_writer/code",
    "agents/article_writer/tests",
    "mcp_server/schemas",
    "mcp_server/resources",
    "mcp_server/prompts",
    "files/incoming",
    "files/working",
    "files/approved",
    "files/published",
    "files/archive",
    "logs",
    "reports",
    "scripts",
    "data",
]

def main():
    print("Initializing Content Generator Workforce...")
    for d in DIRS:
        path = PROJECT_ROOT / d
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {d}")
    
    print("\nProject structure initialized.")
    print(f"Root: {PROJECT_ROOT}")

if __name__ == "__main__":
    main()