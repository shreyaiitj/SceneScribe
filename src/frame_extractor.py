import os
import cv2
import base64
import subprocess
import numpy as np
from typing import List, Tuple, Optional

from src.config import (
    MAX_FRAMES, MIN_FRAMES, BASE_FRAMES, 
    ENABLE_DYNAMIC_FRAMES, MOTION_THRESHOLD
)
from src.utils import _log_info, _log_error, _log_warning, _log_success

def get_video_duration(video_path: str) -> float:
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        duration = float(result.stdout.strip())
        return max(duration, 1.0)
    except Exception as e:
        _log_warning(f"Could not get video duration, assuming 10 seconds: {e}")
        return 10.0

def extract_frames_at_timestamps(video_path: str, timestamps: List[float]) -> List[np.ndarray]:
    frames = []
    for ts in timestamps:
        try:
            cmd = [
                'ffmpeg',
                '-ss', str(ts),
                '-i', video_path,
                '-vframes', '1',
                '-f', 'image2pipe',
                '-vcodec', 'mjpeg',
                'pipe:1'
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0 and len(result.stdout) > 0:
                img_array = np.frombuffer(result.stdout, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                if img is not None and img.size > 0:
                    frames.append(img)
                else:
                    _log_warning(f"Failed to decode frame at {ts}s")
            else:
                _log_warning(f"FFmpeg failed at {ts}s: {result.stderr[:100]}")
        except Exception as e:
            _log_warning(f"Error extracting frame at {ts}s: {e}")
    return frames

def calculate_motion_score(video_path: str, sample_duration: float = 5.0) -> float:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return 0.5
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    
    total_frames_to_analyze = int(fps * sample_duration)
    frame_count = 0
    prev_gray = None
    motion_scores = []
    
    while frame_count < total_frames_to_analyze:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            mean_diff = np.mean(diff) / 255.0
            motion_scores.append(mean_diff)
        
        prev_gray = gray
        frame_count += 1
    
    cap.release()
    
    if not motion_scores:
        return 0.5
    
    avg_motion = min(1.0, sum(motion_scores) / len(motion_scores))
    return avg_motion

def get_dynamic_frame_count(video_path: str, duration: float) -> int:
    if not ENABLE_DYNAMIC_FRAMES:
        return BASE_FRAMES
    
    if duration < 10.0:
        return MIN_FRAMES
    
    motion = calculate_motion_score(video_path)
    _log_info(f"Motion score: {motion:.2f}")
    
    if duration > 60.0 or motion > MOTION_THRESHOLD:
        return MAX_FRAMES
    
    return BASE_FRAMES

def calculate_histogram_similarity(img1: np.ndarray, img2: np.ndarray) -> float:
    if img1 is None or img2 is None:
        return 0.0
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
    
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return max(0.0, min(1.0, similarity))

def select_key_frames(frames: List[np.ndarray], max_frames: int = 8) -> List[np.ndarray]:
    if not frames:
        return []
    
    if len(frames) <= max_frames:
        return frames
    
    selected = [frames[0]]
    threshold = 0.65
    
    for i in range(1, len(frames)):
        similarity = calculate_histogram_similarity(frames[i], selected[-1])
        if similarity < threshold:
            selected.append(frames[i])
    
    if len(selected) > max_frames:
        indices = np.linspace(0, len(selected) - 1, max_frames, dtype=int)
        selected = [selected[i] for i in indices]
    
    if len(selected) < max_frames and len(frames) >= max_frames:
        indices = np.linspace(0, len(frames) - 1, max_frames, dtype=int)
        selected = [frames[i] for i in indices]
    
    _log_info(f"Selected {len(selected)} key frames out of {len(frames)} candidates.")
    return selected[:max_frames]

def extract_key_frames(video_path: str, max_frames: int = None) -> List[str]:
    _log_info(f"Extracting key frames from video: {video_path}")

    frames = []
    timestamps = []
    
    duration = get_video_duration(video_path)
    _log_info(f"Video duration: {duration:.2f} seconds")
    
    if max_frames is None:
        max_frames = get_dynamic_frame_count(video_path, duration)
    _log_info(f"Frame budget: {max_frames} (dynamic)")
    
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("OpenCV VideoCapture failed to open video.")

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 10.0
        _log_info(f"Video duration: {duration:.2f} seconds, FPS: {fps:.2f}")

        sample_count = max(32, max_frames * 3)
        frame_step = max(1, total_frames // sample_count)

        candidate_frames = []
        candidate_timestamps = []

        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if count % frame_step == 0:
                candidate_frames.append(frame)
                candidate_timestamps.append(count / fps if fps > 0 else 0.0)
            
            count += 1
        
        cap.release()

        if len(candidate_frames) > 0:
            _log_info(f"Read {len(candidate_frames)} candidate frames with OpenCV.")
            selected_frames = select_key_frames(candidate_frames, max_frames)
            frames = selected_frames
        else:
            raise Exception("No frames read from VideoCapture.")

    except Exception as e:
        _log_warning(f"OpenCV reader failed ({e}). Falling back to FFmpeg...")
        duration = get_video_duration(video_path)
        num_candidates = min(16, max(4, int(duration / 2)))
        timestamps = [min(duration - 0.1, max(0.0, (i / num_candidates) * duration)) for i in range(num_candidates)]
        candidate_frames = extract_frames_at_timestamps(video_path, timestamps)
        frames = select_key_frames(candidate_frames, max_frames)

    if not frames:
        _log_error("No frames could be extracted from the video.")
        black_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        _, buffer = cv2.imencode('.jpg', black_frame)
        return [base64.b64encode(buffer).decode('utf-8')]

    frames_b64 = []
    for img in frames:
        h, w = img.shape[:2]
        if max(h, w) > 1024:
            scale = 1024 / max(h, w)
            new_w, new_h = int(w * scale), int(h * scale)
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
        frames_b64.append(base64.b64encode(buffer).decode('utf-8'))

    _log_success(f"Extracted {len(frames_b64)} key frames successfully.")
    return frames_b64

__all__ = ["extract_key_frames"]