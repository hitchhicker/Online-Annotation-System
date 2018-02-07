import os
import logging

from flask import Flask
import views

logging.basicConfig(filename='log', filemode='a', level=logging.INFO)

app = Flask(__name__)

app.add_url_rule('/', view_func=views.home)
app.add_url_rule('/upload', view_func=views.upload_annotations_and_photo, methods=['POST'])

if __name__ == '__main__':
    if os.environ.get("XML_SAVE_PATH") is None:
        raise RuntimeError(
            "Please set environment variable XML_SAVE_PATH, this variable indicates where we save XML files in PASCAL VOC format")
    if os.environ.get("IMAGE_SAVE_PATH") is None:
        raise RuntimeError(
            "Please set environment variable IMAGE_SAVE_PATH,  this variable indicates where we save images")
    app.run(debug=True)
c