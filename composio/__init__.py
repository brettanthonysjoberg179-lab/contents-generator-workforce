"""Composio integration module for the Content Generator Workforce.

Wraps the composio-client SDK to provide session management,
tool discovery, and execution for the workforce.
"""
import os
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("composio_workforce")

# Import from the third-party package
from composio_client import Composio as _ComposioSDK

# Re-export
ComposioSDK = _ComposioSDK

# Import our integration classes (based on shared/composio_client.py)
class ComposioClient:
    """Client for Composio tool discovery and execution.
    
    Based on shared/composio_client.py but enhanced with real SDK calls.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("COMPOSIO_API_KEY", "")
        self._sdk = None
        if self.api_key:
            try:
                self._sdk = _ComposioSDK(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Composio SDK: {e}")
    
    def get_sdk(self):
        return self._sdk
    
    async def discover_tools(self, app: str = None) -> List[Dict[str, Any]]:
        if not self._sdk: return []
        try:
            if app:
                tools = self._sdk.tools.list(app=app)
            else:
                tools = self._sdk.tools.list()
            return [{"name": t.name, "description": t.description} for t in tools]
        except Exception: return []
    
    async def execute_tool(self, tool_name: str, arguments: Dict) -> Dict[str, Any]:
        if not self._sdk: return {"success": False, "error": "Not initialized"}
        try:
            result = self._sdk.execute_tool(tool_name, arguments)
            return {"success": True, "result": result}
        except Exception as e: return {"success": False, "error": str(e)}
    
    async def get_tool_schemas(self, apps: List[str] = None) -> List[Dict]:
        if not apps: apps = ["reddit", "x", "tiktok", "facebook", "linkedin"]
        all_tools = []
        for app in apps:
            tools = await self.discover_tools(app)
            all_tools.extend(tools)
        return all_tools

class ComposioIntegration:
    """High-level Composio integration for the workforce."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("COMPOSIO_API_KEY", "")
        self.client = ComposioClient(self.api_key)
        self._sdk = self.client._sdk
    
    def get_session(self, session_id: str) -> Optional[Any]:
        if not self._sdk: return None
        try: return self._sdk.sessions.get(session_id)
        except Exception: return None
    
    def create_session(self, app_name: str, entity_id: str = None) -> str:
        if not self._sdk: raise ValueError("Composio not initialized")
        session = self._sdk.sessions.create(app=app_name, entity_id=entity_id)
        return session.id
    
    def execute_tool(self, session_id: str, tool_name: str, arguments: Dict) -> Dict:
        if not self._sdk: return {"success": False, "error": "Not initialized"}
        try:
            session = self._sdk.sessions.get(session_id)
            result = session.execute_tool(tool_name, arguments)
            return {"success": True, "result": result}
        except Exception as e: return {"success": False, "error": str(e)}
    
    def list_connected_accounts(self) -> List:
        if not self._sdk: return []
        try: return self._sdk.connected_accounts.list()
        except Exception: return []
    
    def list_tools(self, app_name: str = None) -> List:
        if not self._sdk: return []
        try:
            if app_name: return self._sdk.tools.list(app=app_name)
            return self._sdk.tools.list()
        except Exception: return []
    
    def get_auth_url(self, app_name: str, entity_id: str = None) -> str:
        if not self._sdk: return ""
        session = self._sdk.sessions.create(app=app_name, entity_id=entity_id)
        return getattr(session, "auth_url", "")
    
    def get_composio_client(self) -> ComposioClient:
        return self.client

