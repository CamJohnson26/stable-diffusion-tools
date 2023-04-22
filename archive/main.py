import os

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import urllib3
import time
http = urllib3.PoolManager()

ACCESS_TOKEN = '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'

# model_id = "CompVis/stable-diffusion-v1-4"
# model_id = "stabilityai/stable-diffusion-2-1-base"
model_id = "stabilityai/stable-diffusion-2-1"
device = "cuda"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, use_auth_token=ACCESS_TOKEN)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config) # New for 2-1

pipe = pipe.to(device)
pipe.enable_attention_slicing()

# prompt = "a close up, high detail, full color photograph of elon musk hawking a bottle of snake oil out of a wagon in the 19th century"
# prompt = 'An underwater, close up, high detail photo from national geographic of deep ocean a great white shark, fully lit with crystal clear blue water'
# prompt = 'close up high detail screenshot. Tom the cat and Jerry the mouse in the award winning David Fincher film'

URL = 'https://raw.githubusercontent.com/CamJohnson26/stable-diff-inputs/main/inputs'
folder_number = 848

while True:
    try:
        old_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip',
            'DNT': '1',  # Do Not Track Request Header
            'Connection': 'close',
            'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT'
        }
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.8",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "Referer": "https://github.com/",
            "Referrer-Policy": "no-referrer-when-downgrade"
        }
        r = http.request('GET', URL, headers=headers)

        prompts = r.data.decode('utf-8').split('\n')
        print('Prompts: ')
        print(prompts)
        f = open('Dropbox/Dropbox/Stable Diffusion/logged_results', 'r')
        processed = [l.strip() for l in f.readlines()]
        print('processed: ')
        print(processed)
        cur_input = ''
        cur_filename = ''

        for line in prompts:
            prompt_parts = line.split(':')
            print('prompt_parts: ')
            print(prompt_parts)
            filename = prompt_parts[0].strip()
            prompt_text = prompt_parts[1].strip()
            if not filename in processed:
                cur_input = prompt_text
                cur_filename = filename

                os.mkdir(f"Dropbox/Dropbox/Stable Diffusion/{folder_number}-{filename}")

                # with autocast("cuda"):
                images = pipe(cur_input, guidance_scale=9, num_inference_steps=50, num_images_per_prompt=6).images
                # image = pipe(cur_input, guidance_scale=7.5, num_inference_steps=5)["sample"][0]
                for i, image in enumerate(images):
                    image.save(f"Dropbox/Dropbox/Stable Diffusion/{folder_number}-{filename}/{i}.png")
                with open('Dropbox/Dropbox/Stable Diffusion/logged_results', "a") as myfile:
                    myfile.write(f"\n{filename}")
                folder_number += 1
    except Exception as e:
        print(e)
    time.sleep(20)