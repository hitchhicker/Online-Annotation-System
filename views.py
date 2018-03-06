# -*- coding: utf-8 -*-
import base64
import os
import logging

from flask import render_template, jsonify, request, current_app, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import Identity, identity_changed, AnonymousIdentity

from wtforms import PasswordField, StringField, validators, SubmitField
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor

from models import Object, Size, Annotations, DB
from xml_generater import XMLGenerator
from utils import get_image_width_and_height, get_no_repeated_save_path_and_filename

executor = ThreadPoolExecutor(1)
logger = logging.getLogger("views")
XML_SAVE_PATH = os.environ.get("XML_SAVE_PATH")
IMAGE_SAVE_PATH = os.environ.get("IMAGE_SAVE_PATH")
ALLOWED_CATEGORIES = ["plastique|塑料", "metal|金属", "papier|纸", "verre|玻璃", "menage|绿色垃圾", "encombrants|大体积垃圾",
                      "electroniques|电子产品", "piles|电池",
                      "ampoule|灯泡", "vetements|衣服", "medicaments|药品"]


@login_required
def home():
    return render_template('home.html',
                           categories=ALLOWED_CATEGORIES,
                           current_user=current_user)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Sign In')


def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = DB.find_user(username=form.username.data)
        if user and form.password.data == user.password and form.username.data == user.username:
            login_user(user, remember=True)
            logger.info("User " + str(user) + " logged in.")
            session['user_id'] = user.id
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            return redirect('/')
    return render_template('login.html', title='Sign In', form=form)


@login_required
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect('/login')


@login_required
def upload_annotations_and_photo():
    if request.method == 'POST':
        logger.info("Receive a request post.")
        annotations = Annotations(request.json['annotations'])
        logger.info("Annotation information: " + str(annotations))
        image = request.json['imageBase64']
        filename = request.json['filename']
        files = []
        if image:
            filename = secure_filename(filename)
            files.append({'name': filename})
            _upload_image(image, filename, annotations)
            return jsonify(files=files), 201


def _upload_image(img, filename, annotations):
    objects = [Object(name=label, bounding_box=bounding_box) for label, bounding_box in annotations]
    label = objects[0].name if len(objects) else None
    if label is not None:
        save_path, filename = get_no_repeated_save_path_and_filename(
            os.path.join(IMAGE_SAVE_PATH, label), filename)
        logger.info("Start saving image. in: " + save_path)
        _save_image(img, save_path)
        logger.info("Saved image in: " + save_path)
        width, height = get_image_width_and_height(save_path)
        logger.info("Image size: " + str((width, height)))
        size = Size(width=width, height=height, depth=3)
        xml_generator = XMLGenerator(folder=label, filename=filename, path=save_path, size=size, objects=objects)
        xml_generator.build_xml_tree()
        xml_generator.write_xml_to_path(base_path=XML_SAVE_PATH)


def _save_image(img, where_to_save):
    with open(where_to_save, "wb") as fh:
        fh.write(base64.decodebytes(str.encode(img)))


def all_categories():
    return jsonify([cat.split('|')[0] for cat in ALLOWED_CATEGORIES])
