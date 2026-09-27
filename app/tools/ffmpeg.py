import asyncio
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.config import settings
from app.logging_config import logger

class FFmpegTool:
    """Wrapper for executing FFmpeg operations and media inspection."""

    def __init__(self, ffmpeg_path: Optional[str] = None):
        self.ffmpeg_path = ffmpeg_path or settings.ffmpeg_path

    async def run_command(self, args: List[str]) -> Tuple[int, str, str]:
        """Execute ffmpeg command asynchronously and return exit code, stdout, stderr."""
        cmd = [self.ffmpeg_path] + args
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return proc.returncode, stdout.decode("utf-8", errors="ignore"), stderr.decode("utf-8", errors="ignore")

    def run_command_sync(self, args: List[str]) -> Tuple[int, str, str]:
        """Execute ffmpeg synchronously."""
        cmd = [self.ffmpeg_path] + args
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode, result.stdout, result.stderr

    def probe_video(self, file_path: Path) -> Dict[str, Any]:
        """Inspect video file properties using ffmpeg."""
        if not file_path.exists():
            return {"valid": False, "error": "File does not exist"}

        # Use ffmpeg -i to probe format info
        cmd = [self.ffmpeg_path, "-i", str(file_path)]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        info_text = result.stderr

        duration = 0.0
        width = 0
        height = 0
        has_audio = "Audio:" in info_text

        # Parse duration
        import re
        dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", info_text)
        if dur_match:
            hours, minutes, seconds = dur_match.groups()
            duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)

        # Parse resolution
        res_match = re.search(r",\s*(\d{3,4})x(\d{3,4})", info_text)
        if res_match:
            width = int(res_match.group(1))
            height = int(res_match.group(2))

        return {
            "valid": duration > 0 and (width > 0 or "Video:" in info_text),
            "duration": round(duration, 2),
            "resolution": f"{width}x{height}" if width else "1080x1920",
            "width": width,
            "height": height,
            "has_audio": has_audio,
            "file_size_bytes": file_path.stat().st_size
        }

    async def normalize_audio_and_mux(
        self,
        video_input: Path,
        voiceover_audio: Optional[Path],
        music_audio: Optional[Path],
        output_path: Path,
        target_duration: float
    ) -> bool:
        """Combine video with mixed voiceover and background music with audio ducking."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        args = ["-y", "-i", str(video_input)]
        filter_complex = []
        input_count = 1

        if voiceover_audio and voiceover_audio.exists():
            args.extend(["-i", str(voiceover_audio)])
            vo_idx = input_count
            input_count += 1
        else:
            vo_idx = None

        if music_audio and music_audio.exists():
            args.extend(["-i", str(music_audio)])
            music_idx = input_count
            input_count += 1
        else:
            music_idx = None

        # Build audio filter
        if vo_idx is not None and music_idx is not None:
            # Duck music volume to 25%, keep VO at 100%
            filter_complex = [
                f"[{vo_idx}:a]volume=1.0[vo];"
                f"[{music_idx}:a]volume=0.22,aloop=loop=-1:size=2e+09[bgm];"
                f"[vo][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
            ]
            args.extend([
                "-filter_complex", "".join(filter_complex),
                "-map", "0:v",
                "-map", "[aout]",
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-t", str(target_duration),
                str(output_path)
            ])
        elif vo_idx is not None:
            args.extend([
                "-map", "0:v",
                "-map", f"{vo_idx}:a",
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-t", str(target_duration),
                str(output_path)
            ])
        elif music_idx is not None:
            args.extend([
                "-map", "0:v",
                "-map", f"{music_idx}:a",
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-t", str(target_duration),
                str(output_path)
            ])
        else:
            # Generate silent audio stream to guarantee playable valid audio track
            args.extend([
                "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                "-t", str(target_duration),
                str(output_path)
            ])

        code, out, err = await self.run_command(args)
        if code != 0:
            logger.error(f"FFmpeg audio mux failed: {err}")
            return False
        return True

ffmpeg_tool = FFmpegTool()
