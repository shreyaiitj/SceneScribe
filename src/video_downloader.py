import os
import tempfile
import requests
from typing import Optional

from src.config import MAX_RETRIES, RETRY_DELAY_SECONDS, TIMEOUT_SECONDS
from src.utils import _log_info, _log_error, _log_warning, _log_success

def download_video(url: str) -> Optional[str]:
    _log_info(f"Downloading video from: {url[:60]}...")

    try:
        temp_file = tempfile.NamedTemporaryFile(
            suffix='.mp4',
            delete=False,
            dir=tempfile.gettempdir()
        )
        temp_path = temp_file.name
        temp_file.close()
    except Exception as e:
        _log_error(f"Failed to create temporary file: {e}")
        return None

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                url,
                stream=True,
                timeout=TIMEOUT_SECONDS,
                headers={"User-Agent": "Mozilla/5.0 (compatible; HackathonBot/1.0)"}
            )
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

            if os.path.getsize(temp_path) == 0:
                raise Exception("Downloaded file is empty.")

            _log_success(f"Video downloaded successfully ({downloaded // 1024} KB)")
            return temp_path

        except requests.exceptions.Timeout:
            _log_warning(f"Timeout on attempt {attempt + 1}/{MAX_RETRIES}")
        except requests.exceptions.RequestException as e:
            _log_warning(f"Request error on attempt {attempt + 1}/{MAX_RETRIES}: {e}")
        except Exception as e:
            _log_warning(f"Error on attempt {attempt + 1}/{MAX_RETRIES}: {e}")

        if attempt < MAX_RETRIES - 1:
            import time
            time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))

    if os.path.exists(temp_path):
        os.unlink(temp_path)
    _log_error(f"Failed to download video after {MAX_RETRIES} attempts.")
    return None

__all__ = ["download_video"]