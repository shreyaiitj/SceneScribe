#!/usr/bin/env python3
import os
from dotenv import load_dotenv
load_dotenv(override=True)

import sys
import signal
import traceback

def timeout_handler(signum, frame):
    print("[ERROR] Global timeout triggered after 9 minutes. Exiting.")
    sys.exit(1)

if hasattr(signal, 'SIGALRM'):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(540)

from src.task_loader import get_all_tasks
from src.video_downloader import download_video
from src.frame_extractor import extract_key_frames
from src.caption_engine import CaptionEngine
from src.output_writer import save_results
from src.utils import _log_info, _log_error, _log_success, _log_warning
import os as _os

def main() -> int:
    results = []
    tasks = []
    
    try:
        tasks = get_all_tasks()
    except Exception as e:
        _log_error(f"Failed to load tasks: {e}")
        traceback.print_exc()

    if not tasks:
        _log_warning("No tasks found or failed to load tasks. Writing empty results file.")
        save_results([])
        return 0

    try:
        engine = CaptionEngine()
    except Exception as e:
        _log_error(f"Failed to initialize CaptionEngine: {e}")
        traceback.print_exc()
        class DummyEngine:
            def generate_scene_description(self, frames): return "Fallback description due to engine initialization failure."
            def generate_all_captions(self, desc, audio=None): return {
                "formal": "Failed to initialize engine.",
                "sarcastic": "Failed to initialize engine.",
                "humorous_tech": "Failed to initialize engine.",
                "humorous_non_tech": "Failed to initialize engine."
            }
        engine = DummyEngine()

    for task in tasks:
        task_id = task.get("task_id", "UNKNOWN")
        requested_styles = task.get("styles", ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"])
        video_path = None
        try:
            video_url = task.get("video_url")
            if not video_url:
                raise Exception("Missing video_url")
                
            video_path = download_video(video_url)
            if not video_path:
                raise Exception("Video download failed")

            frames_b64 = extract_key_frames(video_path)
            scene_description = engine.generate_scene_description(frames_b64)
            captions = engine.generate_all_captions(scene_description)

            # only keep requested styles
            filtered = {k: v for k, v in captions.items() if k in requested_styles}
            results.append({"task_id": task_id, "captions": filtered})
            _log_success(f"Completed task {task_id}")

        except Exception as e:
            _log_error(f"Task {task_id} failed: {e}")
            traceback.print_exc()
            
            fallback_caps = {
                "formal": "Processing failed.",
                "sarcastic": "Processing failed.",
                "humorous_tech": "Processing failed.",
                "humorous_non_tech": "Processing failed."
            }
            filtered_fallback = {k: v for k, v in fallback_caps.items() if k in requested_styles}
            
            results.append({
                "task_id": task_id,
                "captions": filtered_fallback
            })
        finally:
            if video_path and _os.path.exists(video_path):
                try:
                    _os.unlink(video_path)
                except Exception:
                    pass

    try:
        ok = save_results(results)
        return 0 if ok else 1
    except Exception as e:
        _log_error(f"Critical error saving results: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    if "PORT" in os.environ:
        import uvicorn
        from server import app
        port = int(os.environ.get("PORT", 8000))
        print(f"[INFO] PORT environment variable detected. Launching FastAPI server on port {port}...")
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        sys.exit(main())