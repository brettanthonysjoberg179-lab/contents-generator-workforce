"""MCP Server — exposes the agent workforce as tools.

Updated to support both HTTP (FastAPI) and stdio modes for Hermes integration.
"""
import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

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
from agents.x_intelligence.agent import XIntelligenceAgent
from agents.tiktok_intelligence.agent import TikTokIntelligenceAgent
from agents.facebook_intelligence.agent import FacebookIntelligenceAgent
from agents.linkedin_intelligence.agent import LinkedInIntelligenceAgent
from agents.wordpress_intelligence.agent import WordPressIntelligenceAgent
from agents.wix_intelligence.agent import WixIntelligenceAgent

logger = logging.getLogger("mcp_server")


class ToolRequest(BaseModel):
    tool: str
    arguments: Dict[str, Any] = {}


class ToolResponse(BaseModel):
    success: bool
    result: Any = None
    error: str = None


class MCPTool:
    """Wrapper to expose an agent as an MCP tool."""
    
    def __init__(self, name: str, description: str, agent, input_schema: Dict):
        self.name = name
        self.description = description
        self.agent = agent
        self.input_schema = input_schema
    
    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = await self.agent.execute(arguments)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}


class MCPServer:
    """FastAPI MCP server with stdio support for Hermes integration."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self.app = FastAPI(title="Content Generator Workforce MCP")
        self.orchestrator = MasterOrchestrator({})
        self.tools: Dict[str, MCPTool] = {}
        self._setup_routes()
        self._register_agents()
    
    def _setup_routes(self):
        @self.app.get("/health")
        async def health():
            return {"status": "healthy", "agents": len(self.orchestrator.agents), "tools": len(self.tools)}
        
        @self.app.get("/tools")
        async def list_tools():
            return {"tools": [{"name": t.name, "description": t.description, "input_schema": t.input_schema} for t in self.tools.values()]}
        
        @self.app.post("/tools/call")
        async def call_tool(request: ToolRequest):
            if request.tool not in self.tools:
                raise HTTPException(status_code=404, detail=f"Tool '{request.tool}' not found")
            result = await self.tools[request.tool].execute(request.arguments)
            if result["success"]:
                return ToolResponse(success=True, result=result["result"])
            return ToolResponse(success=False, error=result["error"])
        
        @self.app.post("/workflows/run")
        async def run_workflow(request: Dict[str, Any]):
            workflow_id = request.get("workflow_id", "default")
            input_data = request.get("input", {})
            result = await self.orchestrator.execute_workflow(workflow_id, input_data)
            return result
        
        @self.app.get("/agents")
        async def list_agents():
            return {"agents": self.orchestrator.get_agent_status()}
    
    def _register_agents(self):
        agents_config = {
            "trend_intelligence": (TrendIntelligenceAgent, {"platforms": ["reddit", "x", "tiktok", "facebook", "linkedin"]}),
            "research": (ResearchAgent, {"max_sources": 10, "min_credibility_score": 0.7}),
            "audience_intelligence": (AudienceIntelligenceAgent, {"segments": ["interested", "active", "advocate"]}),
            "content_strategy": (ContentStrategyAgent, {"posting_frequency": "daily"}),
            "article_writer": (ArticleWriterAgent, {"writing_style": "professional", "target_word_count": 1500}),
            "social_content": (SocialContentAgent, {"platforms": ["x", "facebook", "linkedin"], "tone": "conversational"}),
            "video_script": (VideoScriptAgent, {"format": "short_form", "target_duration": 60}),
            "seo": (SEOAgent, {"keyword_density": 0.02}),
            "repurposing": (RepurposingAgent, {"output_formats": ["x_post", "linkedin_post", "facebook_post", "tiktok_concept", "hook"]}),
            "fact_check": (FactCheckAgent, {"confidence_threshold": 0.8}),
            "qa": (QAAgent, {"checklist": ["grammar", "brand_voice", "format", "links"]}),
            "publishing": (PublishingAgent, {"platforms": ["x", "facebook", "linkedin", "tiktok"]}),
            "analytics": (AnalyticsAgent, {"metrics": ["impressions", "engagement", "clicks", "conversions"]}),
            "optimisation": (OptimisationAgent, {"learning_rate": 0.1}),
            "reddit_intelligence": (RedditIntelligenceAgent, {"subreddits": [], "min_engagement": 10}),
            "x_intelligence": (XIntelligenceAgent, {"accounts_to_monitor": [], "hashtags": []}),
            "tiktok_intelligence": (TikTokIntelligenceAgent, {"hashtags": [], "creators": []}),
            "facebook_intelligence": (FacebookIntelligenceAgent, {"pages": [], "groups": []}),
            "linkedin_intelligence": (LinkedInIntelligenceAgent, {"hashtags": [], "companies": []}),
            "wordpress_intelligence": (WordPressIntelligenceAgent, {"site_url": "", "require_seo_check": True}),
            "wix_intelligence": (WixIntelligenceAgent, {"site_id": "", "site_url": "", "use_seo_wiz": True}),
        }
        
        for agent_id, (agent_class, config) in agents_config.items():
            agent = agent_class(config)
            self.orchestrator.register_agent(agent)
            self.tools[agent_id] = MCPTool(
                name=agent_id,
                description=agent.get_system_prompt()[:100],
                agent=agent,
                input_schema={"type": "object", "properties": {}}
            )
        
        # High-level workflow tools
        self.tools["create_campaign"] = MCPTool(
            name="create_campaign",
            description="Create a new content campaign",
            agent=self.orchestrator,
            input_schema={"type": "object", "properties": {"name": {"type": "string"}, "topic": {"type": "string"}, "platforms": {"type": "array", "items": {"type": "string"}}}, "required": ["name", "topic"]}
        )
        self.tools["run_agent"] = MCPTool(
            name="run_agent",
            description="Run a specific agent by ID",
            agent=self.orchestrator,
            input_schema={"type": "object", "properties": {"agent_id": {"type": "string"}, "input": {"type": "object"}}, "required": ["agent_id"]}
        )
    
    def run(self):
        """Run the FastAPI HTTP server."""
        uvicorn.run(self.app, host=self.host, port=self.port)
    
    async def stdio_serve(self):
        """Serve via stdio for Hermes MCP integration."""
        from mcp.server.mcpserver import MCPServer as MCPServerClass
        from mcp.types import TextContent, Tool
        
        mcp = MCPServerClass("content-generator-workforce")
        
        @mcp.tool()
        async def call_tool(tool: str, arguments: Dict[str, Any] = {}) -> str:
            if tool not in self.tools:
                return json.dumps({"error": f"Tool '{tool}' not found"})
            result = await self.tools[tool].execute(arguments)
            return json.dumps(result, indent=2)
        
        @mcp.tool()
        async def list_tools() -> str:
            return json.dumps([{"name": t.name, "description": t.description} for t in self.tools.values()])
        
        @mcp.tool()
        async def run_workflow(workflow_id: str, input_data: Dict = {}) -> str:
            result = await self.orchestrator.execute_workflow(workflow_id, input_data)
            return json.dumps(result, indent=2)
        
        @mcp.resource()
        async def agents() -> str:
            return json.dumps(self.orchestrator.get_agent_status(), indent=2)
        
        logger.info("Starting MCP stdio server...")
        await mcp.run_stdio()


def main():
    """Main entry point."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    
    server = MCPServer(port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)
    
    # Check if we should use stdio mode
    if "--stdio" in sys.argv or os.getenv("MCPSERVER_MODE") == "stdio":
        asyncio.run(server.stdio_serve())
    else:
        logger.info(f"Starting HTTP MCP server on {server.host}:{server.port}")
        server.run()


if __name__ == "__main__":
    import os
    main()