from typing import Optional
from pydantic import BaseModel, Field

class RenderJob(BaseModel):
    """Specification of a video rendering job."""
    concept_id: str
    storyboard_id: str
    target_resolution: str = "1080x1920"
    fps: int = 30
    duration: float
    output_path: str
    audio_enabled: bool = True
    voiceover_enabled: bool = True

class RenderResult(BaseModel):
    """Output metrics and verification from VideoAgent rendering."""
    concept_id: str
    output_path: str
    duration: float
    resolution: str
    fps: int = 30
    has_audio: bool
    is_valid: bool
    renderer_used: str
    error: Optional[str] = None
