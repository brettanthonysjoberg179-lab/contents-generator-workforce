"""SEO Agent — optimize content for search engines."""
from typing import Any, Dict
from shared.base_agent import BaseAgent

class SEOAgent(BaseAgent):
    agent_id = "seo"
    name = "SEO"
    upstream_agents = ["orchestrator", "content_strategy", "article_writer", "audience_intelligence"]
    downstream_agents = ["qa", "publishing"]
    allowed_tools = ["ollama", "search", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["content_briefs", "research", "content"]
    write_permissions = ["seo_metadata", "content"]

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        articles = context.get("article_writer_output", {}).get("articles", [])
        optimized = [{"title": a.get("title"), "meta": "", "keywords": [], "seo_score": 0} for a in articles]
        return {"optimized_articles": optimized, "total": len(optimized)}

    def get_system_prompt(self) -> str:
        return "You are the SEO Agent. Optimize content for search engines."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
