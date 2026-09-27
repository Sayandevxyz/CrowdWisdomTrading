import logging
import sys
from rich.console import Console
from rich.logging import RichHandler

console = Console()

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure structured, elegant terminal logging with Rich."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                show_time=False,
                show_path=False,
                markup=True
            )
        ]
    )
    logger = logging.getLogger("crowdwisdom_studio")
    logger.setLevel(level)
    return logger

logger = setup_logging()

def log_agent(agent_name: str, message: str, level: str = "info") -> None:
    """Emit formatted agent message conforming to spec: [AgentName] message."""
    color_map = {
        "Orchestrator": "bold magenta",
        "AdsManager": "bold cyan",
        "AdResearch": "cyan",
        "MarketingAnalysis": "bold yellow",
        "PainPointAgent": "bold red",
        "ICPAgent": "bold blue",
        "DataAgent": "bold green",
        "CreativeDirector": "bold magenta",
        "ScriptAgent": "bold yellow",
        "StoryboardAgent": "bold cyan",
        "VideoAgent": "bold red",
        "QAAgent": "bold green",
    }
    color = color_map.get(agent_name, "bold white")
    text = f"[{color}][{agent_name}][/{color}] {message}"
    console.print(text)
