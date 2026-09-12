"""Article Writer Agent — produce long-form content."""
from typing import Any, Dict
from shared.base_agent import BaseAgent

class ArticleWriterAgent(BaseAgent):
    agent_id = "article_writer"
    name = "Article Writer"
    upstream_agents = ["orchestrator", "content_strategy", "research"]
    downstream_agents = ["seo", "repurposing", "fact_check", "qa"]
    allowed_tools = ["ollama", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write", "google_drive_read", "google_drive_write"]
    read_permissions = ["content_briefs", "research", "brand"]
    write_permissions = ["content", "drafts"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.style = config.get("writing_style", "professional")
        self.target_words = config.get("target_word_count", 1500)

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        briefs = context.get("content_strategy_output", {}).get("content_briefs", [])
        articles = [{"title": b.get("topic", ""), "word_count": 0, "status": "draft"} for b in briefs]
        return {"articles": articles, "total": len(articles)}

    def get_system_prompt(self) -> str:
        return f"You are the Article Writer. Style: {self.style}. Target: {self.target_words} words."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
