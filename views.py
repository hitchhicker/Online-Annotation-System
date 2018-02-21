# -*- coding: utf-8 -*-
import base64
import os
import logging

from flask import render_template, jsonify, request, current_app, redirect, session
from flask_login import login_user, logout_user, login_required
from flask_principal import Identity, identity_changed, AnonymousIdentity
from wtforms import PasswordField, StringField, validators, SubmitField
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor

from models import Object, Size, Annotations, DB
from xml_generater import XMLGenerator
from utils import get_image_width_and_height


executor = ThreadPoolExecutor(1)
logger = logging.getLogger("views")
XML_SAVE_PATH = os.environ.get("XML_SAVE_PATH")
IMAGE_SAVE_PATH = os.environ.get("IMAGE_SAVE_PATH")


@login_required
def home():
    return render_template('home.html')


def upload_annotations_and_photo():
    if request.method == 'POST':
        annotations = Annotations(request.json['annotations'])
        logger.info(annotations)
        image = request.json['imageBase64']
        filename = request.json['filename']
        files = []
        if image:
            filename = secure_filename(filename)
            files.append({'name': filename})
            executor.submit(_async_upload_image, image, filename, annotations)
            return jsonify(files=files), 201


def _async_upload_image(img, filename, annotations):
    save_path = os.path.abspath(os.path.join(IMAGE_SAVE_PATH, filename))
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
    xml_generator.write_xml_to_path(base_path=XML_SAVE_PATH)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Sign In')


# @app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = DB.find_user(username=form.username.data)
        if user and form.password.data == user.password and form.username.data == user.username:
            login_user(user)
            session['user_id'] = user.id
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            return redirect('/')
    return render_template('login.html', title='Sign In', form=form)


# @app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect('/login')
