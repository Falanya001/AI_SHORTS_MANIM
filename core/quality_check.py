"""Basic MP4 integrity, dimension, duration and audio checks using ffprobe."""
import json
import subprocess
from pathlib import Path
from .config import VIDEO_HEIGHT, VIDEO_WIDTH, get_ffprobe_executable, log_progress

def inspect_video(video_path: str | Path) -> dict:
    path = Path(video_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    cmd = [get_ffprobe_executable(), "-v", "error", "-show_entries",
           "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate",
           "-of", "json", str(path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"ffprobe failed: {result.stderr[-1500:]}")
    data = json.loads(result.stdout)
    log_progress(f"Inspected {path.name}.", "QC")
    return data

def quality_check(video_path: str | Path, expected_width: int = VIDEO_WIDTH,
                  expected_height: int = VIDEO_HEIGHT, minimum_duration: float = 1.0):
    metadata = inspect_video(video_path)
    streams = metadata.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    errors = []
    if not videos:
        errors.append("No video stream found.")
    else:
        v = videos[0]
        if (v.get("width"), v.get("height")) != (expected_width, expected_height):
            errors.append(f"Wrong dimensions: {v.get('width')}x{v.get('height')}.")
    if not audios:
        errors.append("No audio stream found.")
    duration = float(metadata.get("format", {}).get("duration", 0))
    if duration < minimum_duration:
        errors.append(f"Duration too short: {duration:.2f}s.")
    passed = not errors
    log_progress("QC PASSED." if passed else "QC FAILED: " + " ".join(errors), "QC")
    return passed, errors, metadata
