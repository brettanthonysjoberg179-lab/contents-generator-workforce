"""Video Script Agent — produce video scripts and storyboards."""
from typing import Any, Dict
from shared.base_agent import BaseAgent

class VideoScriptAgent(BaseAgent):
    agent_id = "video_script"
    name = "Video Script"
    upstream_agents = ["orchestrator", "content_strategy"]
    downstream_agents = ["repurposing", "publishing", "qa"]
    allowed_tools = ["ollama", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write", "google_drive_read", "google_drive_write"]
    read_permissions = ["content_briefs", "brand"]
    write_permissions = ["content", "drafts"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.format = config.get("format", "short_form")
        self.duration = config.get("target_duration", 60)

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        briefs = context.get("content_strategy_output", {}).get("content_briefs", [])
        scripts = [{"hook": "", "scenes": [], "cta": "", "status": "draft"} for _ in briefs]
        return {"scripts": scripts, "total": len(scripts)}

    def get_system_prompt(self) -> str:
        return f"You are the Video Script Agent. Format: {self.format}. Duration: {self.duration}s."

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
