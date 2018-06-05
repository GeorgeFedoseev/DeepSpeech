import os

import sys
current_dir_path = os.path.dirname(os.path.realpath(__file__))
project_root_path = os.path.join(current_dir_path, os.pardir)

sys.path.insert(0, project_root_path)

from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

import jinja2
import file_transcriber

import json
from search import yt_search

templates_folder_path = os.path.join(current_dir_path, "flask", "templates")
js_folder_path = os.path.join(templates_folder_path, "js")
tmp_folder_path = os.path.join(project_root_path, "tmp")

app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader(templates_folder_path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(js_folder_path, path)
    

@app.route("/")
def continuous():
    return render_template("continuous.html")

@app.route("/search")
def search():
    return render_template("search.html")


@app.route('/file')
def single_file_transcribe():
    return render_template("single_file_transcribe.html")

@app.route('/search_results')
def get_search_results():
    query = request.args.get('q', '')
    #return query
    return json.dumps(yt_search.search(query), indent=3, ensure_ascii=False)

@app.route('/transcribe_file', methods=['POST'])
def transcribe_file():
    if request.method == 'POST':
        f = request.files['wav_file']
        file_path = os.path.join(tmp_folder_path, secure_filename(f.filename))
        f.save(file_path)

        t = file_transcriber.transcribe_file(file_path)

        return t
        





app.run(host= '0.0.0.0', port=5000, debug=True)