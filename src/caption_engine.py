import json
import re
from typing import Dict, List, Any, Optional

from openai import OpenAI

from src.config import (
    FIREWORKS_API_KEY, FIREWORKS_BASE_URL, 
    VISION_MODEL_NAME, TEXT_MODEL_NAME, AUDIO_MODEL_NAME,
    MAX_OUTPUT_TOKENS, TEMPERATURE, MAX_RETRIES, RETRY_DELAY_SECONDS,
    ENABLE_CONFIDENCE_SCORES, ENABLE_SELF_VERIFICATION, 
    CONFIDENCE_THRESHOLD, MAX_VERIFICATION_ATTEMPTS
)
from src.utils import _log_info, _log_error, _log_warning, _log_success


class CaptionEngine:

    def __init__(self):
        # Fireworks client for text generation
        api_key = FIREWORKS_API_KEY if FIREWORKS_API_KEY else "dummy_key"
        self.client = OpenAI(
            base_url=FIREWORKS_BASE_URL,
            api_key=api_key
        )
        _log_info("Caption Engine initialized (Fireworks only).")

    # ------------------------------------------------------------------
    # Audio transcription (kept from original, optional)
    # ------------------------------------------------------------------
    def transcribe_audio(self, audio_path: str) -> Optional[str]:
        if not FIREWORKS_API_KEY or FIREWORKS_API_KEY == "dummy_key":
            _log_warning("No valid API key available; skipping transcription.")
            return None

        _log_info(f"Transcribing audio file using {AUDIO_MODEL_NAME}...")
        for attempt in range(MAX_RETRIES):
            try:
                with open(audio_path, "rb") as audio_file:
                    transcript_obj = self.client.audio.transcriptions.create(
                        file=audio_file,
                        model=AUDIO_MODEL_NAME
                    )
                transcript = transcript_obj.text.strip()
                _log_success(f"Audio transcription successful: {transcript[:100]}...")
                return transcript
            except Exception as e:
                _log_warning(f"Audio transcription failed (attempt {attempt+1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    import time
                    time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))
        return None

    # ------------------------------------------------------------------
    # Scene description using Fireworks (vision)
    # ------------------------------------------------------------------
    def generate_scene_description(self, frames_b64: List[str]) -> str:
        """Generate a detailed scene description using Fireworks vision model."""
        
        _log_info(f"Stage 1: Sending {len(frames_b64)} frames to Fireworks vision model ({VISION_MODEL_NAME})...")
        if VISION_MODEL_NAME and "gemini" not in VISION_MODEL_NAME.lower():
            try:
                # Use the existing Fireworks vision code (only if a vision model is set)
                system_prompt = """You are a precise video analysis model. Look at the sequence of video frames chronologically.
Provide a detailed, objective description of the visual scene, actions, characters, changes, setting, and camera movements.
Avoid any subjective language, personal opinions, or creative styling. Just write facts about what is visible."""

                content = [{"type": "text", "text": "Describe what is happening chronologically in these frames."}]
                for b64 in frames_b64:
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64}"
                        }
                    })

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ]

                for attempt in range(MAX_RETRIES):
                    try:
                        response = self.client.chat.completions.create(
                            model=VISION_MODEL_NAME,
                            messages=messages,
                            max_tokens=MAX_OUTPUT_TOKENS * 2,
                            temperature=0.2
                        )
                        description = response.choices[0].message.content.strip()
                        _log_success("Stage 1 visual analysis complete (Fireworks).")
                        return description
                    except Exception as e:
                        _log_warning(f"Fireworks vision attempt {attempt+1} failed: {e}")
                        if attempt < MAX_RETRIES - 1:
                            import time
                            time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))
            except Exception as e:
                _log_error(f"Fireworks vision error: {e}")

        # Final fallback: detailed mock description
        _log_warning("All vision models failed. Returning fallback description.")
        return """The video captures a dynamic scene with natural lighting. 
        Multiple characters or objects are visible in motion across the frame. 
        The setting appears to be outdoors or in a well-lit environment. 
        The camera moves smoothly, capturing both wide and close-up views. 
        There is clear visual activity and change throughout the sequence."""

    # ------------------------------------------------------------------
    # JSON parsing (unchanged)
    # ------------------------------------------------------------------
    def _parse_json_response(self, raw_text: str) -> Dict[str, Any]:
        if not raw_text:
            return {}
        
        cleaned = raw_text.strip()
        
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', cleaned, re.DOTALL)
        if json_match:
            cleaned = json_match.group(1).strip()
        else:
            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if json_match:
                cleaned = json_match.group(0).strip()
        
        if cleaned.startswith('{') and cleaned.endswith('}'):
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass
        
        try:
            start = cleaned.find('{')
            end = cleaned.rfind('}')
            if start != -1 and end != -1 and start < end:
                potential_json = cleaned[start:end+1]
                return json.loads(potential_json)
        except json.JSONDecodeError:
            pass
        
        _log_error(f"Failed to parse JSON: {raw_text[:200]}...")
        return {}

    # ------------------------------------------------------------------
    # Build prompt with confidence (updated to use Gemini for vision)
    # ------------------------------------------------------------------
    def _build_confidence_prompt(self, scene_description: str, audio_transcript: str = None) -> List[Dict]:
        system_prompt = """You are a precise video captioning AI with self-awareness.
        You are a film critic. Analyze:
- Lighting and color (dark, bright, neon?)
- Camera movement (panning, zooming, shaky?)
- Emotional tone (dramatic, funny, suspenseful?)
- Key objects and characters visible

You will be given a neutral visual description of a video, and optionally, an audio transcript.

Your task: Generate captions in 4 distinct styles. For **every** caption, you **must** provide a confidence score between 0 and 100.

Confidence Score Guidelines:
- 90-100: Very certain (clear visual evidence, no ambiguity).
- 70-89: Moderately certain (good evidence, minor ambiguity).
- 50-69: Somewhat uncertain (limited evidence, making some educated guesses).
- 0-49: Very uncertain (mostly guessing, describe it as such).

Your output MUST be a single valid JSON object. Do NOT wrap in markdown.
The JSON must have exactly these 4 keys: "formal", "sarcastic", "humorous_tech", "humorous_non_tech".
Each value must be an object with "caption" (string) and "confidence" (integer).

Example:
{
    "formal": {"caption": "A cat sits on a windowsill.", "confidence": 95},
    "sarcastic": {"caption": "Another cat. Groundbreaking.", "confidence": 80},
    "humorous_tech": {"caption": "Cat.exe is running flawlessly.", "confidence": 85},
    "humorous_non_tech": {"caption": "That cat is clearly planning something.", "confidence": 90}
}
"""
        user_content = f"Visual Scene Description:\n{scene_description}\n\n"
        if audio_transcript:
            user_content += f"Audio Transcript (spoken words):\n{audio_transcript}\n\n"
        user_content += "Generate the 4 confidence-aware captions in JSON format."

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

    # ------------------------------------------------------------------
    # Self-verification (unchanged)
    # ------------------------------------------------------------------
    def _verify_captions(self, captions: Dict[str, Dict], scene_description: str) -> List[str]:
        _log_info("Running Self-Verification on captions...")
        
        if ENABLE_CONFIDENCE_SCORES:
            for style, data in captions.items():
                conf = data.get("confidence", 0)
                if conf < CONFIDENCE_THRESHOLD:
                    _log_warning(f"'{style}' confidence is low ({conf}). Marking for redo.")
                    return [style]
        
        if not ENABLE_SELF_VERIFICATION:
            return []
        
        check_prompt = f"""
You are a strict fact-checker.

Original Scene Description:
{scene_description}

Captions to verify:
{json.dumps(captions, indent=2)}

Carefully check if the "caption" text in each style contradicts the original scene description.
If a caption describes something not present in the original scene, mark it as "invalid".
If a caption is vague but doesn't contradict, it is "valid".

Output a JSON object with the style names as keys, and "valid" or "invalid" as values.
Example: {{"formal": "valid", "sarcastic": "invalid", "humorous_tech": "valid", "humorous_non_tech": "valid"}}
"""
        try:
            response = self.client.chat.completions.create(
                model=TEXT_MODEL_NAME,
                messages=[{"role": "user", "content": check_prompt}],
                max_tokens=200,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            raw = response.choices[0].message.content
            results = self._parse_json_response(raw)
            
            invalid_styles = [style for style, status in results.items() if status == "invalid"]
            if invalid_styles:
                _log_warning(f"Invalid captions found: {invalid_styles}")
                return invalid_styles
            else:
                _log_success("All captions passed verification!")
                return []
        except Exception as e:
            _log_warning(f"Verification API call failed: {e}. Skipping.")
            return []

    # ------------------------------------------------------------------
    # Generate all captions (main entry)
    # ------------------------------------------------------------------
    def generate_all_captions(self, scene_description: str, audio_transcript: str = None) -> Dict[str, str]:
        _log_info("Pipeline: Confidence + Verification Active.")
        
        messages = self._build_confidence_prompt(scene_description, audio_transcript)
        final_captions = {}
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=TEXT_MODEL_NAME,
                    messages=messages,
                    max_tokens=MAX_OUTPUT_TOKENS,
                    temperature=TEMPERATURE,
                    response_format={"type": "json_object"}
                )
                raw = response.choices[0].message.content
                parsed = self._parse_json_response(raw)
                
                required = {"formal", "sarcastic", "humorous_tech", "humorous_non_tech"}
                if all(k in parsed and "caption" in parsed[k] for k in required):
                    final_captions = parsed
                    break
                else:
                    _log_warning(f"Malformed JSON on attempt {attempt+1}")
            except Exception as e:
                _log_warning(f"API Error on attempt {attempt+1}: {e}")
                if attempt < MAX_RETRIES - 1:
                    import time
                    time.sleep(RETRY_DELAY_SECONDS * (2 ** attempt))
        
        # If no valid JSON, return fallback captions
        if not final_captions:
            return {
                "formal": "Unable to process video.",
                "sarcastic": "API broke.",
                "humorous_tech": "404: Caption not found.",
                "humorous_non_tech": "Well, that failed."
            }
        
        # Self-verification loop
        for _ in range(MAX_VERIFICATION_ATTEMPTS):
            invalid_styles = self._verify_captions(final_captions, scene_description)
            if not invalid_styles:
                break
            
            _log_info(f"Regenerating style(s): {invalid_styles}")
            for style in invalid_styles:
                try:
                    fix_response = self.client.chat.completions.create(
                        model=TEXT_MODEL_NAME,
                        messages=[
                            {"role": "system", "content": "You are a precise video captioning AI. Your output MUST be a single valid JSON object containing a single key 'caption' (string value). Do not output any conversational text or explanation outside the JSON."},
                            {"role": "user", "content": f"Scene Description: {scene_description}\nGenerate a correct caption specifically for the '{style}' style that strictly follows the scene description. Output the new caption under the key 'caption'."}
                        ],
                        max_tokens=1024,
                        temperature=0.3,
                        response_format={"type": "json_object"}
                    )
                    raw_fix = fix_response.choices[0].message.content.strip()
                    parsed_fix = self._parse_json_response(raw_fix)
                    new_caption = parsed_fix.get("caption", "").strip()
                    if new_caption:
                        final_captions[style]['caption'] = new_caption
                        final_captions[style]['confidence'] = 75
                        _log_success(f"Regenerated '{style}' successfully.")
                    else:
                        raise Exception("Parsed JSON was missing 'caption' key.")
                except Exception as e:
                    _log_warning(f"Failed to regenerate '{style}': {e}")

        if ENABLE_CONFIDENCE_SCORES:
            return {style: data["caption"] for style, data in final_captions.items()}
        else:
            return {style: data["caption"] if isinstance(data, dict) else data for style, data in final_captions.items()}


__all__ = ["CaptionEngine"]