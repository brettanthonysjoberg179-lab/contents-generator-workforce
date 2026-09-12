"""Audience Intelligence Agent — combine platform findings into audience model."""
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class AudienceIntelligenceAgent(BaseAgent):
    agent_id = "audience_intelligence"
    name = "Audience Intelligence"
    upstream_agents = ["orchestrator", "reddit_intelligence", "x_intelligence", "tiktok_intelligence", "facebook_intelligence", "linkedin_intelligence"]
    downstream_agents = ["content_strategy", "article_writer", "social_content", "video_script", "seo"]
    allowed_tools = ["ollama", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["research", "platform_data"]
    write_permissions = ["audience_model", "personas"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.segments = config.get("segments", ["interested", "active", "advocate"])

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        model = {
            "primary_persona": {},
            "pain_points": [],
            "questions": [],
            "segments": {},
            "platforms": {k: v for k, v in context.items() if k.endswith("_output")}
        }
        return {"audience_model": model, "platforms_analyzed": len(model["platforms"])}

    def get_system_prompt(self) -> str:
        return f"""You are the Audience Intelligence Agent.
Combine platform research into a single audience model.
Segments: {', '.join(self.segments)}."""

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
