import os
import torch
from diffusers import StableDiffusionPipeline

IMAGE_DIR = "assets/images"
MODEL_ID = "runwayml/stable-diffusion-v1-5"


def ensure_image_dir():
    os.makedirs(IMAGE_DIR, exist_ok=True)


def load_pipeline():
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float32,
        safety_checker=None
    )

    pipe = pipe.to("cpu")
    return pipe


def attach_images(pipe, scenes):
    ensure_image_dir()

    for i, scene in enumerate(scenes, 1):
        image = pipe(scene["visual_prompt"], num_inference_steps=20).images[0]
        path = os.path.join(IMAGE_DIR, f"scene_{i}.png")
        image.save(path)
        scene["image_path"] = path

    return scenes