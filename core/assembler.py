"""Assemble rendered animation, narration, optional music and subtitles with FFmpeg."""
from pathlib import Path
import subprocess
from .config import (AUDIO_BITRATE, AUDIO_CODEC, PIXEL_FORMAT, VIDEO_CODEC,
                     VIDEO_CRF, VIDEO_FPS, VIDEO_PRESET, get_ffmpeg_executable, log_progress)

def assemble_video(video_path: str | Path, narration_path: str | Path,
                   output_path: str | Path, music_path: str | Path | None = None,
                   subtitles_path: str | Path | None = None) -> Path:
    video, narration, output = Path(video_path), Path(narration_path), Path(output_path)
    for required in (video, narration):
        if not required.is_file():
            raise FileNotFoundError(required)
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [get_ffmpeg_executable(), "-y", "-i", str(video), "-i", str(narration)]
    if music_path is not None:
        music = Path(music_path)
        if not music.is_file():
            raise FileNotFoundError(music)
        cmd += ["-stream_loop", "-1", "-i", str(music)]
        cmd += ["-filter_complex", "[1:a]volume=1.0[n];[2:a]volume=0.16[m];[n][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
                "-map", "0:v:0", "-map", "[a]"]
    else:
        cmd += ["-map", "0:v:0", "-map", "1:a:0"]
    if subtitles_path is not None:
        subtitles = Path(subtitles_path)
        if not subtitles.is_file():
            raise FileNotFoundError(subtitles)
        escaped = str(subtitles).replace("\\", "/").replace(":", r"\\:").replace("'", r"\\'")
        cmd += ["-vf", f"subtitles='{escaped}'"]
    cmd += ["-r", str(VIDEO_FPS), "-c:v", VIDEO_CODEC, "-preset", VIDEO_PRESET,
            "-crf", str(VIDEO_CRF), "-pix_fmt", PIXEL_FORMAT,
            "-c:a", AUDIO_CODEC, "-b:a", AUDIO_BITRATE, "-movflags", "+faststart", str(output)]
    log_progress("Starting FFmpeg assembly.", "ASSEMBLER")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        log_progress(result.stderr[-2500:], "ASSEMBLER")
        raise RuntimeError("FFmpeg assembly failed.")
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("FFmpeg did not create a valid output.")
    log_progress(f"Created {output} ({output.stat().st_size:,} bytes).", "ASSEMBLER")
    return output
