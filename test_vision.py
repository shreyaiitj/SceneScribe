import os
from src.frame_extractor import extract_key_frames
from src.caption_engine import CaptionEngine

# 1. Provide a path to a real video file on your computer to test
video_path = r"C:\Users\Shreya\Downloads\6567877-uhd_4096_2160_25fps.mp4" 

print("Extracting frames...")
frames_b64 = extract_key_frames(video_path, max_frames=5)

print("Sending frames to the vision model...")
engine = CaptionEngine()
description = engine.generate_scene_description(frames_b64)

print("\n--- Scene Description Result ---")
print(description)