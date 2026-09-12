"""Master Orchestrator — the operating system of the workforce."""
import asyncio
import logging
from typing import Any, Dict, List

from shared.base_agent import BaseAgent

class MasterOrchestrator(BaseAgent):
    agent_id = "orchestrator"
    name = "Master Orchestrator"
    upstream_agents = []
    downstream_agents = []  # Will be populated dynamically
    allowed_tools = ["ollama", "mcp", "composio", "airtable", "obsidian", "google_drive", "filesystem", "scheduler", "git"]
    read_permissions = ["*"]
    write_permissions = ["*"]

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config.get("name", "Master Orchestrator"), config.get("role", "orchestrator"))
        self.agents: Dict[str, BaseAgent] = {}
        self.completed_agents: List[str] = []
        self.workflow_history: List[Dict[str, Any]] = []

    def register_agent(self, agent: BaseAgent) -> None:
        self.agents[agent.agent_id] = agent
        if agent.agent_id not in self.downstream_agents:
            self.downstream_agents.append(agent.agent_id)

    async def execute_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info(f"Starting workflow: {workflow_id}")
        order = self._topological_sort()
        results, errors = {}, []
        
        for agent_id in order:
            agent = self.agents.get(agent_id)
            if not agent or not agent.validate_dependencies(self.completed_agents):
                continue
            try:
                agent.update_status("running")
                context = {f"{d}_output": results.get(d) for d in agent.upstream_agents if d in results}
                context.update({"workflow_id": workflow_id, "global_input": input_data})
                results[agent_id] = await agent.execute(context)
                self.completed_agents.append(agent_id)
                agent.update_status("completed")
            except Exception as e:
                agent.update_status("failed")
                errors.append({"agent_id": agent_id, "error": str(e)})
                if agent.config.get("fail_fast", False):
                    break
        
        return {"workflow_id": workflow_id, "results": results, "errors": errors, "completed": len(self.completed_agents), "total": len(self.agents)}

    def _topological_sort(self) -> List[str]:
        visited, order = set(), []
        def visit(aid):
            if aid in visited:
                return
            visited.add(aid)
            agent = self.agents.get(aid)
            if agent:
                for dep in agent.upstream_agents:
                    visit(dep)
                order.append(aid)
        for aid in self.agents:
            visit(aid)
        return order

    async def execute(self, context: Dict[str, Any]) -> Any:
        return await self.execute_workflow(context.get("workflow_id", "default"), context.get("input", {}))

    def get_system_prompt(self) -> str:
        return "You are the Master Orchestrator. Coordinate agents, enforce dependencies, manage state."

    def get_agent_status(self) -> List[Dict[str, Any]]:
        return [a.get_capabilities() for a in self.agents.values()]

    def run(self, task_context: Dict[str, Any]) -> Any:
        """Execute the orchestrator's task."""
        workflow_id = task_context.get("workflow_id", "default")
        input_data = task_context.get("input", {})
        import asyncio
        return asyncio.run(self.execute_workflow(workflow_id, input_data))
