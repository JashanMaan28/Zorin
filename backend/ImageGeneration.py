import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
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
            sleep(1)  # Pause for 1 second before opening the next image

        except IOError:
            print(f"Error opening image: {image_path}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_image(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resoulution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

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
            Data: str = f.read()

        Prompt, Status = Data.split(",")

        if Status == "True":
            print("Generating images...")
            ImageStatus = GenerateImages(prompt=Prompt)

            with open(r"Data\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
                break 

        else:
            sleep(1)
        
    except Exception as e:
        print(e)

