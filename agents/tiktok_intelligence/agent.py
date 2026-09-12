"""TikTok Intelligence Agent — understand TikTok trends."""
from typing import Any, Dict
from shared.base_agent import BaseAgent

class TikTokIntelligenceAgent(BaseAgent):
    agent_id = "tiktok_intelligence"
    name = "TikTok Intelligence"
    upstream_agents = ["orchestrator"]
    downstream_agents = ["audience_intelligence", "trend_intelligence", "research"]
    allowed_tools = ["ollama", "composio", "tiktok", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["trends", "videos"]
    write_permissions = ["research", "audience_insights"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.hashtags = config.get("hashtags", [])
        self.creators = config.get("creators", [])

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"trends": [], "hooks": [], "hashtags": self.hashtags, "creators": self.creators}

    def get_system_prompt(self) -> str:
        return f"You are the TikTok Intelligence Agent. Hashtags: {self.hashtags}. Creators: {self.creators}."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
