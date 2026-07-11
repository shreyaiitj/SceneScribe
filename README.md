# 🎬 Video Captioning Agent - AMD Hackathon Act II

## 🏆 Track 2: Video Captioning Agent

This project generates captions for video clips in four distinct styles:
- **Formal**: Professional, factual tone.
- **Sarcastic**: Dry, ironic, mocking tone.
- **Humorous Tech**: Funny with programming/tech references.
- **Humorous Non-Tech**: Funny with everyday jokes.

## 🔥 Secret Sauce

**Scene Detection with Histogram Analysis**

Unlike most submissions that extract random frames, this agent:
1. Extracts **16 candidate frames** evenly across the video.
2. Uses **OpenCV histogram correlation** to detect scene changes.
3. Filters out duplicate/similar frames to keep the **8 most visually diverse** scenes.
4. Sends these to Gemma 4 for highly accurate captioning.

This ensures the AI sees the **beginning, middle, and end** of the video, capturing the full story.

## 🧠 Tech Stack

- **AI Model**: Google Gemma 4 (via Fireworks AI)
- **Video Processing**: FFmpeg + OpenCV
- **Packaging**: Docker (linux/amd64)
- **Language**: Python 3.10


## 🚀 How to Build & Run

### Locally:
```bash
# 1. Create a .env file with your API key
echo 'FIREWORKS_API_KEY="fw_your_key"' > .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python main.py

# 1. Build
docker buildx build --platform linux/amd64 -t video-captioner:latest .

# 2. Run
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  -e FIREWORKS_API_KEY="fw_your_key" \
  video-captioner:latest