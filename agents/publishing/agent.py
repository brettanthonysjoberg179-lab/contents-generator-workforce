"""Publishing Agent — move approved content to platforms."""
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class PublishingAgent(BaseAgent):
    agent_id = "publishing"
    name = "Publishing"
    upstream_agents = ["orchestrator", "qa"]
    downstream_agents = ["analytics"]
    allowed_tools = ["ollama", "composio", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["content", "approved_content"]
    write_permissions = ["publish_log", "status"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.platforms = config.get("platforms", ["x", "facebook", "linkedin", "tiktok", "wordpress", "wix"])

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        results = context.get("qa_output", {}).get("qa_results", [])
        approved = [r for r in results if r["status"] == "PASS"]
        published = [{"item": a.get("item"), "platform": p, "status": "published"} for a in approved for p in self.platforms]
        return {"published": published, "total": len(published)}

    def get_system_prompt(self) -> str:
        return f"You are the Publishing Agent. Platforms: {', '.join(self.platforms)}."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
