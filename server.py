from flask import Flask
import views


app = Flask(__name__)


app.add_url_rule('/', view_func=views.home)
app.add_url_rule('/upload', view_func=views.upload_annotations_and_photo, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
