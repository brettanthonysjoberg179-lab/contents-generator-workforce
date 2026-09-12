"""LLM-powered agent base class using Ollama."""
import logging
from typing import Any, Dict, List, Optional

from shared.base_agent import BaseAgent
from shared.ollama_client import OllamaClient, make_tool

logger = logging.getLogger("llm_agent")


class LLMAgent(BaseAgent):
    """Agent powered by Ollama LLM with tool calling support."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model = config.get("model", "llama3.2:latest")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 4096)
        self.ollama = OllamaClient()
        self._tools: List[Dict] = []

    def set_tools(self, tools: List[Dict]) -> None:
        """Set available tools for this agent."""
        self._tools = tools

    async def think(self, prompt: str, system: str = None) -> str:
        """Send a prompt and get text response."""
        return await self.ollama.generate(
            prompt=prompt,
            model=self.model,
            system=system or self.get_system_prompt(),
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

    async def think_with_tools(self, prompt: str, tools: List[Dict] = None) -> Dict[str, Any]:
        """Send a prompt with tools and get response + tool calls."""
        return await self.ollama.tool_call(
            prompt=prompt,
            tools=tools or self._tools,
            model=self.model,
            system=self.get_system_prompt(),
        )

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """Chat with the model."""
        result = await self.ollama.chat(
            messages=messages,
            model=self.model,
            tools=self._tools,
        )
        return result.get("message", {}).get("content", "")

    async def structured_output(self, prompt: str, schema: Dict) -> Dict[str, Any]:
        """Get structured JSON output matching a schema."""
        import json
        schema_str = json.dumps(schema, indent=2)
        full_prompt = f"""{prompt}

Respond with valid JSON matching this schema:
{schema_str}

JSON response:"""

        response = await self.think(full_prompt)
        # Extract JSON from response
        try:
            # Find JSON in response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON from response: {response[:100]}")

        return {"raw_response": response, "parsed": False}

    async def close(self):
        """Close the Ollama client."""
        await self.ollama.close()
