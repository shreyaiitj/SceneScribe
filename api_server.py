from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import subprocess
import uuid
import shutil

app = Flask(__name__)
CORS(app)

@app.route('/api/generate-captions', methods=['POST'])
def generate_captions():
    data = request.get_json()
    video_url = data.get('video_url')
    
    if not video_url:
        return jsonify({'error': 'No video_url provided'}), 400
    
    task_id = f"v{str(uuid.uuid4())[:8]}"
    
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    tasks = [{
        "task_id": task_id,
        "video_url": video_url,
        "styles": ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]
    }]
    
    with open(os.path.join(input_dir, "tasks.json"), "w") as f:
        json.dump(tasks, f)
    
    try:
        result = subprocess.run(
            ["python", "main.py"],
            capture_output=True,
            text=True,
            timeout=600,
            cwd="/app"
        )
        
        output_path = os.path.join(output_dir, "results.json")
        if os.path.exists(output_path):
            with open(output_path, "r") as f:
                results = json.load(f)
                if results:
                    return jsonify(results[0])
        
        return jsonify({"error": "Processing failed"}), 500
        
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Processing timeout"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)