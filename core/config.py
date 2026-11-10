"""
Global configuration for the AI Shorts production project.

Project layout:
    AI_SHORTS/
        global/config.py
        assets/
        videos/
        output/

Project paths can be overridden with environment variables for Kaggle or
local execution. Importing this module does not create directories.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

GLOBAL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = GLOBAL_DIR.parent

ASSETS_DIR = PROJECT_ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
SVG_DIR = ASSETS_DIR / "svg"
BACKGROUNDS_DIR = ASSETS_DIR / "backgrounds"
GLOBAL_AUDIO_DIR = ASSETS_DIR / "audio"

VIDEOS_DIR = PROJECT_ROOT / "videos"
OUTPUT_DIR = Path(os.getenv("AI_SHORTS_OUTPUT_DIR", str(PROJECT_ROOT / "output")))
WORK_DIR = Path(os.getenv("AI_SHORTS_WORK_DIR", str(PROJECT_ROOT / "work")))


# ---------------------------------------------------------------------------
# Video defaults
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class VideoDefaults:
    """Technical defaults shared by all videos."""

    width: int = 1080
    height: int = 1920
    fps: int = 30

    video_codec: str = "libx264"
    audio_codec: str = "aac"
    audio_sample_rate: int = 44100
    audio_channels: int = 2
    pixel_format: str = "yuv420p"

    # Logical Manim scene dimensions, not pixel dimensions.
    manim_frame_height: float = 14.0
    manim_frame_width: float = 14.0 * 9.0 / 16.0

    @property
    def aspect_ratio(self) -> str:
        return f"{self.width}:{self.height}"


VIDEO = VideoDefaults(
    width=int(os.getenv("AI_SHORTS_WIDTH", "1080")),
    height=int(os.getenv("AI_SHORTS_HEIGHT", "1920")),
    fps=int(os.getenv("AI_SHORTS_FPS", "30")),
)


# ---------------------------------------------------------------------------
# Audio defaults
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AudioDefaults:
    """Defaults for narration and final audio mixing."""

    tts_provider: str = "edge_tts"
    tts_voice: str = "en-US-ChristopherNeural"
    tts_rate: str = "+10%"
    tts_pitch: str = "+0Hz"
    tts_volume: str = "+0%"

    sample_rate: int = 44100
    narration_gain_db: float = 0.0
    music_gain_db: float = -24.0
    sound_effects_gain_db: float = -10.0
    fade_out_seconds: float = 1.5


AUDIO = AudioDefaults()


# ---------------------------------------------------------------------------
# Rendering defaults
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RenderDefaults:
    """Defaults for Manim rendering and production behaviour."""

    renderer: str = "cairo"
    quality: str = os.getenv("AI_SHORTS_MANIM_QUALITY", "medium_quality")
    background_color: str = "#080D19"
    preview_quality: str = "low_quality"
    final_quality: str = "high_quality"
    max_repair_attempts: int = 2


RENDER = RenderDefaults()


# ---------------------------------------------------------------------------
# Subtitle defaults
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SubtitleDefaults:
    """Subtitle layout defaults."""

    enabled: bool = True
    max_lines: int = 2
    max_characters_per_line: int = 38
    font_size: int = 48
    bottom_safe_margin: int = 260
    outline_width: int = 3


SUBTITLES = SubtitleDefaults()


# ---------------------------------------------------------------------------
# Runtime helpers
# ---------------------------------------------------------------------------

def ensure_project_directories() -> None:
    """Create shared directories only when explicitly requested."""
    directories = (
        ASSETS_DIR,
        FONTS_DIR,
        SVG_DIR,
        BACKGROUNDS_DIR,
        GLOBAL_AUDIO_DIR,
        VIDEOS_DIR,
        OUTPUT_DIR,
        WORK_DIR,
    )
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def _validate_video_id(video_id: str) -> None:
    """Reject empty names and path traversal."""
    if not video_id or video_id in {".", ".."}:
        raise ValueError("video_id must be a non-empty directory name")
    if any(char in video_id for char in ("/", "\\", "\0")):
        raise ValueError(f"Invalid video_id: {video_id!r}")


def video_dir(video_id: str) -> Path:
    """Return a video's project directory without creating it."""
    _validate_video_id(video_id)
    return VIDEOS_DIR / video_id


def video_output_dir(video_id: str) -> Path:
    """Return a video's output directory without creating it."""
    return video_dir(video_id) / "output"


def get_ffmpeg_executable() -> str:
    """Return FFmpeg's executable name/path, with optional override."""
    return os.getenv("FFMPEG_BIN", "ffmpeg")


def get_ffprobe_executable() -> str:
    """Return FFprobe's executable name/path, with optional override."""
    return os.getenv("FFPROBE_BIN", "ffprobe")


if __name__ == "__main__":
    # Running this file directly creates shared folders and prints the setup.
    ensure_project_directories()
    print(f"Project root : {PROJECT_ROOT}")
    print(f"Assets       : {ASSETS_DIR}")
    print(f"Videos       : {VIDEOS_DIR}")
    print(f"Output       : {OUTPUT_DIR}")
    print(f"Work         : {WORK_DIR}")
    print(f"Video        : {VIDEO.width}x{VIDEO.height} @ {VIDEO.fps} fps")
    print(f"Audio voice  : {AUDIO.tts_voice}")
