import sys
import traceback
from src.task_loader import get_all_tasks
from src.video_downloader import download_video
from src.frame_extractor import extract_key_frames
from src.caption_engine import CaptionEngine
from src.output_writer import save_results

def run_test():
    print("Getting tasks...")
    tasks = get_all_tasks()
    print("Tasks:", tasks)
    if not tasks:
        return
        
    task = tasks[0]
    print("Downloading video from:", task["video_url"])
    video_path = download_video(task["video_url"])
    print("Downloaded video path:", video_path)
    if not video_path:
        print("Failed to download video!")
        return
        
    print("Extracting frames...")
    try:
        frames_b64 = extract_key_frames(video_path)
        print(f"Extracted {len(frames_b64)} frames.")
    except Exception as e:
        print("Frame extraction failed!")
        traceback.print_exc()
        return
        
    print("Initializing engine...")
    engine = CaptionEngine()
    
    print("Generating scene description...")
    try:
        scene_description = engine.generate_scene_description(frames_b64)
        print("Scene description:", scene_description)
    except Exception as e:
        print("Scene description generation failed!")
        traceback.print_exc()
        return
        
    print("Generating captions...")
    try:
        captions = engine.generate_all_captions(scene_description)
        print("Captions:", captions)
    except Exception as e:
        print("Caption generation failed!")
        traceback.print_exc()
        return

if __name__ == "__main__":
    run_test()
