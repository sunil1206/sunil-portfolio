import os
import torch
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import uuid
from fastapi.responses import JSONResponse
app = FastAPI()


class DiffusionImageGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device="cpu", seed=42):
        self.device = device
        self.model_id = model_id
        self.seed = seed
        self.pipe = self._load_pipeline()

    def _load_pipeline(self):
        torch.manual_seed(self.seed)
        pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float32,  # Use float32 for CPU-only environments
            revision="fp32",  # Ensure compatibility with CPU
            use_auth_token=True
        )
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe = pipe.to(self.device)
        return pipe

    def generate_images(self, prompt, num_images=4, resolution="1024x1024", guidance_scale=7.5, steps=30):
        width, height = map(int, resolution.lower().replace("px", "").split("x"))
        results = []
        for _ in range(num_images):
            image = self.pipe(
                prompt=prompt,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                height=height,
                width=width
            ).images[0]

            # Save the generated image with a unique filename
            filename = f"image_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join("static/generated", filename)
            image.save(filepath)
            results.append(filepath)

        return results


# Initialize the image generator (CPU-only setup)
image_generator = DiffusionImageGenerator(device="cpu")


class ImageGenerationRequest(BaseModel):
    prompt: str
    resolution: str = "1024x1024"
    guidance_scale: float = 7.5
    num_images: int = 1
    steps: int = 30


@app.post("/generate-images")
async def generate_images(request: ImageGenerationRequest):
    try:
        # Generate the images based on the user's request
        image_paths = image_generator.generate_images(
            prompt=request.prompt,
            num_images=request.num_images,
            resolution=request.resolution,
            guidance_scale=request.guidance_scale,
            steps=request.steps
        )

        # Return the image paths in the response
        return JSONResponse(content={"images": image_paths}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


if __name__ == '__main__':
    # Make sure the static/generated folder exists
    if not os.path.exists("static/generated"):
        os.makedirs("static/generated")
