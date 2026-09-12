"""LinkedIn Intelligence Agent — understand LinkedIn trends."""
from typing import Any, Dict
from shared.base_agent import BaseAgent

class LinkedInIntelligenceAgent(BaseAgent):
    agent_id = "linkedin_intelligence"
    name = "LinkedIn Intelligence"
    upstream_agents = ["orchestrator"]
    downstream_agents = ["audience_intelligence", "trend_intelligence", "research"]
    allowed_tools = ["ollama", "composio", "linkedin", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["posts", "articles", "profiles"]
    write_permissions = ["research", "audience_insights"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.hashtags = config.get("hashtags", [])
        self.companies = config.get("companies", [])

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"trends": [], "thought_leadership": [], "hashtags": self.hashtags, "companies": self.companies}

    def get_system_prompt(self) -> str:
        return f"You are the LinkedIn Intelligence Agent. Hashtags: {self.hashtags}. Companies: {self.companies}."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
