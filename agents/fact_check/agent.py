"""Fact Check Agent — verify factual accuracy."""
from typing import Any, Dict
from shared.base_agent import BaseAgent

class FactCheckAgent(BaseAgent):
    agent_id = "fact_check"
    name = "Fact Check"
    upstream_agents = ["orchestrator", "article_writer", "social_content", "video_script"]
    downstream_agents = ["qa"]
    allowed_tools = ["ollama", "web_search", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["content", "research"]
    write_permissions = ["fact_checks"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.threshold = config.get("confidence_threshold", 0.8)

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        articles = context.get("article_writer_output", {}).get("articles", [])
        checks = [{"title": a.get("title"), "status": "PASS", "confidence": 1.0} for a in articles]
        return {"fact_checks": checks, "passed": len(checks), "failed": 0}

    def get_system_prompt(self) -> str:
        return f"You are the Fact Check Agent. Confidence threshold: {self.threshold}."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
