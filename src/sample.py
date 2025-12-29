# src/sample.py
import torch

def prompt_to_prompt_edit(pipe, base_prompt, edit_prompt, negative_prompt, seed):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    generator = torch.Generator(device).manual_seed(seed)

    full_prompt = f"{base_prompt}, {edit_prompt}"

    image = pipe(
        prompt=full_prompt,
        negative_prompt=negative_prompt,
        generator=generator,
        num_inference_steps=50,
        guidance_scale=7.5
    ).images[0]

    return image
