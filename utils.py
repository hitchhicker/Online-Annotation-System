from PIL import Image


def get_image_width_and_height(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width, height
