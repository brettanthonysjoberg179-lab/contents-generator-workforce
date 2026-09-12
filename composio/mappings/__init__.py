"""Composio tool group mappings."""

RESEARCH_TOOLS = ["reddit", "x", "tiktok", "facebook", "linkedin", "web_search", "google_search"]
STORAGE_TOOLS = ["airtable", "google_drive", "obsidian"]
PRODUCTION_TOOLS = ["google_drive", "obsidian", "github", "filesystem"]
PUBLISHING_TOOLS = ["facebook", "tiktok", "x", "linkedin"]
ANALYTICS_TOOLS = ["airtable", "platform_analytics"]

TOOL_GROUP_DEFINITIONS = {
    "research": {
        "tools": RESEARCH_TOOLS,
        "description": "Research and discovery tools for scanning platforms and finding information",
        "permission": "read",
        "agents": ["trend_intelligence", "research", "reddit_intelligence", "x_intelligence", "tiktok_intelligence", "facebook_intelligence", "linkedin_intelligence"]
    },
    "storage": {
        "tools": STORAGE_TOOLS,
        "description": "Data storage tools for reading and writing structured data",
        "permission": "read_write",
        "agents": ["all"]
    },
    "production": {
        "tools": PRODUCTION_TOOLS,
        "description": "Content production and file management tools",
        "permission": "read_write",
        "agents": ["article_writer", "social_content", "video_script", "seo", "repurposing"]
    },
    "publishing": {
        "tools": PUBLISHING_TOOLS,
        "description": "Social media publishing tools",
        "permission": "write",
        "agents": ["publishing"]
    },
    "analytics": {
        "tools": ANALYTICS_TOOLS,
        "description": "Analytics and performance tracking tools",
        "permission": "read",
        "agents": ["analytics", "optimisation"]
    }
}

def get_tools_for_group(group_name: str) -> list:
    """Get the list of apps for a tool group."""
    return TOOL_GROUP_DEFINITIONS.get(group_name, {}).get("tools", [])

def get_all_tool_groups() -> dict:
    """Get all tool group definitions."""
    return TOOL_GROUP_DEFINITIONS.copy()

def get_agents_for_group(group_name: str) -> list:
    """Get agents assigned to a tool group."""
    return TOOL_GROUP_DEFINITIONS.get(group_name, {}).get("agents", [])