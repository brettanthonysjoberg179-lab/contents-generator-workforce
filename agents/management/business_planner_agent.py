from shared.base_agent import BaseAgent
from shared.database_manager import DatabaseManager
from typing import Any, Dict

class BusinessPlannerAgent(BaseAgent):
    """
    Specialized agent for strategic planning, roadmap development, and project scheduling.
    """
    def __init__(self, db: DatabaseManager):
        super().__init__(name="BusinessPlannerAgent", role="Planning")
        self.db = db
        self.load_skill("strategic_planning")
        self.load_skill("roadmap_development")
        self.load_skill("project_scheduling")

    def run(self, task_context: Dict[str, Any]) -> Any:
        goal = task_context.get("goal", "growth")
        
        self.log(f"Developing strategic plan for: {goal}")
        
        # Simulated roadmap
        roadmap = {
            "goal": goal,
            "phases": [
                {"phase": "Q1", "action": "Market expansion"},
                {"phase": "Q2", "action": "Product diversification"},
                {"phase": "Q3", "action": "Scale operations"}
            ]
        }
        
        self.db.write_obsidian(f"planning/roadmap_{goal}.md", str(roadmap))
        return roadmap
