from PIL import Image, ImageFilter
import io

def grayscale(imgBytes):
    stream = io.BytesIO(imgBytes)
    img = Image.open(stream)
    return img.convert('L')

def filter(imgBytes, filttype):
    stream = io.BytesIO(imgBytes)
    img = Image.open(stream)
    img = img.filter(eval(f'ImageFilter.{filttype}'))
    return img