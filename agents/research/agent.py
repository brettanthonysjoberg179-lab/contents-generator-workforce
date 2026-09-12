"""Research Agent — turn topics into reliable research."""
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class ResearchAgent(BaseAgent):
    """Produces structured research from topics and trends."""
    
    agent_id = "research"
    name = "Research Agent"
    upstream_agents = ["orchestrator", "trend_intelligence"]
    downstream_agents = ["content_strategy", "article_writer", "fact_check"]
    allowed_tools = ["composio", "web_search", "airtable_read", "airtable_write",
                     "obsidian_read", "obsidian_write", "google_drive_read", "google_drive_write"]
    read_permissions = ["trends", "brand", "research"]
    write_permissions = ["research", "sources", "facts"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.max_sources = config.get("max_sources", 10)
        self.min_credibility = config.get("min_credibility_score", 0.7)

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        trends = context.get("trend_intelligence_output", {}).get("trends", [])
        briefs = [await self._research(t) for t in trends[:5]]
        return {"research_briefs": briefs, "total": len(briefs)}

    async def _research(self, topic: Dict) -> Dict[str, Any]:
        return {"topic": topic.get("topic"), "sources": [], "facts": [], "quotes": []}

    def get_system_prompt(self) -> str:
        return f"""You are the Research Agent. Turn topics into reliable research.
Max sources: {self.max_sources}. Min credibility: {self.min_credibility}.
All claims must be verifiable."""

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
