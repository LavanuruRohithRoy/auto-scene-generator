import os
import subprocess

OUTPUT_DIR = "assets/output"
TEMP_DIR = "assets/temp"
MUSIC_PATH = "assets/music/bg.mp3"


def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)


def create_scene_video(scene, index):
    output_path = os.path.join(TEMP_DIR, f"scene_{index}.mp4")

    duration = str(scene["duration"])

    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", scene["image_path"],
        "-i", scene["audio_path"],
        "-filter_complex",
        f"""
        [0:v]scale=1920:1080,
        fade=t=in:st=0:d=0.5,
        fade=t=out:st={float(duration)-0.5}:d=0.5[v];
        [1:a]volume=1.8,aresample=44100[a]
        """,
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-t", duration,
        "-pix_fmt", "yuv420p",
        output_path
    ]

    subprocess.run(cmd)
    return output_path


def concatenate_scenes(scene_videos):
    concat_file = os.path.join(TEMP_DIR, "concat.txt")

    with open(concat_file, "w") as f:
        for video in scene_videos:
            f.write(f"file '{os.path.abspath(video)}'\n")

    merged = os.path.join(TEMP_DIR, "merged.mp4")

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        merged
    ]

    subprocess.run(cmd)
    return merged


def add_background_music(video_path):
    final_output = os.path.join(OUTPUT_DIR, "final_video.mp4")

    if not os.path.exists(MUSIC_PATH):
        return video_path

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", MUSIC_PATH,
        "-filter_complex",
        """
        [1:a]volume=0.25[a2];
        [0:a][a2]amix=inputs=2:duration=first:dropout_transition=2[aout]
        """,
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        final_output
    ]

    subprocess.run(cmd)
    return final_output


def build_video(scenes):
    ensure_dirs()
    clips = []

    for i, scene in enumerate(scenes, 1):
        clips.append(create_scene_video(scene, i))

    merged = concatenate_scenes(clips)
    final = add_background_music(merged)

    return final