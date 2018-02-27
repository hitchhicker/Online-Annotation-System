import os
import logging

from flask import Flask
from flask import Response
from flask_principal import Principal
from flask_login import LoginManager
from flask_cors import CORS
import views
from models import DB

# logging.basicConfig(filename='log', filemode='a', level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

app.add_url_rule('/', view_func=views.home)
app.add_url_rule('/upload', view_func=views.upload_annotations_and_photo, methods=['POST'])
app.add_url_rule('/login', view_func=views.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=views.logout)
app.secret_key = '\xcc\x93\xc6\xc0\xf2*sY\xadWn\xa9\x9e\xb6x\xb5\xc8{2\xe7Z\n\x07\xa5'
CORS(app, resources={r"/upload": {"origins": "*"}})
Principal(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "views.login"


@login_manager.user_loader
def load_user(user_id):
    return DB.find_user(id=user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return Response('You have not logged in.', 401, {'WWWAuthenticate': 'Basic realm="Login Required"'})


if __name__ == '__main__':
    if os.environ.get("XML_SAVE_PATH") is None:
        raise RuntimeError(
            "Please set environment variable XML_SAVE_PATH, this variable indicates where we save XML files in PASCAL VOC format")
    if os.environ.get("IMAGE_SAVE_PATH") is None:
        raise RuntimeError(
            "Please set environment variable IMAGE_SAVE_PATH,  this variable indicates where we save images")
    app.run(host='0.0.0.0', debug=False)
