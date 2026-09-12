"""Optimisation Agent — close the feedback loop."""
import logging
from typing import Any, Dict, List
from shared.base_agent import BaseAgent

class OptimisationAgent(BaseAgent):
    """Learns from analytics and improves strategy."""
    agent_id = "optimisation"
    name = "Optimisation"

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.upstream_agents = ["orchestrator", "analytics"]
        self.downstream_agents = ["content_strategy", "trend_intelligence"]
        self.allowed_tools = [
            "ollama", "airtable_read", "airtable_write", "obsidian_read", "obsidian_write"
        ]
        self.read_permissions = ["analytics", "content", "campaigns"]
        self.write_permissions = ["learnings", "recommendations"]
        
        self.learning_rate = config.get("learning_rate", 0.1)

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance and recommend improvements."""
        analytics = context.get("analytics_output", {}).get("analytics", [])
        strategy = context.get("content_strategy_output", {})
        
        # Identify patterns
        patterns = self._identify_patterns(analytics)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(patterns, strategy)
        
        return {
            "patterns": patterns,
            "recommendations": recommendations,
            "confidence": 0.0
        }

    def _identify_patterns(self, analytics: List) -> List[Dict[str, Any]]:
        """Identify performance patterns."""
        return []

    def _generate_recommendations(self, patterns: List, strategy: Dict) -> List[str]:
        """Generate improvement recommendations."""
        return []

    def get_system_prompt(self) -> str:
        return f"""You are the Optimisation Agent.
You analyze performance data and recommend improvements.
Learning rate: {self.learning_rate}.
You identify what worked, what failed, and what to do next."""

    def get_capabilities(self) -> Dict[str, Any]:
        caps = super().get_capabilities()
        caps["learning_rate"] = self.learning_rate
        return caps

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the agent's task."""
        context = task_context.get("context", task_context)
        return asyncio.run(self.execute(context))
