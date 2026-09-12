from shared.base_agent import BaseAgent
from shared.database_manager import DatabaseManager
from typing import Any, Dict

class BusinessManagerAgent(BaseAgent):
    """
    High-level oversight agent for business strategy, KPIs, and resource allocation.
    """
    def __init__(self, db: DatabaseManager):
        super().__init__(name="BusinessManagerAgent", role="Management")
        self.db = db
        self.load_skill("business_strategy")
        self.load_skill("resource_allocation")
        self.load_skill("kpi_monitoring")

    def run(self, task_context: Dict[str, Any]) -> Any:
        report_type = task_context.get("report_type", "summary")
        
        self.log(f"Generating business management report: {report_type}")
        
        # Simulated high-level business metrics
        report = {
            "report_type": report_type,
            "status": "healthy",
            "kpis": {
                "revenue": 5000,
                "growth": "15%",
                "efficiency": "high"
            },
            "recommendation": "Maintain current production cadence"
        }
        
        self.db.write_obsidian(f"reports/management_report.md", str(report))
        return report
