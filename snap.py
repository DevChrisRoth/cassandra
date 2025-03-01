import os.path
import shutil
import time
from PIL import Image
from mss import mss
import torch
import torchvision.transforms as t
import numpy as np
import keyboard

# Pfad für Screenshots
pathName = "screens"
whileLoopIterator = 1

# Main function to take screenshots periodically
def screencapture() -> None:
    #Cleanup folder
    if os.path.exists(pathName):
        shutil.rmtree(pathName)
    if not os.path.exists(pathName):
        os.mkdir(pathName)

    # Take 5 new screenshots and compress them
    with mss() as sct:
        sct.compression_level = 9
        while whileLoopIterator:
            for j in range(5):
                sct.shot(mon=1, output=pathName + "/sc-%d.png" % j)
                compress_image(j)
                time.sleep(1)


#-----------Bild optimierung--------------#
# Prüfe, ob OpenCV verfügbar ist
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


# Zielauflösung
TARGET_SIZE = (1920, 1080)

# Nutze GPU, falls vorhanden
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Compress the image and set new resolution to 16:9, quality 55%
# Create new image and delete the old one
def compress_image(img_number: int) -> None:
    img_path = f"{pathName}/sc-{img_number}.png"
    output_path = f"{pathName}/sc-{img_number}-compressed.png"

    # Lade Bild
    img = Image.open(img_path).convert("RGB")
    original_width, original_height = img.size

    # **Seitenverhältnis berechnen**
    target_aspect = 16 / 9
    current_aspect = original_width / original_height

    if current_aspect > target_aspect:
        # Bild ist **zu breit** → oben und unten mit Rändern füllen
        new_width = original_width
        new_height = int(original_width / target_aspect)
    else:
        # Bild ist **zu hoch** → links und rechts mit Rändern füllen
        new_height = original_height
        new_width = int(original_height * target_aspect)

    # **Neues Bild mit Rändern erstellen**
    new_img = Image.new("RGB", (new_width, new_height), (255, 255, 255))  # Weiß als Füllfarbe
    new_img.paste(img, ((new_width - original_width) // 2, (new_height - original_height) // 2))

    # **Schnellere Skalierung mit OpenCV**
    if OPENCV_AVAILABLE:
        img = cv2.cvtColor(np.array(new_img), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, TARGET_SIZE, interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, 55])
    else:
        # **GPU-Optimierte Skalierung mit PyTorch**
        if torch.cuda.is_available():
            transform = t.Compose([
                t.Resize(TARGET_SIZE, interpolation=t.InterpolationMode.LANCZOS),
                t.ToPILImage()
            ])
            new_img = transform(t.ToTensor()(new_img).to(DEVICE))
        else:
            # **Fallback: Standard PIL**
            new_img.thumbnail(TARGET_SIZE, Image.Resampling.LANCZOS)

        # Speichern mit optimierter JPEG-Kompression
        new_img.save(output_path, "JPEG", optimize=True, quality=55, progressive=True, subsampling="4:2:0")

    os.remove("%s/sc-%d.png" % (pathName, img_number))