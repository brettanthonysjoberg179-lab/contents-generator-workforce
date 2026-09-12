"""Content Strategy Agent — determine what should be produced."""
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class ContentStrategyAgent(BaseAgent):
    agent_id = "content_strategy"
    name = "Content Strategy"
    upstream_agents = ["orchestrator", "trend_intelligence", "research", "audience_intelligence"]
    downstream_agents = ["article_writer", "social_content", "video_script", "seo", "repurposing"]
    allowed_tools = ["airtable_read", "airtable_write", "obsidian_read", "obsidian_write", "google_drive_read", "google_drive_write"]
    read_permissions = ["trends", "research", "audience", "brand", "analytics"]
    write_permissions = ["campaigns", "content_briefs", "content_calendar"]

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        trends = context.get("trend_intelligence_output", {}).get("trends", [])
        research = context.get("research_output", {}).get("research_briefs", [])
        audience = context.get("audience_intelligence_output", {})
        
        briefs = [{
            "topic": t.get("topic"),
            "trend_score": t.get("trend_score"),
            "audience": audience.get("audience_model", {}),
            "platforms": ["reddit", "x", "linkedin"]
        } for t in trends[:3]]
        
        return {"content_briefs": briefs, "total": len(briefs)}

    def get_system_prompt(self) -> str:
        return "You are the Content Strategy Agent. Create content briefs from research and trends."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
