import ollama
from PIL import Image

# Function to load all pictures from "screens_backup" directory
images = []

def load_images() -> None:
    images.clear()
    for i in range(1):
        images.append(f"screens/sc-{i}-compressed.png")
    print("==>Images loaded")

def vision() -> str:
    load_images()

    #Debugging
    #image = Image.open(images[0])
    #image.show()

    response = ollama.chat(
       model="llama3.2-vision",
       messages=[
            {
                "role": "user",
                "content": "Was kann man auf diesen Bildern erkennen?",
                "images": images
            }
        ]
    )
    return response['message']['content']

print(vision())

