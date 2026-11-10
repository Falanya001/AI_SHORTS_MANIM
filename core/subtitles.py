"""Write subtitle timing data as an SRT file."""
from pathlib import Path
from typing import Iterable
from .config import log_progress

def _stamp(seconds: float) -> str:
    ms = max(0, round(seconds * 1000))
    hours, ms = divmod(ms, 3_600_000)
    minutes, ms = divmod(ms, 60_000)
    secs, millis = divmod(ms, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def write_srt(segments: Iterable[dict], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    cues = []
    for index, item in enumerate(segments, 1):
        start, end = float(item["start"]), float(item["end"])
        caption = str(item["text"]).strip()
        if not caption:
            continue
        if start < 0 or end <= start:
            raise ValueError(f"Invalid timing in subtitle cue {index}.")
        cues.append(f"{len(cues)+1}\n{_stamp(start)} --> {_stamp(end)}\n{caption}\n")
    if not cues:
        raise ValueError("No valid subtitle segments supplied.")
    output.write_text("\n".join(cues), encoding="utf-8")
    log_progress(f"Wrote {len(cues)} subtitle cues to {output}.", "SUBTITLES")
    return output
