"""Trend Intelligence Agent — determine what topics are gaining attention."""
from typing import Any, Dict, List
import asyncio
from shared.base_agent import BaseAgent

class TrendIntelligenceAgent(BaseAgent):
    """Scans platforms for emerging trends and scores them."""
    
    agent_id = "trend_intelligence"
    name = "Trend Intelligence"
    upstream_agents = ["orchestrator"]
    downstream_agents = ["content_strategy", "research"]
    allowed_tools = ["composio", "reddit", "x", "tiktok", "facebook", "linkedin",
                     "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"]
    read_permissions = ["trends", "research", "analytics"]
    write_permissions = ["trends", "opportunities"]

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config=config)
        self.platforms = config.get("platforms", ["reddit", "x", "tiktok"]) if config else ["reddit", "x", "tiktok"]
        self.trend_threshold = config.get("trend_threshold", 0.6) if config else 0.6

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Scan platforms for trends and score them."""
        trends = []
        for platform in self.platforms:
            trends.extend(await self._scan_platform(platform))
        
        scored = sorted(
            [{**t, "trend_score": self._score(t)} for t in trends],
            key=lambda x: x["trend_score"],
            reverse=True
        )
        filtered = [t for t in scored if t["trend_score"] >= self.trend_threshold]
        
        return {"trends": filtered, "total_discovered": len(trends), "total_qualified": len(filtered)}

    async def _scan_platform(self, platform: str) -> List[Dict[str, Any]]:
        """Scan a single platform for trends."""
        return []

    def _score(self, trend: Dict) -> float:
        """Calculate composite trend score."""
        return (
            trend.get("momentum", 0) * 0.5 +
            trend.get("audience_size", 0) * 0.3 +
            (1 - trend.get("competition", 1)) * 0.2
        )

    def get_system_prompt(self) -> str:
        return f"""You are the Trend Intelligence Agent.
Scan {', '.join(self.platforms)} for emerging topics.
Score trends by momentum (50%), audience (30%), competition (20%).
Only pass trends above {self.trend_threshold} threshold."""

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))