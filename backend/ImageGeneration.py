import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
import json
from time import sleep

def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            

        except IOError:
            print(f"Error opening image: {image_path}")

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_image(prompt: str):
    tasks = []

    for _ in range(3):  # Only create 3 images
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # Wait for all tasks AFTER creating them
    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
            f.write(image_bytes)

def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt))
    open_images(prompt)


while True:
    try:
        with open(r"Data\Files\ImageGeneration.data", "r") as f:
            data = json.load(f)

        Prompt = data.get("prompt", "")
        Status = data.get("status", False)

        if Status == True:
            print("Generating images...")
            GenerateImages(prompt=Prompt)

            with open(r"Data\Files\ImageGeneration.data", "w") as f:
                json.dump({"prompt": "", "status": False}, f)

            break

        else:
            sleep(1)
        
    except Exception as e:
        print(e)






# while True:
#     try:
#         with open(r"Data\Files\ImageGeneration.data", "r") as f:
#             data = json.load(f)

#         Prompt = data.get("prompt", "")
#         Status = data.get("status", False)

#         if Status == True:
#             print("Generating images...")
#             GenerateImages(prompt=Prompt)

#             # Notify after image generation is done
#             eel.showSiri()
#             eel.DisplayMessage("✅ The images have been successfully generated, sir.")
#             speak("✅ The images have been successfully generated, sir.")
#             eel.DisplayMessage("🖼️ Please take a look at your screen.")
#             speak("🖼️ Please take a look at your screen.")
#             eel.DisplayMessage("If you don’t see them immediately, they should appear momentarily.")
#             speak("If you don’t see them immediately, they should appear momentarily.")
    
#             # Update the ImageGeneration.data file to reflect the completion status
#             with open(r"Data\Files\ImageGeneration.data", "w") as f:
#                 json.dump({"prompt": "", "status": False}, f)

#             break

#         else:
#             sleep(1)

#     except Exception as e:
#         print(e)