class SessionManager:
    """Manages Composio sessions with caching and TTL."""
    
    def __init__(self, composio: ComposioIntegration = None, ttl_seconds: int = 3600):
        self.composio = composio or ComposioIntegration()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = ttl_seconds
    
    def create_session(self, app_name: str, entity_id: str = None) -> str:
        session_id = self.composio.create_session(app_name, entity_id)
        self._cache[session_id] = {
            "id": session_id, "app": app_name,
            "created_at": __import__("datetime").datetime.now().isoformat(),
            "expires_at": (__import__("datetime").datetime.now() + __import__("datetime").timedelta(seconds=self._ttl)).isoformat()
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        if session_id in self._cache:
            data = self._cache[session_id]
            import datetime
            if datetime.datetime.fromisoformat(data["expires_at"]) > datetime.datetime.now():
                return data
            del self._cache[session_id]
        return None
    
    def execute_tool(self, session_id: str, tool_name: str, arguments: Dict) -> Dict:
        session = self.get_session(session_id)
        if not session: return {"success": False, "error": "Session not found"}
        return self.composio.execute_tool(session_id, tool_name, arguments)
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        import datetime
        now = datetime.datetime.now()
        return [d for d in self._cache.values() if datetime.datetime.fromisoformat(d["expires_at"]) > now]
    
    def delete_session(self, session_id: str) -> bool:
        if session_id in self._cache: del self._cache[session_id]
        return True
    
    def cleanup_expired(self):
        import datetime
        now = datetime.datetime.now()
        expired = [sid for sid, d in self._cache.items() if datetime.datetime.fromisoformat(d["expires_at"]) < now]
        for sid in expired: del self._cache[sid]

class ToolRegistry:
    """Registry of Composio tools organized by group."""
    
    TOOL_GROUPS = {
        "research": {
            "apps": ["reddit", "x", "tiktok", "facebook", "linkedin", "web_search", "google_search"],
            "description": "Research and discovery tools",
            "permissions": ["read"],
            "tool_prefixes": ["reddit_", "x_", "tiktok_", "facebook_", "linkedin_"]
        },
        "storage": {
            "apps": ["airtable", "google_drive", "obsidian"],
            "description": "Data storage tools",
            "permissions": ["read", "write"],
            "tool_prefixes": ["airtable_", "gdrive_", "obsidian_"]
        },
        "production": {
            "apps": ["google_drive", "obsidian", "github", "filesystem"],
            "description": "Content production tools",
            "permissions": ["read", "write"],
            "tool_prefixes": []
        },
        "publishing": {
                    "tools": PUBLISHING_TOOLS,
                    "description": "Social media and CMS publishing tools including WordPress, Wix, Gumroad and Payhip",
                    "permission": "write",
                    "tool_prefixes": ["facebook_", "tiktok_", "x_", "linkedin_", "wordpress_", "wix_", "gumroad_", "payhip_"]
                },
                "analytics": {
                    "apps": ["airtable", "platform_analytics", "wordpress", "wix", "gumroad", "payhip"],
            "description": "Analytics tools",
            "permissions": ["read"],
            "tool_prefixes": []
        }
    }
    
    def __init__(self):
        self._tools: Dict[str, List[Dict]] = {}
    
    def register_app(self, app_name: str, tools: List[Dict]):
        self._tools[app_name] = tools
    
    def get_tools(self, app_name: str) -> List[Dict]:
        return self._tools.get(app_name, [])
    
    def get_all_tools(self) -> Dict[str, List[Dict]]:
        return self._tools.copy()
    
    def get_tool_group(self, group_name: str) -> Dict[str, Any]:
        return self.TOOL_GROUPS.get(group_name, {})
    
    def get_tools_by_group(self, group_name: str) -> List[str]:
        return self.TOOL_GROUPS.get(group_name, {}).get("apps", [])
    
    def get_tool_groups(self) -> Dict[str, Dict[str, Any]]:
        return self.TOOL_GROUPS.copy()

# Singleton
_composio_integration: Optional[ComposioIntegration] = None

def get_composio_integration() -> ComposioIntegration:
    global _composio_integration
    if _composio_integration is None:
        _composio_integration = ComposioIntegration()
    return _composio_integration

def get_session_manager() -> SessionManager:
    return SessionManager(get_composio_integration())

# Import mappings
from composio.mappings import (
    RESEARCH_TOOLS, STORAGE_TOOLS, PRODUCTION_TOOLS, PUBLISHING_TOOLS, ANALYTICS_TOOLS,
    TOOL_GROUP_DEFINITIONS, get_tools_for_group, get_all_tool_groups, get_agents_for_group, get_platform_agents
)

__version__ = "1.0.0"
__all__ = [
    "ComposioIntegration", "ComposioClient", "ComposioSDK",
    "SessionManager", "ToolRegistry",
    "get_composio_integration", "get_session_manager",
    "RESEARCH_TOOLS", "STORAGE_TOOLS", "PRODUCTION_TOOLS",
    "PUBLISHING_TOOLS", "ANALYTICS_TOOLS", "TOOL_GROUP_DEFINITIONS",
    "get_tools_for_group", "get_all_tool_groups", "get_agents_for_group",
]