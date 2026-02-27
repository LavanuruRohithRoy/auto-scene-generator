import json
import time
from config import MAX_RETRIES

def safe_json_parse(text):
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except Exception:
        return None

def retry(func):
    def wrapper(*args, **kwargs):
        for attempt in range(MAX_RETRIES):
            result = func(*args, **kwargs)
            if result:
                return result
            time.sleep(1)
        return None
    return wrapper