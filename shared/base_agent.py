from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import asyncio

class BaseAgent(ABC):
    """
    Base class for all agents in the Content Generator Workforce.
    Provides common interface, skill loading, and tool access.
    """
    def __init__(self, name: str = "Agent", role: str = "agent", config: Dict[str, Any] = None):
        self.name = name
        self.role = role
        self.skills = []
        self.tools = []
        self.config = config or {}
        self.status = "initialized"
        self.run_count = 0
        self.error_count = 0
        self.last_run = None

    def load_skill(self, skill_name: str):
        self.skills.append(skill_name)

    def register_tool(self, tool_name: str):
        self.tools.append(tool_name)

    @abstractmethod
    def run(self, task_context: Dict[str, Any]) -> Any:
        pass

    def log(self, message: str):
        print(f"[{self.name}][{self.role}] {message}")

    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "agent_id": getattr(self, "agent_id", self.name),
            "name": self.name,
            "role": self.role,
            "upstream": getattr(self, "upstream_agents", []),
            "downstream": getattr(self, "downstream_agents", []),
            "tools": getattr(self, "allowed_tools", []),
            "status": self.status,
        }

    def validate_dependencies(self, completed_agents: List[str]) -> bool:
        upstream = getattr(self, "upstream_agents", [])
        return all(dep in completed_agents for dep in upstream)

    def update_status(self, status: str):
        self.status = status

    def check_permission(self, tool: str) -> bool:
        return tool in getattr(self, "allowed_tools", [])

    def log_run(self, start_time: float, success: bool):
        import time
        self.run_count += 1
        self.last_run = time.time()
        self.last_run_success = success
        if not success:
            self.error_count += 1

    async def execute(self, context: Dict[str, Any]) -> Any:
        raise NotImplementedError