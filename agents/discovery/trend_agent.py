from shared.base_agent import BaseAgent
from shared.database_manager import DatabaseManager
from typing import Any, Dict

class TrendAgent(BaseAgent):
    """
    Determines what topics are gaining attention.
    """
    def __init__(self, db: DatabaseManager):
        super().__init__(name="TrendAgent", role="Trend Intelligence")
        self.db = db
        self.load_skill("trend_detection")
        self.load_skill("momentum_analysis")

    def run(self, task_context: Dict[str, Any]) -> Any:
        self.log("Detecting trends...")
        # Placeholder: Call trending API/Scraper
        trends = [{"topic": "AI Agents", "score": 0.95}]
        self.db.write_airtable("trends", trends[0])
        return trends
