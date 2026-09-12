"""Ollama LLM client for agent workforce."""
import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, AsyncGenerator

import httpx

logger = logging.getLogger("ollama_client")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")


class OllamaClient:
    """Async Ollama API client with tool calling support."""

    def __init__(self, base_url: str = OLLAMA_HOST, default_model: str = DEFAULT_MODEL):
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=120.0)

    async def list_models(self) -> List[Dict[str, Any]]:
        """List available models."""
        resp = await self._client.get("/api/tags")
        resp.raise_for_status()
        return resp.json().get("models", [])

    async def generate(
        self,
        prompt: str,
        model: str = None,
        system: str = None,
        temperature: float = 0.7,
        max_tokens: int = None,
        stream: bool = False,
    ) -> str:
        """Generate text from a prompt."""
        payload = {
            "model": model or self.default_model,
            "prompt": prompt,
            "stream": stream,
            "options": {"temperature": temperature},
        }
        if system:
            payload["system"] = system
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        if stream:
            return self._stream_generate(payload)

        resp = await self._client.post("/api/generate", json=payload)
        resp.raise_for_status()
        return resp.json().get("response", "")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        tools: List[Dict] = None,
        temperature: float = 0.7,
        format: str = None,
    ) -> Dict[str, Any]:
        """Chat with the model, optionally with tools."""
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if tools:
            payload["tools"] = tools
        if format:
            payload["format"] = format

        resp = await self._client.post("/api/chat", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def tool_call(
        self,
        prompt: str,
        tools: List[Dict],
        model: str = None,
        system: str = None,
    ) -> Dict[str, Any]:
        """Send prompt with available tools, return tool calls or text."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        result = await self.chat(messages, model=model, tools=tools)
        message = result.get("message", {})

        # Check if model made tool calls
        if message.get("tool_calls"):
            return {
                "type": "tool_calls",
                "content": message.get("content", ""),
                "tool_calls": message["tool_calls"],
            }

        return {
            "type": "text",
            "content": message.get("content", ""),
            "tool_calls": [],
        }

    async def _stream_generate(self, payload: Dict) -> str:
        """Handle streaming generation."""
        full_text = ""
        async with self._client.stream("POST", "/api/generate", json=payload) as resp:
            async for line in resp.aiter_lines():
                if line:
                    chunk = json.loads(line)
                    full_text += chunk.get("response", "")
                    if chunk.get("done"):
                        break
        return full_text

    async def close(self):
        """Close the client."""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Tool schema helper
def make_tool(name: str, description: str, parameters: Dict) -> Dict:
    """Create an OpenAI-compatible tool schema for Ollama."""
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": parameters,
            },
        },
    }
