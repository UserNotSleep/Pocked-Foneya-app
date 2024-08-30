import base64
import requests
from pathlib import Path

# Константа для URL API
API_URL = "http://127.0.0.1:7860"

def generate_image(prompt: str, negative_prompt: str, steps: int, selected_model: str, output_path: Path) -> bool:
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "batch_size": 1,
        "cfg_scale": 8,
        "refiner_checkpoint": selected_model
    }

    try:
        response = requests.post(url=f'{API_URL}/sdapi/v1/txt2img', json=payload)
        response.raise_for_status()  # Проверка успешности запроса
        r = response.json()

        # Проверяем наличие изображения в ответе
        if 'images' in r and len(r['images']) > 0:
            save_image(base64.b64decode(r['images'][0]), output_path)
            return True
        else:
            print("Error: No images found in the response.")
            return False

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return False
    except (KeyError, ValueError) as e:
        print(f"Failed to decode image: {e}")
        return False

def save_image(image_data: bytes, output_path: Path):
    try:
        with open(output_path, 'wb') as f:
            f.write(image_data)
        print(f"Image saved successfully to {output_path}")
    except IOError as e:
        print(f"Failed to save image: {e}")

def generate_presed(e, prompt, negative_prompt, steps, selected_model):
    print(f'Prompt: {prompt}')
    print(f'Negative Prompt: {negative_prompt}')
    print(f'Steps: {steps}')
    print(f'Selected Model: {selected_model}')

    output_path = Path("image.png")
    success = generate_image(prompt, negative_prompt, steps, selected_model, output_path)
    
    if success:
        print(f"Image generated and saved to {output_path}")
    else:
        print("Image generation failed.")

