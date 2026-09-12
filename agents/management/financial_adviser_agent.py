from shared.base_agent import BaseAgent
from shared.database_manager import DatabaseManager
from typing import Any, Dict

class FinancialAdviserAgent(BaseAgent):
    """
    Specialized agent for financial planning, profit analysis, and budget monitoring.
    """
    def __init__(self, db: DatabaseManager):
        super().__init__(name="FinancialAdviserAgent", role="Finance")
        self.db = db
        self.load_skill("financial_reporting")
        self.load_skill("profit_analysis")
        self.load_skill("budget_management")

    def run(self, task_context: Dict[str, Any]) -> Any:
        analysis_type = task_context.get("analysis_type", "summary")
        
        self.log(f"Running financial analysis: {analysis_type}")
        
        # Simulated financial metrics
        financial_report = {
            "analysis_type": analysis_type,
            "metrics": {
                "total_revenue": 50000,
                "operating_costs": 35000,
                "net_profit": 15000
            },
            "insight": "Profit margins are healthy, but operating costs should be monitored."
        }
        
        self.db.write_obsidian(f"finance/report_{analysis_type}.md", str(financial_report))
        return financial_report
