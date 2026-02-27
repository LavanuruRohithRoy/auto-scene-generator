import requests
import json
import time
from pydantic import BaseModel
from typing import List, Optional


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"
TIMEOUT = 240


class ScriptCore(BaseModel):
    hook: str
    body: str
    visuals: List[str]


def call_llm(prompt: str) -> Optional[str]:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.85
        }
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        if r.status_code != 200:
            return None
        return r.json().get("response")
    except:
        return None


def generate_core_script(topic: str) -> Optional[ScriptCore]:
    prompt = f"""
Generate a cinematic educational short video script.

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

    raw = call_llm(prompt)
    if not raw:
        return None

    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        parsed = json.loads(raw[start:end])
        return ScriptCore(**parsed)
    except:
        return None


def generate_cta(topic: str) -> Optional[str]:
    prompt = f"Write a short 5-word call to action about {topic}. No punctuation."
    return call_llm(prompt)


def generate_script(topic: str) -> Optional[dict]:
    core = generate_core_script(topic)
    if not core:
        return None

    cta = generate_cta(topic)
    if not cta:
        return None

    return {
        "hook": core.hook.strip(),
        "body": core.body.strip(),
        "visuals": core.visuals,
        "cta": cta.strip()
    }


if __name__ == "__main__":
    start = time.perf_counter()
    script = generate_script("Black holes")
    end = time.perf_counter()

    if script:
        print(json.dumps(script, indent=2))
    else:
        print("Generation failed")

    print("Latency:", round(end - start, 2), "seconds")