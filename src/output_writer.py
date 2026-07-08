import os
import json
import tempfile
import shutil
from typing import List, Dict, Any

from src.config import OUTPUT_RESULTS_PATH
from src.utils import _log_info, _log_error, _log_warning, _log_success
from src.utils import validate_result_structure

def save_results(results: List[Dict[str, Any]], file_path: str = OUTPUT_RESULTS_PATH) -> bool:
    output_dir = os.path.dirname(file_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    if not validate_result_structure(results):
        _log_error("Cannot save: invalid result structure.")
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
            json.dump(results, tmp_file, indent=4, ensure_ascii=False)
            tmp_path = tmp_file.name

        shutil.move(tmp_path, file_path)
        _log_success(f"Results successfully saved to {file_path}")
        return True

    except Exception as e:
        _log_error(f"Failed to save results: {e}")
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return False

__all__ = ["save_results"]