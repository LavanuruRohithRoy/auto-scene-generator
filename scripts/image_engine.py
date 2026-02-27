import os
import torch
from diffusers import StableDiffusionPipeline
from typing import List, Dict

IMAGE_DIR = "assets/images"
MODEL_ID = "runwayml/stable-diffusion-v1-5"


def ensure_image_dir():
    os.makedirs(IMAGE_DIR, exist_ok=True)


def load_pipeline():
    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float32
    )
    pipe.to("cpu")
    pipe.enable_attention_slicing()
    return pipe


def generate_image(pipe, prompt: str, filename: str) -> str:
    ensure_image_dir()

    image = pipe(
        prompt,
        num_inference_steps=20,
        guidance_scale=7.5
    ).images[0]

    path = os.path.join(IMAGE_DIR, filename)
    image.save(path)

    return path


def attach_images_to_scenes(pipe, scenes: List[Dict]) -> List[Dict]:
    updated_scenes = []

    for i, scene in enumerate(scenes):
        prompt = scene["visual_prompt"] + ", cinematic lighting, high detail"

        filename = f"scene_{i+1}.png"
        image_path = generate_image(pipe, prompt, filename)

        updated_scene = scene.copy()
        updated_scene["image_path"] = image_path

        updated_scenes.append(updated_scene)

    return updated_scenes


if __name__ == "__main__":
    from script_engine import generate_script
    from scene_engine import build_scenes

    print("Loading Stable Diffusion model (first time will download)...")
    pipe = load_pipeline()

    script = generate_script("Black holes")

    if script:
        scenes = build_scenes(script)
        scenes_with_images = attach_images_to_scenes(pipe, scenes)

        for idx, scene in enumerate(scenes_with_images, 1):
            print(f"\nScene {idx}")
            print(scene)
    else:
        print("Script generation failed.")