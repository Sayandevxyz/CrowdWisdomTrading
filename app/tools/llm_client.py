import asyncio
import json
import time
from typing import Any, Dict, List, Optional, Type, TypeVar
import httpx
from pydantic import BaseModel, ValidationError

from app.config import settings
from app.logging_config import logger
from app.tools.cache import cache
from app.utils.json_utils import extract_json_from_text, repair_json_string

T = TypeVar("T", bound=BaseModel)

class UsageTracker:
    """Tracks token and request metrics across the campaign."""
    def __init__(self):
        self.total_requests: int = 0
        self.prompt_tokens: int = 0
        self.completion_tokens: int = 0
        self.estimated_cost_usd: float = 0.0

    def add_usage(self, prompt_tokens: int, completion_tokens: int, cost: float = 0.0):
        self.total_requests += 1
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.estimated_cost_usd += cost

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

usage_tracker = UsageTracker()

class LLMClient:
    """Unified client for OpenRouter and NVIDIA Build API with structured Pydantic validation."""

    def __init__(self):
        self.provider = settings.llm_provider
        self.last_call_time = 0.0
        self.min_interval = 0.2  # Basic rate limit delay

    def _get_api_config(self) -> Dict[str, str]:
        if self.provider == "nvidia":
            return {
                "base_url": "https://integrate.api.nvidia.com/v1/chat/completions",
                "api_key": settings.nvidia_api_key,
                "model": settings.nvidia_model or "meta/llama-3.1-70b-instruct"
            }
        # default to openrouter
        return {
            "base_url": "https://openrouter.ai/api/v1/chat/completions",
            "api_key": settings.openrouter_api_key,
            "model": settings.openrouter_model or "anthropic/claude-3.5-sonnet"
        }

    async def _rate_limit(self):
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_interval:
            await asyncio.sleep(self.min_interval - elapsed)
        self.last_call_time = time.time()

    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        use_cache: bool = True
    ) -> str:
        """Call LLM API with exponential backoff and caching."""
        cfg = self._get_api_config()
        api_key = cfg["api_key"]
        
        # Check cache
        cache_payload = {
            "provider": self.provider,
            "model": cfg["model"],
            "messages": messages,
            "temperature": temperature
        }
        if use_cache:
            cached = cache.get("llm_completion", cache_payload)
            if cached:
                return cached.get("content", "")

        # Fallback if no valid key is provided
        if not api_key or "your_" in api_key.lower():
            logger.warning(f"No active API key configured for {self.provider}. Using deterministic agent reasoning.")
            return ""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        if self.provider == "openrouter":
            headers["HTTP-Referer"] = "https://github.com/CrowdWisdomTrading"
            headers["X-Title"] = "CrowdWisdom AI Creative Studio"

        payload = {
            "model": cfg["model"],
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Exponential backoff retry loop
        max_retries = 3
        backoff = 2.0
        for attempt in range(max_retries):
            try:
                await self._rate_limit()
                async with httpx.AsyncClient(timeout=60.0) as client:
                    resp = await client.post(cfg["base_url"], headers=headers, json=payload)
                    resp.raise_for_status()
                    data = resp.json()
                    
                    content = data["choices"][0]["message"]["content"]
                    usage = data.get("usage", {})
                    p_tokens = usage.get("prompt_tokens", len(str(messages)) // 4)
                    c_tokens = usage.get("completion_tokens", len(content) // 4)
                    
                    # Estimate cost ($0.003 / 1k tokens approx)
                    est_cost = ((p_tokens + c_tokens) / 1000.0) * 0.003
                    usage_tracker.add_usage(p_tokens, c_tokens, est_cost)

                    if use_cache:
                        cache.set("llm_completion", cache_payload, {"content": content})
                    return content
            except Exception as e:
                logger.warning(f"LLM request attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(backoff ** attempt)
        return ""

    async def generate_structured(
        self,
        messages: List[Dict[str, str]],
        response_model: Type[T],
        temperature: float = 0.5,
        max_retries: int = 2
    ) -> T:
        """Enforce strict Pydantic model response with automatic repair and fallback."""
        schema_json = json.dumps(response_model.model_json_schema(), indent=2)
        system_instruction = (
            f"\n\nCRITICAL INSTRUCTION: You MUST return a strictly valid JSON object matching this schema:\n"
            f"{schema_json}\n"
            f"DO NOT include markdown explanations outside the JSON. Return only the raw JSON or wrapped in ```json ```."
        )
        
        augmented_messages = list(messages)
        augmented_messages[-1] = {
            "role": augmented_messages[-1]["role"],
            "content": augmented_messages[-1]["content"] + system_instruction
        }

        raw_output = await self.generate_completion(augmented_messages, temperature=temperature)
        
        # If no LLM output (e.g. offline / mock / demo), caller handles fallback
        if not raw_output:
            raise ValueError(f"Empty LLM output for schema {response_model.__name__}")

        # Try parsing
        cleaned_json = extract_json_from_text(raw_output)
        repaired_json = repair_json_string(cleaned_json)
        
        try:
            parsed_dict = json.loads(repaired_json)
            return response_model.model_validate(parsed_dict)
        except (json.JSONDecodeError, ValidationError) as err:
            logger.warning(f"Structured validation failed for {response_model.__name__}: {err}. Attempting repair.")
            # Repair attempt
            repair_messages = [
                {"role": "system", "content": "You are a JSON repair specialist. Output ONLY valid parseable JSON adhering to the specified schema."},
                {"role": "user", "content": f"The following output was invalid:\n{raw_output}\n\nSchema:\n{schema_json}\n\nFix it and output ONLY valid JSON."}
            ]
            repair_output = await self.generate_completion(repair_messages, temperature=0.1)
            repaired_clean = repair_json_string(extract_json_from_text(repair_output))
            parsed_repaired = json.loads(repaired_clean)
            return response_model.model_validate(parsed_repaired)

llm_client = LLMClient()
