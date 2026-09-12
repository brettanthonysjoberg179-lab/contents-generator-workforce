"""Composio session management for the Content Generator Workforce."""
import os
import logging
import time
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger("composio.sessions")

class SessionManager:
    """Manages Composio sessions with caching and TTL."""
    
    def __init__(self, composio_client: Any = None, ttl_seconds: int = 3600):
        self._composio = composio_client
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = ttl_seconds
    
    def create_session(self, app_name: str, entity_id: str = None) -> str:
        """Create a new Composio session for an app."""
        if not self._composio:
            raise ValueError("Composio client not initialized")
        
        session = self._composio.sessions.create(app=app_name, entity_id=entity_id)
        session_data = {
            "id": session.id,
            "app": app_name,
            "entity_id": entity_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(seconds=self._ttl)).isoformat(),
            "auth_url": getattr(session, "auth_url", None),
            "status": "pending"
        }
        self._cache[session.id] = session_data
        logger.info(f"Created session {session.id} for {app_name}")
        return session.id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a session from cache or Composio."""
        # Check cache first
        if session_id in self._cache:
            cached = self._cache[session_id]
            expires_at = datetime.fromisoformat(cached["expires_at"])
            if datetime.now() < expires_at:
                return cached
            else:
                del self._cache[session_id]
        
        # Try to fetch from Composio
        if self._composio:
            try:
                session = self._composio.sessions.get(session_id)
                return {
                    "id": session.id,
                    "app": getattr(session, "app", None),
                    "status": getattr(session, "status", "unknown"),
                    "entity_id": getattr(session, "entity_id", None),
                }
            except Exception:
                return None
        return None
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all cached sessions."""
        self._cleanup_expired()
        return list(self._cache.values())
    
    def execute_tool(self, session_id: str, tool_name: str, arguments: Dict) -> Dict[str, Any]:
        """Execute a tool through a session."""
        session = self.get_session(session_id)
        if not session:
            return {"success": False, "error": f"Session {session_id} not found"}
        
        if not self._composio:
            return {"success": False, "error": "Composio client not initialized"}
        
        try:
            result = self._composio.sessions.get(session_id).execute_tool(tool_name, arguments)
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return {"success": False, "error": str(e)}
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self._cache:
            del self._cache[session_id]
        if self._composio:
            try:
                self._composio.sessions.delete(session_id)
                return True
            except Exception:
                return False
        return True
    
    def cleanup_expired(self):
        """Remove expired sessions from cache."""
        now = datetime.now()
        expired = [
            sid for sid, data in self._cache.items()
            if datetime.fromisoformat(data["expires_at"]) < now
        ]
        for sid in expired:
            del self._cache[sid]
        logger.info(f"Cleaned up {len(expired)} expired sessions")
    
    def get_session_status(self, session_id: str) -> str:
        """Get the status of a session."""
        session = self.get_session(session_id)
        if not session:
            return "not_found"
        return session.get("status", "unknown")