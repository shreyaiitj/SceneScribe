import os
from typing import List, Dict, Any

from src.utils import load_tasks, _log_info, _log_success, _log_warning, _log_error
from src.config import INPUT_TASKS_PATH, INPUT_DIR, INPUT_TASKS_FILE

def resolve_tasks_path(custom_path: str = None) -> str:
    if custom_path:
        _log_info(f"Using custom tasks path: {custom_path}")
        return custom_path

    if os.path.exists(INPUT_TASKS_PATH):
        _log_info(f"Using config path: {INPUT_TASKS_PATH}")
        return INPUT_TASKS_PATH

    local_path = "input/tasks.json"
    if os.path.exists(local_path):
        _log_info(f"Using local fallback path: {local_path}")
        return local_path

    _log_warning(f"No tasks file found. Defaulting to: {INPUT_TASKS_PATH}")
    return INPUT_TASKS_PATH

def get_all_tasks(custom_path: str = None) -> List[Dict[str, Any]]:
    file_path = resolve_tasks_path(custom_path)
    _log_info(f"Loading tasks from: {file_path}")

    tasks = load_tasks(file_path)

    if not tasks:
        _log_warning(f"No tasks loaded from {file_path}. Please verify the file exists and contains valid data.")
        return []

    task_ids = [task.get("task_id", "UNKNOWN") for task in tasks]
    total_styles = sum(len(task.get("styles", [])) for task in tasks)
    
    _log_success(f"Successfully loaded {len(tasks)} tasks.")
    _log_info(f"Task IDs: {', '.join(task_ids)}")
    _log_info(f"Total caption styles to generate: {total_styles}")

    if tasks:
        sample = tasks[0]
        _log_info(f"Sample task: {sample.get('task_id')} -> styles: {sample.get('styles', [])}")

    return tasks

__all__ = [
    "get_all_tasks",
    "resolve_tasks_path",
]