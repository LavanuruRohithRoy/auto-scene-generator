import re

WORDS_PER_SECOND = 2.5
MIN_DURATION = 2.0


def split_sentences(text: str):
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def estimate_duration(text: str):
    wc = len(text.split())
    return round(max(MIN_DURATION, wc / WORDS_PER_SECOND), 2)


def build_scenes(script: dict):
    scenes = []

    segments = []
    segments.append(script["hook"])
    segments.extend(split_sentences(script["body"]))
    segments.append(script["cta"])

    visuals = script["visuals"]

    for i, text in enumerate(segments):
        visual_index = min(i, len(visuals) - 1)

        scenes.append({
            "text": text,
            "visual_prompt": visuals[visual_index],
            "duration": estimate_duration(text)
        })

    return scenes