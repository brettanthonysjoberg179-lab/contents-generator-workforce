#!/usr/bin/env python3
"""Main entry point for the Content Generator Workforce."""
import asyncio
import logging
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from mcp_server.main import MCPServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("workforce")

def main():
    """Run the workforce."""
    logger.info("=" * 60)
    logger.info("  Content Generator Workforce")
    logger.info("  20+ AI Agents for Content Marketing")
    logger.info("=" * 60)
    
    # Get config from environment
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))
    
    # Create and run server
    server = MCPServer(host=host, port=port)
    
    logger.info(f"Starting MCP server on {host}:{port}")
    logger.info(f"Registered {len(server.tools)} tools")
    logger.info(f"Registered {len(server.orchestrator.agents)} agents")
    logger.info("")
    logger.info("Available endpoints:")
    logger.info("  GET  /health     - Health check")
    logger.info("  GET  /tools      - List all MCP tools")
    logger.info("  POST /tools/call - Call a specific tool")
    logger.info("  POST /workflows/run - Run a workflow")
    logger.info("  GET  /agents     - List all agents")
    logger.info("")
    
    server.run()

if __name__ == "__main__":
    main()
