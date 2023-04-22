from PIL import Image, ImageFilter
import io
import pilgram


def pilgram_filters(imgBytes, filttype):
    if type(imgBytes) == type(bytes()):
        stream = io.BytesIO(imgBytes)
        img = Image.open(stream)
    else:
        img = imgBytes
    imgres = eval(f'pilgram.{filttype}')(img)
    return imgres

def grayscale(imgBytes):
    if type(imgBytes) == type(bytes()):
        stream = io.BytesIO(imgBytes)
        img = Image.open(stream)
    else:
        img = imgBytes
    return img.convert('L')


def filter(imgBytes, filttype):
    if type(imgBytes) == type(bytes()):
        stream = io.BytesIO(imgBytes)
        img = Image.open(stream)
    else:
        img = imgBytes
    img = img.filter(eval(f'ImageFilter.{filttype}'))
    return img