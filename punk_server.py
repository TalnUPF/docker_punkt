import os
import logging

from flask import Flask, flash, request, Response, url_for, redirect, render_template_string
from werkzeug.utils import secure_filename

PROST_OUT_DIR = 'prost_output'
PREDICTION_FILE = 'prediction.txt'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['wav', 'align'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def store_file(param):

    if param not in request.files:
        raise Exception('No %s file parameter found!' % param)

    upload_file = request.files[param]
    if not upload_file or upload_file.filename == '':
        raise Exception('No selected file!')

    if not allowed_file(upload_file.filename):
        raise Exception('Invalid file type!')

    filename = secure_filename(upload_file.filename)
    upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return filename


@app.route('/punkt', methods=['GET','POST'])
def punkt():
    if request.method == 'POST':

        try:
            audio_filename = store_file('audio')
            align_filename = store_file('align')
            basename = audio_filename.rsplit(".", 1)[0]

            os.system("cd Proscripter; ./run.sh ../uploads/%s ../uploads/%s ../%s" % (audio_filename, align_filename, PROST_OUT_DIR))

            os.system("cd krisPunctuator/; ./run.sh ../%s/%s/proscript/%s.proscript.csv ../%s/%s" % (PROST_OUT_DIR, basename, basename, PROST_OUT_DIR, PREDICTION_FILE))

            output = open("%s/%s" % (PROST_OUT_DIR, PREDICTION_FILE)).read()            
            return output

        except Exception as e:
            flash(str(e))
            return redirect(request.url)

    return render_template_string('''
    <!doctype html>
    <title>Punktuator service</title>
    <h1>Punktuator service</h1>
    <h2>Set the sentence and the related audio file to be used:</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul class=flashes>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method=post enctype=multipart/form-data>
      <p>Audio file: <input type=file name=audio></p>
      <p>Align file: <input type=file name=align></p>
      <input type=submit value=Upload>
    </form>
    ''')


@app.route('/')
def index():
    return "This is the base page for the punktuation service."

def launch_server():

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(PROST_OUT_DIR):
        os.makedirs(PROST_OUT_DIR)

    app.debug = True
    app.debug_log_format = "%(asctime)s - %(levelname)s - %(message)s"
    app.config['PROPAGATE_EXCEPTIONS'] = True

    app.secret_key = 'super secret key'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.run(host='0.0.0.0', port=80)

if __name__ == "__main__":

    launch_server()
