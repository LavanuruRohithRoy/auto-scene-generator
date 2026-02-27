import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


def generate_script(topic: str) -> dict:
    prompt = f"""
Return ONLY valid JSON.

Format:
{{
  "hook": "...",
  "body": "...",
  "visuals": ["...", "...", "..."]
}}

Rules:
- 65–80 words total
- Exactly 3 visuals
- Visuals max 8 words each
- Informative and concise
- No numbering
- No nested objects

Topic: {topic}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.85
        }
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=240)
    raw = r.json()["response"]

    start = raw.find("{")
    end = raw.rfind("}") + 1
    data = json.loads(raw[start:end])

    cta_prompt = f"Write a short 5-word call to action about {topic}. No punctuation."
    cta_payload = {
        "model": MODEL_NAME,
        "prompt": cta_prompt,
        "stream": False
    }

    cta_resp = requests.post(OLLAMA_URL, json=cta_payload, timeout=120)
    data["cta"] = cta_resp.json()["response"].strip()

    return data