#!/usr/bin/env python3
import sys
import os
import concurrent.futures
import traceback

from src.config import FIREWORKS_API_KEY, ENABLE_AUDIO
from src.task_loader import get_all_tasks
from src.video_downloader import download_video
from src.frame_extractor import extract_key_frames
from src.caption_engine import CaptionEngine
from src.audio_extractor import extract_audio_track
from src.output_writer import save_results
from src.utils import _log_info, _log_error, _log_success

def process_single_task(task, engine):
    task_id = task.get("task_id", "unknown")
    video_url = task.get("video_url")
    styles = task.get("styles", [])
    
    _log_info(f"Processing task {task_id}...")
    
    video_path = None
    audio_path = None
    
    try:
        video_path = download_video(video_url)
        if not video_path:
            raise Exception("Video download failed.")
        
        audio_transcript = None
        if ENABLE_AUDIO:
            audio_path = extract_audio_track(video_path)
            if audio_path:
                audio_transcript = engine.transcribe_audio(audio_path)
        else:
            _log_info("Audio transcription disabled.")
        
        frames_b64 = extract_key_frames(video_path, max_frames=None)
        if not frames_b64:
            raise Exception("Frame extraction failed (no frames returned).")
        
        scene_description = engine.generate_scene_description(frames_b64)
        _log_info(f"Scene description: {scene_description[:100]}...")
        
        all_captions = engine.generate_all_captions(scene_description, audio_transcript)
        
        filtered_captions = {
            style: all_captions[style] 
            for style in styles 
            if style in all_captions
        }
        
        _log_success(f"Task {task_id} completed successfully.")
        return {
            "task_id": task_id,
            "captions": filtered_captions
        }
        
    except Exception as e:
        _log_error(f"Task {task_id} failed: {e}")
        _log_error(traceback.format_exc())
        
        fallback_captions = {
            "formal": "Error processing video content.",
            "sarcastic": "Great, another broken video format.",
            "humorous_tech": "404: Visual data stream corrupted.",
            "humorous_non_tech": "Something went wrong behind the scenes!"
        }
        filtered_fallback = {
            style: fallback_captions[style] 
            for style in styles 
            if style in fallback_captions
        }
        return {
            "task_id": task_id,
            "captions": filtered_fallback
        }
    
    finally:
        if video_path and os.path.exists(video_path):
            try:
                os.unlink(video_path)
            except:
                pass
        if audio_path and os.path.exists(audio_path):
            try:
                os.unlink(audio_path)
            except:
                pass

def main() -> int:
    _log_info("=" * 60)
    _log_info("AMD Hackathon: Video Captioning Agent (Track 2) - 10/10")
    _log_info("Using Gemma with Histogram Scene Detection")
    _log_info("Audio Transcription: Whisper (Fireworks AI)")
    _log_info("Concurrent Processing: Up to 3 videos at once")
    _log_info("Confidence-Aware Captions + Self-Verification")
    _log_info("=" * 60)

    if not FIREWORKS_API_KEY:
        _log_error("FIREWORKS_API_KEY environment variable is not set!")
        _log_error("Please set it in your .env file for local testing.")
        _log_error("The hackathon judges will inject this automatically.")
        return 1

    tasks = get_all_tasks()
    if not tasks:
        _log_error("No tasks loaded. Exiting.")
        return 1

    _log_info(f"Loaded {len(tasks)} tasks. Starting concurrent processing...")

    engine = CaptionEngine()
    final_results = []

    MAX_WORKERS = 3
    
    _log_info(f"Using {MAX_WORKERS} concurrent workers...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_task = {
            executor.submit(process_single_task, task, engine): task 
            for task in tasks
        }
        
        for future in concurrent.futures.as_completed(future_to_task):
            try:
                result = future.result(timeout=120)
                final_results.append(result)
                _log_success(f"Collected result for task: {result['task_id']}")
            except concurrent.futures.TimeoutError:
                _log_error("A task timed out after 120 seconds.")
            except Exception as e:
                _log_error(f"Unexpected error in future: {e}")

    _log_info("\n" + "=" * 60)
    _log_info(f"All tasks processed. Saving {len(final_results)} results...")
    
    if save_results(final_results):
        _log_success("Pipeline execution completed successfully!")
        return 0
    else:
        _log_error("Failed to save results.")
        return 1

if __name__ == "__main__":
    sys.exit(main())