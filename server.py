import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.video_downloader import download_video
from src.frame_extractor import extract_key_frames
from src.caption_engine import CaptionEngine
from src.utils import _log_info, _log_error, _log_success

app = FastAPI(title="SceneScribe API Server")

# Allow CORS so that any frontend client can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CaptionRequest(BaseModel):
    video_url: str

class CaptionResponse(BaseModel):
    task_id: str
    captions: dict

# Initialize CaptionEngine
try:
    engine = CaptionEngine()
except Exception as e:
    engine = None
    print(f"Error initializing CaptionEngine: {e}")

@app.get("/health")
def health():
    return {"status": "ok", "engine_ready": engine is not None}

@app.post("/api/generate-captions", response_model=CaptionResponse)
async def generate_captions_endpoint(request: CaptionRequest):
    global engine
    if not engine:
        try:
            engine = CaptionEngine()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Caption engine not ready: {e}")

    _log_info(f"Received frontend request for video: {request.video_url}")
    video_path = None
    try:
        video_path = download_video(request.video_url)
        if not video_path:
            raise HTTPException(status_code=400, detail="Failed to download video from the provided URL.")

        frames_b64 = extract_key_frames(video_path)
        scene_description = engine.generate_scene_description(frames_b64)
        captions = engine.generate_all_captions(scene_description)

        _log_success("Generated captions successfully for frontend request.")
        return CaptionResponse(
            task_id="frontend-task",
            captions=captions
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        _log_error(f"Error processing frontend request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if video_path and os.path.exists(video_path):
            try:
                os.unlink(video_path)
            except Exception:
                pass

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
