import os.path
import shutil
import time
from PIL import Image
from mss import mss

pathName = "screens"
whileLoopIterator = 1

def screencapture() -> None:
    #Cleanup folder
    if os.path.exists(pathName):
        shutil.rmtree(pathName)
    if not os.path.exists(pathName):
        os.mkdir(pathName)


    with mss() as sct:
        sct.compression_level = 9
        while whileLoopIterator:
            for j in range(5):
                sct.shot(mon=1, output=pathName + "/sc-%d.png" % j)
                compress_image(j)
                time.sleep(1)
            print("new iteration")


def compress_image(img_number: int) -> None:
    img = Image.open("%s/sc-%d.png" % (pathName, img_number))
    img = img.resize((1280, 920), Image.Resampling.LANCZOS)
    img.save("%s/sc-%d-compressed.png" % (pathName, img_number), optimize=True, quality=55)
    os.remove("%s/sc-%d.png" % (pathName, img_number))


screencapture()