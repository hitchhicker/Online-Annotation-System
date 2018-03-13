import os

from PIL import Image


def get_image_width_and_height(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width, height


def get_no_repeated_save_path_and_filename(base_path, filename):
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    save_path = os.path.abspath(os.path.join(base_path, filename))
    while os.path.exists(save_path):
        file, ext = filename.split('.')
        filename = file + '_1.' + ext
        save_path = os.path.abspath(os.path.join(base_path, filename))
    return save_path, filename


def count_files_by_category(base_path, category):
    category_path = os.path.join(base_path, category)
    if not os.path.exists(category_path):
        return 0
    else:
        return len([_ for _ in os.listdir(category_path)])
