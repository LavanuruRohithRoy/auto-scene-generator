from script_engine import generate_script
from scene_engine import build_scenes
from audio_engine import attach_audio
from image_engine import load_pipeline, attach_images
from video_engine import build_video

TOPIC = "Black holes"

print("Generating script...")
script = generate_script(TOPIC)

print("Building scenes...")
scenes = build_scenes(script)

print("Generating neural voice...")
scenes = attach_audio(scenes)

print("Loading Stable Diffusion...")
pipe = load_pipeline()

print("Generating images...")
scenes = attach_images(pipe, scenes)

print("Building cinematic video...")
final_video = build_video(scenes)

print("Done:", final_video)