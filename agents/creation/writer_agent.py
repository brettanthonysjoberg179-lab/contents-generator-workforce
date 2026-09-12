from shared.base_agent import BaseAgent
from shared.database_manager import DatabaseManager
from typing import Any, Dict

class WriterAgent(BaseAgent):
    """
    Specialized agent for long-form content generation.
    """
    def __init__(self, db: DatabaseManager):
        super().__init__(name="WriterAgent", role="Writer")
        self.db = db
        self.load_skill("long_form_writing")
        self.load_skill("storytelling")
        self.load_skill("brand_voice_adherence")

    def run(self, task_context: Dict[str, Any]) -> Any:
        topic = task_context.get("topic", "general topic")
        self.log(f"Drafting content for: {topic}")
        
        # Placeholder: Simulated drafting results
        draft = {
            "topic": topic,
            "content": f"# {topic}\n\nThis is a detailed draft about {topic}..."
        }
        
        self.db.write_obsidian(f"drafts/{topic}.md", draft["content"])
        return draft
