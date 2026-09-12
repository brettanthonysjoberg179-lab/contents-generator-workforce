from shared.base_agent import BaseAgent
from shared.database_manager import DatabaseManager
from agents.orchestrator.workflows import get_workflow
from typing import Any, Dict

class MasterOrchestrator(BaseAgent):
    """
    The brain of the workforce.
    Handles task decomposition, agent dispatch, and dependency resolution.
    """
    def __init__(self, db: DatabaseManager):
        super().__init__(name="MasterOrchestrator", role="Orchestrator")
        self.db = db
        self.load_skill("task_decomposition")
        self.load_skill("agent_dispatch")
        self.load_skill("dependency_resolution")
        self.agents = {}

    def register_agent(self, agent_id: str, agent: BaseAgent):
        self.agents[agent_id] = agent
        self.log(f"Registered agent: {agent_id}")

    def run(self, task_context: Dict[str, Any]) -> Any:
        self.log(f"Received task: {task_context.get('task_name')}")
        
        # New workflow-based logic
        workflow_id = task_context.get("workflow_id")
        if workflow_id:
            return self.execute_workflow(workflow_id, task_context)
        
        return {"status": "error", "message": "No workflow specified"}

    def execute_workflow(self, workflow_id: str, context: Dict[str, Any]) -> Any:
        workflow = get_workflow(workflow_id)
        if not workflow:
            return {"status": "error", "message": f"Workflow {workflow_id} not found"}

        self.log(f"Executing workflow: {workflow_id}")
        results = {}
        # Chainable context
        current_context = context.copy()
        
        for step in workflow:
            agent_id = step["agent_id"]
            
            # Combine original context with previous results
            step_context = current_context.copy()
            step_context.update(results)
            
            # Filter input based on input_key if defined
            if step["input_key"]:
                # If input_key is provided, extract only that from the combined context
                step_context = {step["input_key"]: step_context.get(step["input_key"])}
            
            step_result = self.dispatch(agent_id, step_context)
            results[step["step_name"]] = step_result
            
        return results

    def dispatch(self, agent_id: str, task_context: Dict[str, Any]) -> Any:
        if agent_id not in self.agents:
            self.log(f"Agent {agent_id} not found!")
            return {"status": "error", "message": "Agent not found"}
            
        self.log(f"Dispatching task to {agent_id}")
        return self.agents[agent_id].run(task_context)
