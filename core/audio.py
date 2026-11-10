"""Edge TTS narration generation and MP3 duration helper."""
from __future__ import annotations
import asyncio
from pathlib import Path
from mutagen.mp3 import MP3
from .config import TTS_RATE, TTS_VOICE, TTS_VOLUME, TTS_PITCH, log_progress

async def _edge_save(text: str, output: Path, voice: str, rate: str, volume: str, pitch: str):
    try:
        import edge_tts
    except ImportError as exc:
        raise RuntimeError("Install edge-tts: pip install edge-tts") from exc
    await edge_tts.Communicate(text, voice, rate=rate, volume=volume, pitch=pitch).save(str(output))

def generate_narration(text: str, output_path: str | Path, voice: str = TTS_VOICE,
                       rate: str = TTS_RATE, volume: str = TTS_VOLUME,
                       pitch: str = TTS_PITCH) -> Path:
    if not text.strip():
        raise ValueError("Narration text is empty.")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    log_progress(f"Generating narration: {output.name}", "AUDIO")
    asyncio.run(_edge_save(text, output, voice, rate, volume, pitch))
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("TTS produced no usable audio file.")
    log_progress(f"Saved narration ({output.stat().st_size:,} bytes).", "AUDIO")
    return output

def get_audio_duration(audio_path: str | Path) -> float:
    path = Path(audio_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    duration = float(MP3(path).info.length)
    log_progress(f"Audio duration: {duration:.2f}s", "AUDIO")
    return duration
