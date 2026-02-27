import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
os.chdir(PROJECT_ROOT)

def run_pipeline(topic):
    from script_engine import generate_script
    from scene_engine import build_scenes
    from audio_engine import attach_audio
    from image_engine import load_pipeline, attach_images
    from video_engine import build_video

    script = generate_script(topic)
    scenes = build_scenes(script)
    scenes = attach_audio(scenes)

    pipe = load_pipeline()
    scenes = attach_images(pipe, scenes)

    final_video = build_video(scenes)

    return final_video