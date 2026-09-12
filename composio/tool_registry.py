"""Tool registry for Composio tools organized by group."""
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("composio.tool_registry")

class ToolRegistry:
    """Registry of Composio tools organized by functional group."""
    
    TOOL_GROUPS = {
        "research": {
            "apps": ["reddit", "x", "tiktok", "facebook", "linkedin", "web_search", "google_search"],
            "description": "Tools for researching topics across platforms",
            "permissions": ["read"],
            "tool_prefixes": ["reddit_", "x_", "tiktok_", "facebook_", "linkedin_"]
        },
        "storage": {
            "apps": ["airtable", "google_drive", "obsidian"],
            "description": "Tools for reading and writing structured data and files",
            "permissions": ["read", "write"],
            "tool_prefixes": ["airtable_", "gdrive_", "obsidian_"]
        },
        "production": {
            "apps": ["google_drive", "obsidian", "github", "filesystem"],
            "description": "Tools for content production and file management",
            "permissions": ["read", "write"],
            "tool_prefixes": []
        },
        "publishing": {
            "apps": ["facebook", "tiktok", "x", "linkedin"],
            "description": "Tools for publishing content to social platforms",
            "permissions": ["write"],
            "tool_prefixes": ["facebook_", "tiktok_", "x_", "linkedin_"]
        },
        "analytics": {
            "apps": ["airtable", "platform_analytics"],
            "description": "Tools for collecting performance metrics",
            "permissions": ["read"],
            "tool_prefixes": []
        }
    }
    
    def __init__(self):
        self._tools: Dict[str, List[Dict[str, Any]]] = {}
        self._tool_schemas: Dict[str, Dict[str, Any]] = {}
    
    def register_app(self, app_name: str, tools: List[Dict[str, Any]]):
        """Register tools for an app."""
        self._tools[app_name] = tools
        for tool in tools:
            name = tool.get("name", "")
            self._tool_schemas[name] = tool
        logger.info(f"Registered {len(tools)} tools for {app_name}")
    
    def get_tools(self, app_name: str) -> List[Dict[str, Any]]:
        """Get tools for an app."""
        return self._tools.get(app_name, [])
    
    def get_all_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all registered tools."""
        return self._tools.copy()
    
    def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get the schema for a specific tool."""
        return self._tool_schemas.get(tool_name)
    
    def get_tool_group(self, group_name: str) -> Dict[str, Any]:
        """Get tool group definition."""
        return self.TOOL_GROUPS.get(group_name, {})
    
    def get_tools_by_group(self, group_name: str) -> List[str]:
        """Get app names for a tool group."""
        group = self.TOOL_GROUPS.get(group_name, {})
        return group.get("apps", [])
    
    def get_tool_groups(self) -> Dict[str, Dict[str, Any]]:
        """Get all tool groups."""
        return self.TOOL_GROUPS.copy()
    
    def get_tools_for_agent(self, agent_tools: List[str]) -> List[Dict[str, Any]]:
        """Get tool schemas for an agent's allowed tools."""
        schemas = []
        for tool_name in agent_tools:
            schema = self.get_tool_schema(tool_name)
            if schema:
                schemas.append(schema)
        return schemas
    
    def discover_tools(self, composio_client: Any, apps: List[str] = None) -> Dict[str, List[Dict]]:
        """Discover tools from Composio for given apps."""
        if not composio_client or not apps:
            return {}
        
        discovered = {}
        for app in apps:
            try:
                tools = composio_client.tools.list(app=app)
                tool_list = []
                for t in tools:
                    tool_list.append({
                        "name": getattr(t, "name", str(t)),
                        "description": getattr(t, "description", ""),
                        "parameters": getattr(t, "parameters", {}),
                        "app": app
                    })
                discovered[app] = tool_list
                self.register_app(app, tool_list)
            except Exception as e:
                logger.error(f"Failed to discover tools for {app}: {e}")
        return discovered

# Singleton
_tool_registry_instance: Optional[ToolRegistry] = None

def get_tool_registry() -> ToolRegistry:
    """Get the global tool registry instance."""
    global _tool_registry_instance
    if _tool_registry_instance is None:
        _tool_registry_instance = ToolRegistry()
    return _tool_registry_instance