"""Content Generator Workforce — shared package init."""
from shared.base_agent import BaseAgent
from shared.ollama_client import OllamaClient, make_tool
from shared.composio_client import ComposioClient
from shared.llm_agent import LLMAgent

__version__ = "1.0.0"
__all__ = ["BaseAgent", "OllamaClient", "make_tool", "ComposioClient", "LLMAgent"]