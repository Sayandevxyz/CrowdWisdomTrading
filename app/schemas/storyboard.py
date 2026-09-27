from typing import List
from pydantic import BaseModel, Field

class Shot(BaseModel):
    """Detailed visual shot specification for generative video production."""
    shot_id: str = Field(description="e.g. S01, S02")
    duration: float = Field(ge=0.5, le=10.0, description="Shot duration in seconds")
    description: str
    visual_prompt: str = Field(description="Detailed generative prompt for visual synthesis")
    camera_motion: str
    lens: str
    lighting: str
    environment: str
    subject: str
    voiceover: str = ""
    sfx: str = ""
    music: str = ""
    transition: str = "cut"

class Storyboard(BaseModel):
    """Production-ready storyboard containing 12-25 dynamic shots."""
    concept_id: str
    title: str
    aspect_ratio: str = "9:16"
    resolution: str = "1080x1920"
    total_duration: float
    shots: List[Shot]
