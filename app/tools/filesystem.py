from pathlib import Path
from typing import Union
from app.config import settings

def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure a directory exists and return Path object."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def get_artifact_path(category: str, filename: str) -> Path:
    """Get absolute path to an artifact according to category."""
    mapping = {
        "research": settings.research_dir,
        "analysis": settings.analysis_dir,
        "scripts": settings.scripts_dir,
        "storyboards": settings.storyboards_dir,
        "videos": settings.videos_dir,
        "final": settings.final_dir,
        "reports": settings.reports_dir,
        "approved": settings.approved_data_dir,
        "cache": settings.cache_dir,
    }
    target_dir = mapping.get(category, settings.output_dir / category)
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / filename
