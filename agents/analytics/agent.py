"""Analytics Agent — collect performance metrics."""
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class AnalyticsAgent(BaseAgent):
    agent_id = "analytics"
    name = "Analytics"
    upstream_agents = ["orchestrator", "publishing"]
    downstream_agents = ["optimisation", "content_strategy"]
    allowed_tools = ["ollama", "composio", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["publish_log", "content"]
    write_permissions = ["analytics", "reports"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.metrics = config.get("metrics", ["impressions", "engagement", "clicks", "conversions"])

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        published = context.get("publishing_output", {}).get("published", [])
        analytics = [{"item": p.get("item"), "platform": p.get("platform"), "metrics": {m: 0 for m in self.metrics}} for p in published]
        return {"analytics": analytics, "total": len(analytics)}

    def get_system_prompt(self) -> str:
        return f"You are the Analytics Agent. Metrics: {', '.join(self.metrics)}."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
