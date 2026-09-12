"""Authentication helpers for Composio."""
import os
import logging
from typing import Optional

logger = logging.getLogger("composio.auth")

class AuthManager:
    """Manages Composio authentication flows."""
    
    def __init__(self, composio_client: Any = None):
        self._composio = composio_client or self._get_default_client()
        self._auth_tokens: Dict[str, str] = {}
    
    def _get_default_client(self):
        """Get a default Composio client from env."""
        api_key = os.getenv("COMPOSIO_API_KEY", "")
        if api_key:
            from composio import Composio
            return Composio(api_key=api_key)
        return None
    
    def ensure_auth(self, app_name: str) -> bool:
        """Ensure the current user is authenticated for an app."""
        try:
            accounts = self._composio.connected_accounts.list() if self._composio else []
            for account in accounts:
                if getattr(account, "app", None) == app_name:
                    return True
            return False
        except Exception:
            return False
    
    def get_auth_url(self, app_name: str, entity_id: str = None) -> Optional[str]:
        """Get the authentication URL for an app."""
        if not self._composio:
            return None
        try:
            session = self._composio.sessions.create(app=app_name, entity_id=entity_id)
            auth_url = getattr(session, "auth_url", None)
            if auth_url:
                self._auth_tokens[session.id] = auth_url
            return auth_url
        except Exception as e:
            logger.error(f"Failed to get auth URL for {app_name}: {e}")
            return None
    
    def handle_callback(self, app_name: str, code: str) -> Optional[str]:
        """Handle the OAuth callback and return session ID."""
        if not self._composio:
            return None
        try:
            session_id = self._composio.sessions.create(app=app_name)
            # In a real implementation, exchange code for token
            session = self._composio.sessions.get(session_id)
            return session_id
        except Exception as e:
            logger.error(f"Failed to handle callback for {app_name}: {e}")
            return None
    
    def get_token(self, session_id: str) -> Optional[str]:
        """Get the auth token for a session."""
        return self._auth_tokens.get(session_id)
    
    def revoke_auth(self, app_name: str) -> bool:
        """Revoke authentication for an app."""
        try:
            if self._composio:
                accounts = self._composio.connected_accounts.list()
                for account in accounts:
                    if getattr(account, "app", None) == app_name:
                        self._composio.connected_accounts.delete(account.id)
                        return True
            return False
        except Exception:
            return False
    
    def is_connected(self, app_name: str) -> bool:
        """Check if an app is connected."""
        return self.ensure_auth(app_name)