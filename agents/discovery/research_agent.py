from shared.base_agent import BaseAgent
from shared.database_manager import DatabaseManager
from typing import Any, Dict

class ResearchAgent(BaseAgent):
    """
    Turns a topic into reliable research.
    """
    def __init__(self, db: DatabaseManager):
        super().__init__(name="ResearchAgent", role="Research")
        self.db = db
        self.load_skill("web_research")
        self.load_skill("fact_extraction")

    def run(self, task_context: Dict[str, Any]) -> Any:
        topic = task_context.get("topic")
        self.log(f"Conducting research on: {topic}")
        # Placeholder: Search + Summarization
        research_data = {"topic": topic, "facts": ["Fact 1", "Fact 2"]}
        self.db.write_obsidian(f"research/{topic}.md", str(research_data))
        return research_data
