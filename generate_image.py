from os import environ, mkdir, path
from os.path import join

from dotenv import load_dotenv

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import datetime

MODEL_ID = "stabilityai/stable-diffusion-2-1"
DEVICE = "cuda"
OUTPUT_FOLDER = 'output'

GUIDANCE_SCALE = 9
NUM_INFERENCE_STEPS = 50
NUM_IMAGES_PER_PROMPT = 6

load_dotenv()
ACCESS_TOKEN = environ.get("ACCESS_TOKEN")

pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16, use_auth_token=ACCESS_TOKEN)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)  # New for 2-1

pipe = pipe.to(DEVICE)
pipe.enable_attention_slicing()


def generate_image(description):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{timestamp}_{description[:50]}'

    if not path.exists(OUTPUT_FOLDER):
        mkdir(OUTPUT_FOLDER)

    destination_folder = join(OUTPUT_FOLDER, filename)
    if not path.exists(destination_folder):
        mkdir(destination_folder)

    images = pipe(description, guidance_scale=GUIDANCE_SCALE, num_inference_steps=NUM_INFERENCE_STEPS,
                  num_images_per_prompt=NUM_IMAGES_PER_PROMPT).images

    for i, image in enumerate(images):
        image.save(f"{destination_folder}/{filename}_{i}.png")

    """Create text file with description and timestamp."""
    with open(f"{destination_folder}/{filename}.txt", "w") as text_file:
        text_file.write(f"{description} {timestamp}")
