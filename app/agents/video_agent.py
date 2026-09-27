from pathlib import Path
from typing import List, Optional

from app.agents.base_agent import HermesAgent
from app.config import settings
from app.schemas.storyboard import Storyboard
from app.schemas.video import RenderResult
from app.tools.video_renderer import video_renderer
from app.utils.json_utils import load_json

class VideoAgent(HermesAgent):
    """Autonomous Video Producer rendering cinematic 9:16 vertical MP4 video advertisements."""

    def __init__(self):
        super().__init__(name="VideoAgent", prompt_file="video.txt")
        self.register_tool("video_renderer", video_renderer)

    async def render_concept_video(
        self,
        storyboard: Storyboard,
        render_quality: str = "standard"
    ) -> RenderResult:
        """Render storyboard shots into an MP4 file with audio, voiceover, and color grading."""
        self.log(f"Rendering {storyboard.concept_id}: {storyboard.title}")
        output_mp4 = settings.videos_dir / f"{storyboard.concept_id}.mp4"
        
        result = await video_renderer.render_storyboard(
            storyboard=storyboard,
            output_mp4=output_mp4,
            render_quality=render_quality
        )
        
        if result.is_valid:
            self.log(f"Rendered {output_mp4.name} ({result.duration:.1f}s, {result.resolution}, Audio: {result.has_audio})")
        else:
            self.log(f"Rendering failed for {storyboard.concept_id}: {result.error}", level="error")
        return result

    async def run(
        self,
        storyboards: Optional[List[Storyboard]] = None,
        concept_filter: Optional[int] = None,
        render_quality: str = "standard"
    ) -> List[RenderResult]:
        """Execute video production for all or selected concepts."""
        self.log("Starting video production pipeline")

        # Load from disk if not provided
        if not storyboards:
            storyboards = []
            for cid in ["concept_01", "concept_02", "concept_03"]:
                sb_path = settings.storyboards_dir / f"{cid}.json"
                if sb_path.exists():
                    data = load_json(sb_path)
                    storyboards.append(Storyboard.model_validate(data))

        # Filter if single concept requested
        if concept_filter is not None:
            cid_target = f"concept_{concept_filter:02d}"
            storyboards = [sb for sb in storyboards if sb.concept_id == cid_target]
            self.log(f"Filtering to single target concept: {cid_target}")

        results: List[RenderResult] = []
        for sb in storyboards:
            res = await self.render_concept_video(sb, render_quality=render_quality)
            results.append(res)

        return results

video_agent = VideoAgent()
