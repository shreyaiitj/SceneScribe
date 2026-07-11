"""
Configuration File - Optimized for Judge Evaluation
"""
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Paths
if os.path.exists("/.dockerenv") or os.path.isdir("/input") or os.path.isdir("/output"):
    INPUT_DIR = "/input"
    OUTPUT_DIR = "/output"
else:
    INPUT_DIR = "input"
    OUTPUT_DIR = "output"

INPUT_TASKS_FILE = "tasks.json"
OUTPUT_RESULTS_FILE = "results.json"
INPUT_TASKS_PATH = os.path.join(INPUT_DIR, INPUT_TASKS_FILE)
OUTPUT_RESULTS_PATH = os.path.join(OUTPUT_DIR, OUTPUT_RESULTS_FILE)

# Video Processing
MAX_FRAMES = 8
MIN_FRAME_INTERVAL_SECONDS = 2.0

# Dynamic Frame Budget
ENABLE_DYNAMIC_FRAMES = True
MIN_FRAMES = 4
BASE_FRAMES = 8
MAX_FRAMES = 8
MOTION_THRESHOLD = 0.1

# ============================================
# 🔥 USE FIREWORKS FOR EVERYTHING
# ============================================
# Vision model (Qwen2.5-VL for video understanding)
VISION_MODEL_NAME = os.environ.get("VISION_MODEL", "accounts/fireworks/models/qwen2.5-32b-vl")
# Fallback vision models (if the above fails, try one of these)
# VISION_MODEL_NAME = "accounts/fireworks/models/llava-v1.5-13b"
# VISION_MODEL_NAME = "accounts/fireworks/models/pixtral-12b"

# Text model (for final captions)
TEXT_MODEL_NAME = os.environ.get("TEXT_MODEL", "accounts/fireworks/models/deepseek-v4-pro")

AUDIO_MODEL_NAME = os.environ.get("AUDIO_MODEL", "audio-whisper-large-v3")

FIREWORKS_BASE_URL = "https://api.fireworks.ai/inference/v1"
FIREWORKS_API_KEY_ENV_VAR = "FIREWORKS_API_KEY"

# API Settings
MAX_OUTPUT_TOKENS = 1024
TEMPERATURE = 0.7
TIMEOUT_SECONDS = 300
MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 1.0

# Confidence & Verification
ENABLE_CONFIDENCE_SCORES = True
ENABLE_SELF_VERIFICATION = True
CONFIDENCE_THRESHOLD = 70
MAX_VERIFICATION_ATTEMPTS = 1

# Audio - DISABLED
ENABLE_AUDIO = False

# API Key - Fireworks ONLY
FIREWORKS_API_KEY = os.environ.get("FIREWORKS_API_KEY")
if not FIREWORKS_API_KEY:
    print("⚠️ WARNING: FIREWORKS_API_KEY not found in environment!")
    print("Using fallback captions only.")
else:
    print(f"Config loaded. Vision: {VISION_MODEL_NAME} | Text: {TEXT_MODEL_NAME}")