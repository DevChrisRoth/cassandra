import random
import ollama
from PIL import Image
import tts

# Function to load all pictures from "screens_backup" directory
images = []

# Load image paths into images list
# Currently limited to 1 image due to LLM limitations
def load_images() -> None:
    images.clear()
    # Generate random number between 0 and 4
    random_image_index_number = random.randint(0, 4)
    images.append(f"screens/sc-{random_image_index_number}-compressed.png")
    print("==>Images loaded")

def vision_stream() -> str:
    load_images()

    response = ollama.chat(
       model="llama3.2-vision",
       messages=[
            {
                "role": "user",
                "content": "Was kann man auf diesen Bildern erkennen?",
                "images": images
            }
        ],
        stream=True
    )
    for chunk in response:
        # Replacing the print statement with a function to return the content as audio
        print(chunk['message']['content'], end='', flush=True)
        tts.speak(chunk['message']['content'])

vision_stream()