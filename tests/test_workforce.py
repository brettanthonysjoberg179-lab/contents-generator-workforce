"""Tests for the Content Generator Workforce."""
import pytest
import asyncio
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.base_agent import BaseAgent
from agents.orchestrator.agent import MasterOrchestrator
from agents.trend_intelligence.agent import TrendIntelligenceAgent
from agents.research.agent import ResearchAgent
from agents.audience_intelligence.agent import AudienceIntelligenceAgent
from agents.content_strategy.agent import ContentStrategyAgent
from agents.article_writer.agent import ArticleWriterAgent
from agents.social_content.agent import SocialContentAgent
from agents.video_script.agent import VideoScriptAgent
from agents.seo.agent import SEOAgent
from agents.repurposing.agent import RepurposingAgent
from agents.fact_check.agent import FactCheckAgent
from agents.qa.agent import QAAgent
from agents.publishing.agent import PublishingAgent
from agents.analytics.agent import AnalyticsAgent
from agents.optimisation.agent import OptimisationAgent
from agents.reddit_intelligence.agent import RedditIntelligenceAgent


def test_base_agent_init():
    """Test base agent initialization."""
    agent = TrendIntelligenceAgent({})
    assert agent.agent_id == "trend_intelligence"
    assert agent.status == "initialized"
    assert agent.run_count == 0


def test_agent_dependencies():
    """Test agent dependencies are set correctly."""
    trend = TrendIntelligenceAgent({})
    assert "orchestrator" in trend.upstream_agents
    assert "content_strategy" in trend.downstream_agents


def test_agent_permissions():
    """Test agent has required permissions."""
    trend = TrendIntelligenceAgent({})
    assert "composio" in trend.allowed_tools
    assert "airtable_read" in trend.allowed_tools
    assert "trends" in trend.read_permissions


def test_agent_capabilities():
    """Test agent capabilities reporting."""
    agent = ResearchAgent({})
    caps = agent.get_capabilities()
    assert "agent_id" in caps
    assert "name" in caps
    assert "upstream" in caps
    assert "tools" in caps


def test_orchestrator_registration():
    """Test orchestrator registers agents."""
    orch = MasterOrchestrator({})
    agent = TrendIntelligenceAgent({})
    orch.register_agent(agent)
    assert "trend_intelligence" in orch.agents


def test_orchestrator_topological_sort():
    """Test topological sort respects dependencies."""
    orch = MasterOrchestrator({})
    
    # Register agents
    orch.register_agent(TrendIntelligenceAgent({}))
    orch.register_agent(ResearchAgent({}))
    orch.register_agent(ContentStrategyAgent({}))
    
    order = orch._topological_sort()
    # Trend should come before research (research depends on trend)
    assert order.index("trend_intelligence") < order.index("research")
    # Research should come before strategy (strategy depends on research)
    assert order.index("research") < order.index("content_strategy")


def test_validate_dependencies():
    """Test dependency validation."""
    agent = ResearchAgent({})
    # Should fail without dependencies completed
    assert not agent.validate_dependencies([])
    # Should fail with only orchestrator completed (needs trend_intelligence too)
    assert not agent.validate_dependencies(["orchestrator"])
    # Should pass with all dependencies completed
    assert agent.validate_dependencies(["orchestrator", "trend_intelligence"])


def test_check_permission():
    """Test permission checking."""
    agent = TrendIntelligenceAgent({})
    assert agent.check_permission("composio")
    assert not agent.check_permission("invalid_tool")


def test_update_status():
    """Test status updates."""
    agent = TrendIntelligenceAgent({})
    agent.update_status("running")
    assert agent.status == "running"


def test_log_run():
    """Test run logging."""
    import time
    agent = TrendIntelligenceAgent({})
    start = time.time()
    agent.log_run(start, True)
    assert agent.run_count == 1
    assert agent.error_count == 0
    assert agent.last_run is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
