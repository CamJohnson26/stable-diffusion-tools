import os
from os.path import isfile, join

import torch
from PIL import Image
from torch import autocast
from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler
import urllib3
import time
http = urllib3.PoolManager()

ACCESS_TOKEN = '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'

# model_id = "CompVis/stable-diffusion-v1-4"
# model_id = "stabilityai/stable-diffusion-2-1-base"
model_id = "stabilityai/stable-diffusion-2-1"
device = "cuda"

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16, use_auth_token=ACCESS_TOKEN)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config) # New for 2-1

pipe = pipe.to(device)
pipe.enable_attention_slicing()

prompt = """
painting by monet, soft lighting, charming, professional, HDR, 64k
"""

print('Prompts: ')
print(prompt)

path = './input'
files = [f for f in os.listdir(path) if isfile(join(path, f))]

for file in files:
    f = open(join(path, file), 'r')

    input_image = Image.open(join(path, file)).convert("RGB").resize((512, 512))
    outdir = f"output/{file}"
    try:
        os.mkdir(outdir)
    except FileExistsError:
        pass

    # with autocast("cuda"):
    images = pipe(prompt, strength=0.4, guidance_scale=9, num_inference_steps=50, num_images_per_prompt=6, image=input_image).images
    # image = pipe(cur_input, guidance_scale=7.5, num_inference_steps=5)["sample"][0]
    for i, image in enumerate(images):
        image.save(join(outdir, f"{i}.png"))