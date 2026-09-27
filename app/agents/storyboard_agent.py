from pathlib import Path
from typing import List

from app.agents.base_agent import HermesAgent
from app.config import settings
from app.schemas.scripts import Script
from app.schemas.storyboard import Shot, Storyboard
from app.utils.json_utils import save_json

class StoryboardAgent(HermesAgent):
    """Autonomous Storyboard Artist generating 12-25 dynamic shots per commercial script."""

    def __init__(self):
        super().__init__(name="StoryboardAgent", prompt_file="storyboard.txt")

    def build_storyboard_for_script(self, script: Script) -> Storyboard:
        """Deconstruct 7 script scenes into 14-18 fast-paced cinematic shots."""
        shots: List[Shot] = []
        shot_counter = 1

        for scene in script.scenes:
            # Subdivide scene into 2 distinct cinematic shots (wide + macro, or tension + reaction)
            dur_1 = round(scene.duration * 0.45, 1)
            dur_2 = round(scene.duration * 0.55, 1)

            # Shot A: Environmental setup or action
            s1 = Shot(
                shot_id=f"S{shot_counter:02d}",
                duration=dur_1,
                description=f"{scene.on_screen_text or scene.visual[:40]} - Action",
                visual_prompt=(
                    f"Cinematic vertical 9:16 video frame, {scene.visual}. "
                    f"Anamorphic lens flares, volumetric atmospheric lighting, photorealistic 8k octane render."
                ),
                camera_motion=scene.camera,
                lens="35mm Anamorphic T1.5 prime",
                lighting="Moody volumetric cyan and deep amber with sharp rim illumination",
                environment="Dim trading sanctuary with subtle floating luminescent UI reflections",
                subject="Lone focused trader immersed in real-time market data",
                voiceover=scene.voiceover[:len(scene.voiceover)//2] if scene.voiceover else "",
                sfx=scene.sound_design,
                music=scene.music,
                transition=scene.transition
            )
            shots.append(s1)
            shot_counter += 1

            # Shot B: Macro detail or emotional reaction
            s2 = Shot(
                shot_id=f"S{shot_counter:02d}",
                duration=dur_2,
                description=f"{scene.on_screen_text or scene.action[:40]} - Detail",
                visual_prompt=(
                    f"Extreme close-up macro cinematography, 9:16 vertical orientation. "
                    f"Detail of screen interface displaying CrowdWisdom metrics, subtle camera drift, soft bokeh background."
                ),
                camera_motion="Slow cinematic push-in with micro-vibrations",
                lens="85mm Macro f/1.8",
                lighting="High-contrast edge lighting reflecting across glass surfaces",
                environment="Modern institutional trading station with glowing telemetry",
                subject="Tactile interaction with financial intelligence interface",
                voiceover=scene.voiceover[len(scene.voiceover)//2:].strip() if scene.voiceover else "",
                sfx=scene.sound_design,
                music=scene.music,
                transition="Cut"
            )
            shots.append(s2)
            shot_counter += 1

        total_dur = round(sum(s.duration for s in shots), 1)
        return Storyboard(
            concept_id=script.concept_id,
            title=script.title,
            aspect_ratio="9:16",
            resolution="1080x1920",
            total_duration=total_dur,
            shots=shots
        )

    async def run(self, scripts: List[Script]) -> List[Storyboard]:
        """Convert all scripts into production-ready storyboards."""
        storyboards: List[Storyboard] = []
        for s in scripts:
            self.log(f"Building storyboard for {s.concept_id} ({len(s.scenes)} scenes)")
            sb = self.build_storyboard_for_script(s)
            self.log(f"Built {len(sb.shots)} shots for {s.concept_id} (Duration: {sb.total_duration}s)")
            output_file = settings.storyboards_dir / f"{s.concept_id}.json"
            save_json(output_file, sb)
            storyboards.append(sb)
            self.log(f"Saved {s.concept_id}.json to storyboards/")
        return storyboards

storyboard_agent = StoryboardAgent()
