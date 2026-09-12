from shared.base_agent import BaseAgent
from shared.database_manager import DatabaseManager
from typing import Any, Dict

class DigitalProductConceptAgent(BaseAgent):
    """
    Specialized agent for brainstorming and defining new digital product concepts.
    """
    def __init__(self, db: DatabaseManager):
        super().__init__(name="DigitalProductConceptAgent", role="Discovery")
        self.db = db
        self.load_skill("concept_brainstorming")
        self.load_skill("value_proposition_definition")
        self.load_skill("market_alignment")

    def run(self, task_context: Dict[str, Any]) -> Any:
        topic = task_context.get("topic", "general")
        self.log(f"Brainstorming concepts for: {topic}")
        
        # Simulated concept generation
        concept = {
            "topic": topic,
            "concept_name": f"{topic} Mastery Guide",
            "value_proposition": f"Learn to master {topic} in under 30 days.",
            "target_audience": "beginners"
        }
        
        self.db.write_obsidian(f"concepts/{topic}_concept.md", str(concept))
        return concept
