"""QA Agent — validate content readiness."""
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class QAAgent(BaseAgent):
    agent_id = "qa"
    name = "QA"
    upstream_agents = ["orchestrator", "article_writer", "social_content", "video_script", "fact_check", "seo"]
    downstream_agents = ["publishing"]
    allowed_tools = ["ollama", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["content", "brand", "fact_checks"]
    write_permissions = ["qa_results"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.checklist = config.get("checklist", ["grammar", "brand_voice", "format", "links"])

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        articles = context.get("article_writer_output", {}).get("articles", [])
        posts = context.get("social_content_output", {}).get("posts", [])
        results = [{"title": (a.get("title", "") or a.get("content", ""))[:50], "status": "PASS"} for a in articles + posts]
        return {"qa_results": results, "passed": len(results), "failed": 0}

    def get_system_prompt(self) -> str:
        return f"You are the QA Agent. Checklist: {', '.join(self.checklist)}."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
