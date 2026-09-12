"""Reddit Intelligence Agent — understand Reddit conversations."""
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class RedditIntelligenceAgent(BaseAgent):
    agent_id = "reddit_intelligence"
    name = "Reddit Intelligence"
    upstream_agents = ["orchestrator"]
    downstream_agents = ["audience_intelligence", "trend_intelligence", "research"]
    allowed_tools = ["ollama", "composio", "reddit", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["subreddits", "posts", "comments"]
    write_permissions = ["research", "audience_insights"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.subreddits = config.get("subreddits", [])

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"subreddit_insights": [{"subreddit": s, "top_posts": [], "questions": []} for s in self.subreddits], "total": len(self.subreddits)}

    def get_system_prompt(self) -> str:
        return f"You are the Reddit Intelligence Agent. Subreddits: {', '.join(self.subreddits)}."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
