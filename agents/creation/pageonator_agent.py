from shared.base_agent import BaseAgent
from shared.database_manager import DatabaseManager
from typing import Any, Dict

class PageonatorAgent(BaseAgent):
    """
    Specialized agent for templating, layout, and formatting.
    """
    def __init__(self, db: DatabaseManager):
        super().__init__(name="PageonatorAgent", role="Layout")
        self.db = db
        self.load_skill("templating")
        self.load_skill("formatting")
        self.load_skill("layout_assembly")

    def run(self, task_context: Dict[str, Any]) -> Any:
        # Robust content extraction
        content = task_context.get("content")
        if not content and "draft_content" in task_context:
            content = task_context["draft_content"].get("content")
        
        self.log(f"Assembling layout for content...")
        
        # Placeholder: Simulated layout/templating results
        formatted_page = f"--- TEMPLATE START ---\n{content or 'No content found'}\n--- TEMPLATE END ---"
        
        self.db.write_obsidian(f"layouts/final_page.md", formatted_page)
        return {"status": "formatted", "layout": formatted_page}
