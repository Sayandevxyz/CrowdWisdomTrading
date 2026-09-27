import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel

from app.config import settings
from app.logging_config import log_agent, logger
from app.tools.llm_client import llm_client

T = TypeVar("T", bound=BaseModel)

class HermesAgent:
    """Base autonomous agent class following Hermes Agent Framework architecture."""

    def __init__(self, name: str, prompt_file: Optional[str] = None):
        self.name = name
        self.prompt_file = prompt_file
        self.system_prompt = self._load_system_prompt()
        self.tools: Dict[str, Any] = {}

    def _load_system_prompt(self) -> str:
        """Load system prompt from app/prompts/ directory."""
        if not self.prompt_file:
            return f"You are {self.name}, an autonomous agent in the CrowdWisdom AI Creative Studio."
        
        prompt_path = Path(__file__).resolve().parent.parent / "prompts" / self.prompt_file
        if prompt_path.exists():
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return f"You are {self.name}."

    def register_tool(self, name: str, tool_callable: Any):
        """Bind tool to agent."""
        self.tools[name] = tool_callable

    def log(self, message: str, level: str = "info"):
        """Emit formatted log message conforming to spec: [AgentName] message."""
        log_agent(self.name, message, level)

    async def execute_structured_reasoning(
        self,
        user_prompt: str,
        response_model: Type[T],
        temperature: float = 0.5,
        context: Optional[Dict[str, Any]] = None
    ) -> T:
        """Execute reasoning loop with structured Pydantic output validation."""
        context_str = ""
        if context:
            import json
            context_str = f"\n\nCONTEXT:\n{json.dumps(context, indent=2, default=str)}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"{user_prompt}{context_str}"}
        ]

        try:
            return await llm_client.generate_structured(
                messages=messages,
                response_model=response_model,
                temperature=temperature
            )
        except Exception as e:
            logger.warning(f"[{self.name}] LLM invocation notice: {e}. Executing verified domain reasoning.")
            raise
