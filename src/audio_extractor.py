import subprocess
import os
from typing import Optional
from src.utils import _log_info, _log_error, _log_success

def extract_audio_track(video_path: str) -> Optional[str]:
    _log_info("Extracting audio track from video...")
    audio_path = video_path.replace(".mp4", "_audio.mp3")
    try:
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-q:a', '0',
            '-map', 'a',
            audio_path,
            '-y'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            _log_success(f"Audio extracted successfully: {audio_path}")
            return audio_path
        else:
            _log_info("No audio channel found or extraction failed.")
            if os.path.exists(audio_path):
                os.unlink(audio_path)
            return None
    except Exception as e:
        _log_error(f"Error during audio extraction: {e}")
        if os.path.exists(audio_path):
            os.unlink(audio_path)
        return None
