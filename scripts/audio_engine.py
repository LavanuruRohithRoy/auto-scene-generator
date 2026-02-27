import os
import asyncio
import subprocess
import edge_tts

AUDIO_DIR = "assets/audio"
VOICE = "en-US-AriaNeural"


def ensure_audio_dir():
    os.makedirs(AUDIO_DIR, exist_ok=True)


async def generate_audio_async(text: str, path: str):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate="+5%",
        volume="+20%"
    )
    await communicate.save(path)


def generate_audio(text: str, filename: str):
    ensure_audio_dir()
    path = os.path.join(AUDIO_DIR, filename)
    asyncio.run(generate_audio_async(text, path))
    return path


def get_duration(path: str):
    cmd = [
        "ffprobe",
        "-i", path,
        "-show_entries", "format=duration",
        "-v", "quiet",
        "-of", "csv=p=0"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return round(float(result.stdout.strip()), 2)


def attach_audio(scenes):
    updated = []

    for i, scene in enumerate(scenes, 1):
        filename = f"scene_{i}.mp3"
        path = generate_audio(scene["text"], filename)
        duration = get_duration(path)

        scene["audio_path"] = path
        scene["duration"] = duration
        updated.append(scene)

    return updated