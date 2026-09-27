import os
import shutil
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load .env file if available
load_dotenv()

def get_default_ffmpeg_path() -> str:
    """Find system ffmpeg or fallback to imageio-ffmpeg bundled binary."""
    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        return sys_ffmpeg
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

class Settings(BaseModel):
    """Global configuration settings for CrowdWisdom AI Creative Studio."""
    
    # LLM Settings
    llm_provider: str = Field(default_factory=lambda: os.getenv("LLM_PROVIDER", "openrouter").lower())
    openrouter_api_key: str = Field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    openrouter_model: str = Field(default_factory=lambda: os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-70b-instruct"))
    nvidia_api_key: str = Field(default_factory=lambda: os.getenv("NVIDIA_API_KEY", ""))
    nvidia_model: str = Field(default_factory=lambda: os.getenv("NVIDIA_MODEL", "meta/llama-3.1-70b-instruct"))
    
    # Research APIs
    apify_api_token: str = Field(default_factory=lambda: os.getenv("APIFY_API_TOKEN", ""))
    tavily_api_key: str = Field(default_factory=lambda: os.getenv("TAVILY_API_KEY", ""))
    exa_api_key: str = Field(default_factory=lambda: os.getenv("EXA_API_KEY", ""))
    
    # Video & Media Rendering
    openmontage_path: str = Field(default_factory=lambda: os.getenv("OPENMONTAGE_PATH", ""))
    ffmpeg_path: str = Field(default_factory=lambda: os.getenv("FFMPEG_PATH") or get_default_ffmpeg_path())
    
    # Application Config
    output_dir: Path = Field(default_factory=lambda: Path(os.getenv("OUTPUT_DIR", ".")).resolve())
    cache_enabled: bool = Field(default_factory=lambda: os.getenv("CACHE_ENABLED", "true").lower() in ("true", "1", "yes"))
    research_days: int = Field(default_factory=lambda: int(os.getenv("RESEARCH_DAYS", "30")))
    max_competitor_ads: int = Field(default_factory=lambda: int(os.getenv("MAX_COMPETITOR_ADS", "20")))

    # Directory Paths
    @property
    def research_dir(self) -> Path:
        p = self.output_dir / "research"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def analysis_dir(self) -> Path:
        p = self.output_dir / "analysis"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def scripts_dir(self) -> Path:
        p = self.output_dir / "scripts"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def storyboards_dir(self) -> Path:
        p = self.output_dir / "storyboards"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def videos_dir(self) -> Path:
        p = self.output_dir / "videos"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def final_dir(self) -> Path:
        p = self.output_dir / "final"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def reports_dir(self) -> Path:
        p = self.output_dir / "reports"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def data_dir(self) -> Path:
        p = self.output_dir / "data"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def approved_data_dir(self) -> Path:
        p = self.data_dir / "approved"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def cache_dir(self) -> Path:
        p = self.data_dir / "cache"
        p.mkdir(parents=True, exist_ok=True)
        return p

    def init_directories(self) -> None:
        """Create all project directories if not present."""
        _ = self.research_dir
        _ = self.analysis_dir
        _ = self.scripts_dir
        _ = self.storyboards_dir
        _ = self.videos_dir
        _ = self.final_dir
        _ = self.reports_dir
        _ = self.approved_data_dir
        _ = self.cache_dir
        (self.data_dir / "raw").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "processed").mkdir(parents=True, exist_ok=True)

# Global singleton
settings = Settings()
