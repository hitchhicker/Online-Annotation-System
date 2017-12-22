# -*- coding: utf-8 -*-
import base64
import os

from flask import render_template, jsonify
from flask import request
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor

from models import Object, Size, Annotations
from xml_generater import XMLGenerator
from utils import get_image_width_and_height

executor = ThreadPoolExecutor(1)

BASE_SAVE_PATH = "/Users/YU/Desktop/"


def home():
    return render_template('home.html')


def upload_annotations_and_photo():
    if request.method == 'POST':
        annotations = Annotations(request.json['annotations'])
        print(annotations)
        for k in request.json.values():
            print(type(k))
        image = request.json['imageBase64']
        filename = request.json['filename']
        files = []
        if image:
            filename = secure_filename(filename)
            files.append({'name': filename})
            executor.submit(_async_upload_image, image, filename, annotations)
            return jsonify(files=files), 201


def _async_upload_image(img, filename, annotations):
    save_path = os.path.abspath(os.path.join('./static/images', filename))
    with open(save_path, "wb") as fh:
        fh.write(base64.decodebytes(str.encode(img)))
    width, height = get_image_width_and_height(save_path)

    objects = []
    for label, bounding_box in annotations:
        obj = Object(name=label, bounding_box=bounding_box)
        objects += obj,
    size = Size(width=width, height=height, depth=3)
    xml_generator = XMLGenerator(folder=label, filename=filename, path=save_path, size=size, objects=objects)
    xml_generator.build_xml_tree()
    xml_generator.write_xml_to_path(base_path=BASE_SAVE_PATH)
