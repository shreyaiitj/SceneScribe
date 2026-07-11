import os
import json
import tempfile
import shutil
from typing import List, Dict, Any

from src.config import OUTPUT_RESULTS_PATH
from src.utils import _log_info, _log_error, _log_warning, _log_success
from src.utils import validate_result_structure

def save_results(results: List[Dict[str, Any]], file_path: str = OUTPUT_RESULTS_PATH) -> bool:
    candidate_paths = [
        file_path,
        "output/results.json",
        "results.json"
    ]
    
    seen = set()
    unique_paths = []
    for p in candidate_paths:
        abs_p = os.path.abspath(p)
        if abs_p not in seen:
            seen.add(abs_p)
            unique_paths.append(p)
            
    success = False
    
    if not validate_result_structure(results):
        _log_error("Cannot save: invalid result structure.")
        return False

    for path in unique_paths:
        try:
            output_dir = os.path.dirname(path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with tempfile.NamedTemporaryFile(
                mode='w',
                encoding='utf-8',
                dir=output_dir if output_dir else ".",
                prefix='.tmp_',
                suffix='.json',
                delete=False
            ) as tmp_file:
                json.dump(results, tmp_file, indent=4, ensure_ascii=False)
                tmp_path = tmp_file.name

            shutil.move(tmp_path, path)
            _log_success(f"Results successfully saved to {path}")
            success = True
        except Exception as e:
            _log_warning(f"Failed to save results to {path}: {e}")
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
            
    return success

__all__ = ["save_results"]