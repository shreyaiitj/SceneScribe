import os
import json
import base64
import tempfile
import shutil
from typing import List, Dict, Any, Optional
import sys

def _safe_print(prefix: str, msg: str):
    full_msg = f"{prefix} {msg}"
    try:
        print(full_msg)
    except UnicodeEncodeError:
        try:
            print(full_msg.encode('ascii', errors='replace').decode('ascii'))
        except Exception:
            pass

def _log_info(msg: str):
    _safe_print("[INFO]", msg)

def _log_warning(msg: str):
    _safe_print("[WARNING]", msg)

def _log_error(msg: str):
    _safe_print("[ERROR]", msg)

def _log_success(msg: str):
    _safe_print("[SUCCESS]", msg)

def load_tasks(file_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(file_path):
        _log_error(f"Task file not found at {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as e:
        _log_error(f"Invalid JSON in {file_path}: {e}")
        return []
    except Exception as e:
        _log_error(f"Unexpected error reading {file_path}: {e}")
        return []

    if isinstance(raw_data, dict):
        tasks = raw_data.get("tasks", [])
    elif isinstance(raw_data, list):
        tasks = raw_data
    else:
        _log_error(f"Unexpected JSON structure in {file_path}. Expected list or dict with 'tasks' key.")
        return []

    if not tasks:
        _log_warning("No tasks found in the input file.")
        return []

    validated_tasks = []
    required_keys = {"task_id", "video_url", "styles"}

    for idx, task in enumerate(tasks):
        missing_keys = required_keys - set(task.keys())
        if missing_keys:
            _log_warning(f"Task {idx} is missing required keys: {missing_keys}. Skipping.")
            continue

        if not isinstance(task["styles"], list):
            _log_warning(f"Task {idx} has 'styles' that is not a list. Skipping.")
            continue

        if not isinstance(task["task_id"], str):
            _log_warning(f"Task {idx} has 'task_id' that is not a string. Converting to string.")
            task["task_id"] = str(task["task_id"])

        if not isinstance(task["video_url"], str) or not task["video_url"].startswith(("http://", "https://")):
            _log_warning(f"Task {idx} has invalid video_url. Skipping.")
            continue

        validated_tasks.append(task)

    _log_info(f"Loaded and validated {len(validated_tasks)} tasks from {len(tasks)} total entries.")
    return validated_tasks

def save_output(file_path: str, data: List[Dict[str, Any]]) -> bool:
    output_dir = os.path.dirname(file_path)
    if output_dir:
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            _log_error(f"Failed to create output directory {output_dir}: {e}")
            return False

    try:
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            dir=output_dir,
            prefix='.tmp_',
            suffix='.json',
            delete=False
        ) as tmp_file:
            json.dump(data, tmp_file, indent=4, ensure_ascii=False)
            tmp_path = tmp_file.name

        shutil.move(tmp_path, file_path)

        _log_success(f"Results successfully saved to {file_path}")
        return True

    except json.JSONEncodeError as e:
        _log_error(f"Failed to serialize data to JSON: {e}")
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return False
    except Exception as e:
        _log_error(f"Unexpected error saving output: {e}")
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return False

def encode_image_to_base64(image_path: str) -> str:
    try:
        with open(image_path, "rb") as image_file:
            encoded_bytes = base64.b64encode(image_file.read())
            return encoded_bytes.decode('utf-8')
    except FileNotFoundError:
        _log_error(f"Image file not found: {image_path}")
        return ""
    except Exception as e:
        _log_error(f"Error encoding image {image_path}: {e}")
        return ""

def encode_bytes_to_base64(image_bytes: bytes) -> str:
    if not image_bytes:
        _log_error("Received empty image bytes.")
        return ""
    try:
        encoded_bytes = base64.b64encode(image_bytes)
        return encoded_bytes.decode('utf-8')
    except Exception as e:
        _log_error(f"Error encoding image bytes: {e}")
        return ""

def validate_result_structure(results: List[Dict[str, Any]]) -> bool:
    if not results:
        _log_warning("Results list is empty.")
        return True

    valid_caption_styles = {"formal", "sarcastic", "humorous_tech", "humorous_non_tech"}

    for idx, entry in enumerate(results):
        if "task_id" not in entry or not isinstance(entry["task_id"], str):
            _log_error(f"Result {idx} is missing a valid 'task_id'.")
            return False

        if "captions" not in entry or not isinstance(entry["captions"], dict):
            _log_error(f"Result {idx} is missing a 'captions' dictionary.")
            return False

        captions = entry["captions"]
        if not captions:
            _log_error(f"Result {idx} 'captions' dict is empty.")
            return False

        for style in captions.keys():
            if style not in valid_caption_styles:
                _log_error(f"Result {idx} has invalid style: {style}")
                return False
            if not isinstance(captions[style], str):
                _log_error(f"Result {idx} has '{style}' caption that is not a string.")
                return False

    _log_success(f"All {len(results)} results are structurally valid.")
    return True

__all__ = [
    "load_tasks", "save_output", "encode_image_to_base64",
    "encode_bytes_to_base64", "validate_result_structure",
    "_log_info", "_log_error", "_log_warning", "_log_success"
]