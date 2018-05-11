import os

import sys
current_dir_path = os.path.dirname(os.path.realpath(__file__))
project_root_path = os.path.join(current_dir_path, os.pardir)

sys.path.insert(0, project_root_path)

from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

import jinja2
import file_transcriber

templates_folder_path = os.path.join(current_dir_path, "web_demo", "templates")
js_folder_path = os.path.join(templates_folder_path, "js")
tmp_folder_path = os.path.join(project_root_path, "tmp")

app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader(templates_folder_path)




@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/continuous")
def continuous():
    return render_template("continuous.html")

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(js_folder_path, path)

@app.route('/transcribe_file', methods=['POST'])
def transcribe_file():
    if request.method == 'POST':
        f = request.files['wav_file']
        file_path = os.path.join(tmp_folder_path, secure_filename(f.filename))
        f.save(file_path)

        file_transcriber.init()
        t = file_transcriber.transcribe_file(file_path)

        return t





app.run(host= '0.0.0.0', port=5000, debug=True)