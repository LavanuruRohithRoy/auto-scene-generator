import re
from typing import List, Dict

WORDS_PER_SECOND = 2.5
MIN_SCENE_DURATION = 2.0


def estimate_duration(text: str) -> float:
    word_count = len(text.split())
    duration = word_count / WORDS_PER_SECOND
    return round(max(MIN_SCENE_DURATION, duration), 2)


def split_sentences(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def build_scenes(script_data: Dict) -> List[Dict]:
    scenes = []

    hook = script_data.get("hook", "")
    body = script_data.get("body", "")
    visuals = script_data.get("visuals", [])
    cta = script_data.get("cta", "")

    body_sentences = split_sentences(body)

    all_text_segments = []
    if hook:
        all_text_segments.append(hook)

    all_text_segments.extend(body_sentences)

    if cta:
        all_text_segments.append(cta)

    total_visuals = len(visuals)

    for i, text in enumerate(all_text_segments):
        if total_visuals > 0:
            visual_index = min(i, total_visuals - 1)
            visual_prompt = visuals[visual_index]
        else:
            visual_prompt = ""

        scenes.append({
            "text": text,
            "visual_prompt": visual_prompt,
            "duration": estimate_duration(text)
        })

    return scenes


if __name__ == "__main__":
    from script_engine import generate_script

    script = generate_script("Black holes")

    if script:
        scenes = build_scenes(script)   # <-- FIXED (no model_dump)
        for idx, scene in enumerate(scenes, 1):
            print(f"\nScene {idx}")
            print(scene)
    else:
        print("Script generation failed.")