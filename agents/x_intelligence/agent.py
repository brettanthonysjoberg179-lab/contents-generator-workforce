"""X Intelligence Agent — understand X/Twitter trends."""
from typing import Any, Dict
from shared.base_agent import BaseAgent

class XIntelligenceAgent(BaseAgent):
    agent_id = "x_intelligence"
    name = "X Intelligence"
    upstream_agents = ["orchestrator"]
    downstream_agents = ["audience_intelligence", "trend_intelligence", "research"]
    allowed_tools = ["ollama", "composio", "x", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["trends", "conversations"]
    write_permissions = ["research", "audience_insights"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.accounts = config.get("accounts_to_monitor", [])
        self.hashtags = config.get("hashtags", [])

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"trends": [], "conversations": [], "accounts": self.accounts, "hashtags": self.hashtags}

    def get_system_prompt(self) -> str:
        return f"You are the X Intelligence Agent. Accounts: {self.accounts}. Hashtags: {self.hashtags}."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
