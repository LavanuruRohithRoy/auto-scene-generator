import os
import subprocess
from gtts import gTTS
from typing import List, Dict

AUDIO_DIR = "assets/audio"


def ensure_audio_dir():
    os.makedirs(AUDIO_DIR, exist_ok=True)


def generate_audio(text: str, filename: str) -> str:
    ensure_audio_dir()
    path = os.path.join(AUDIO_DIR, filename)

    tts = gTTS(text=text, lang="en")
    tts.save(path)

    return path


def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe",
        "-i", file_path,
        "-show_entries", "format=duration",
        "-v", "quiet",
        "-of", "csv=p=0"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return round(float(result.stdout.strip()), 2)


def attach_audio_to_scenes(scenes: List[Dict]) -> List[Dict]:
    updated_scenes = []

    for i, scene in enumerate(scenes):
        filename = f"scene_{i+1}.mp3"

        audio_path = generate_audio(scene["text"], filename)
        duration = get_audio_duration(audio_path)

        updated_scene = scene.copy()
        updated_scene["audio_path"] = audio_path
        updated_scene["duration"] = duration

        updated_scenes.append(updated_scene)

    return updated_scenes


if __name__ == "__main__":
    from script_engine import generate_script
    from scene_engine import build_scenes

    script = generate_script("Black holes")

    if script:
        scenes = build_scenes(script)
        scenes_with_audio = attach_audio_to_scenes(scenes)

        for idx, scene in enumerate(scenes_with_audio, 1):
            print(f"\nScene {idx}")
            print(scene)
    else:
        print("Script generation failed.")