"""Repurposing Agent — turn one article into an entire campaign."""
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class RepurposingAgent(BaseAgent):
    agent_id = "repurposing"
    name = "Repurposing"
    upstream_agents = ["orchestrator", "content_strategy", "article_writer", "video_script", "social_content"]
    downstream_agents = ["fact_check", "qa", "publishing"]
    allowed_tools = ["ollama", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["content", "content_briefs"]
    write_permissions = ["content", "drafts"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.formats = config.get("output_formats", ["x_post", "linkedin_post", "facebook_post", "tiktok_concept", "hook"])

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        articles = context.get("article_writer_output", {}).get("articles", [])
        pieces = [{"format": f, "source": a.get("title"), "status": "draft"} for a in articles for f in self.formats]
        return {"repurposed_content": pieces, "total": len(pieces)}

    def get_system_prompt(self) -> str:
        return f"You are the Repurposing Agent. Formats: {', '.join(self.formats)}."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
