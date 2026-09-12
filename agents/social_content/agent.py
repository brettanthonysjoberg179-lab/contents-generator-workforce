"""Social Content Agent — produce short-form social copy."""
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class SocialContentAgent(BaseAgent):
    agent_id = "social_content"
    name = "Social Content"
    upstream_agents = ["orchestrator", "content_strategy"]
    downstream_agents = ["publishing", "qa"]
    allowed_tools = ["ollama", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["content_briefs", "brand"]
    write_permissions = ["content", "drafts"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.platforms = config.get("platforms", ["x", "facebook", "linkedin"])
        self.tone = config.get("tone", "conversational")

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        briefs = context.get("content_strategy_output", {}).get("content_briefs", [])
        posts = [{"platform": p, "content": "", "status": "draft"} for b in briefs for p in self.platforms]
        return {"posts": posts, "total": len(posts)}

    def get_system_prompt(self) -> str:
        return f"You are the Social Content Agent. Platforms: {', '.join(self.platforms)}. Tone: {self.tone}."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
