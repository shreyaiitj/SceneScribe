"""
Configuration File - 10/10 Version
All settings centralized. Includes toggles for all advanced features.
"""
import os
from dotenv import load_dotenv

load_dotenv(override=True)

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

MAX_FRAMES = 8
MIN_FRAME_INTERVAL_SECONDS = 2.0

ENABLE_DYNAMIC_FRAMES = True
MIN_FRAMES = 4
BASE_FRAMES = 8
MAX_FRAMES = 12
MOTION_THRESHOLD = 0.15

VISION_MODEL_NAME = os.environ.get("VISION_MODEL", "accounts/fireworks/models/kimi-k2p6")
TEXT_MODEL_NAME = os.environ.get("TEXT_MODEL", "accounts/fireworks/models/kimi-k2p5")
AUDIO_MODEL_NAME = os.environ.get("AUDIO_MODEL", "audio-whisper-large-v3")

FIREWORKS_BASE_URL = "https://api.fireworks.ai/inference/v1"
FIREWORKS_API_KEY_ENV_VAR = "FIREWORKS_API_KEY"

MAX_OUTPUT_TOKENS = 600
TEMPERATURE = 0.7
TIMEOUT_SECONDS = 600
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2.0

ENABLE_CONFIDENCE_SCORES = True
ENABLE_SELF_VERIFICATION = True
CONFIDENCE_THRESHOLD = 70
MAX_VERIFICATION_ATTEMPTS = 2

ENABLE_AUDIO = False

_api_key = os.environ.get(FIREWORKS_API_KEY_ENV_VAR)
if not _api_key:
    raise EnvironmentError(
        f"CRITICAL: Environment variable '{FIREWORKS_API_KEY_ENV_VAR}' is not set.\n"
        f"Please set it in your .env file for local testing, or ensure it is set in your Docker run command.\n"
        f"Your Docker command should include: -e FIREWORKS_API_KEY='fw_your_key'"
    )

FIREWORKS_API_KEY = _api_key

__all__ = [
    "INPUT_DIR", "OUTPUT_DIR", "INPUT_TASKS_FILE", "OUTPUT_RESULTS_FILE",
    "INPUT_TASKS_PATH", "OUTPUT_RESULTS_PATH",
    "MAX_FRAMES", "MIN_FRAME_INTERVAL_SECONDS",
    "ENABLE_DYNAMIC_FRAMES", "MIN_FRAMES", "BASE_FRAMES", "MAX_FRAMES",
    "MOTION_THRESHOLD",
    "VISION_MODEL_NAME", "TEXT_MODEL_NAME", "AUDIO_MODEL_NAME",
    "FIREWORKS_BASE_URL", "FIREWORKS_API_KEY_ENV_VAR",
    "MAX_OUTPUT_TOKENS", "TEMPERATURE", "TIMEOUT_SECONDS",
    "MAX_RETRIES", "RETRY_DELAY_SECONDS",
    "ENABLE_CONFIDENCE_SCORES", "ENABLE_SELF_VERIFICATION",
    "CONFIDENCE_THRESHOLD", "MAX_VERIFICATION_ATTEMPTS",
    "ENABLE_AUDIO",
    "FIREWORKS_API_KEY",
]

print(f"Config loaded. Vision: {VISION_MODEL_NAME} | Text: {TEXT_MODEL_NAME}")