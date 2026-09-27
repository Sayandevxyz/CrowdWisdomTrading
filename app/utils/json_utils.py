import json
import re
from pathlib import Path
from typing import Any, Union
from pydantic import BaseModel

def extract_json_from_text(text: str) -> str:
    """Extract clean JSON string from LLM responses containing markdown fences or commentary."""
    text = text.strip()
    
    # Try finding markdown code fences first
    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text)
    if match:
        candidate = match.group(1).strip()
        if (candidate.startswith("{") and candidate.endswith("}")) or (candidate.startswith("[") and candidate.endswith("]")):
            return candidate

    # Find outermost curly or square braces
    start_curly = text.find("{")
    start_bracket = text.find("[")
    
    if start_curly != -1 and (start_bracket == -1 or start_curly < start_bracket):
        end_curly = text.rfind("}")
        if end_curly != -1 and end_curly > start_curly:
            return text[start_curly:end_curly + 1]
    elif start_bracket != -1:
        end_bracket = text.rfind("]")
        if end_bracket != -1 and end_bracket > start_bracket:
            return text[start_bracket:end_bracket + 1]
            
    return text

def repair_json_string(json_str: str) -> str:
    """Attempt basic repairs for LLM JSON irregularities like trailing commas."""
    # Remove trailing commas before closing braces/brackets
    repaired = re.sub(r",\s*([\]}])", r"\1", json_str)
    return repaired

def save_json(file_path: Union[str, Path], data: Any, indent: int = 2) -> None:
    """Save data or Pydantic model to a JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if isinstance(data, BaseModel):
        content = data.model_dump(mode="json")
    elif hasattr(data, "dict"):
        content = data.dict()
    else:
        content = data
        
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=indent, ensure_ascii=False)

def load_json(file_path: Union[str, Path]) -> Any:
    """Load JSON from file path."""
    path = Path(file_path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
