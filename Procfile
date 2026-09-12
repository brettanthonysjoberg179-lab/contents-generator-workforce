# Content Generator Workforce — Process Definitions
# Usage: honcho start
#        honcho start workforce  # Start just the MCP server
#        honcho start all       # Start everything

# Main MCP Server (FastAPI)
workforce: python3 run_workforce.py

# Optional: Health check server
health: python3 scripts/health_check.py

# Optional: Background worker for async tasks
worker: python3 -c "from agents.orchestrator.agent import MasterOrchestrator; o = MasterOrchestrator(); o.run_background()"
