from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import jinja2

import os

import file_transcriber

app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader('web/templates')




@app.route("/")
def hello():
    return render_template("home.html")

@app.route('/transcribe_file', methods=['POST'])
def transcribe_file():
    if request.method == 'POST':
        f = request.files['wav_file']
        file_path = os.path.join(os.getcwd(), "tmp", secure_filename(f.filename))
        f.save(file_path)

        file_transcriber.init()
        t = file_transcriber.transcribe_file(file_path)

        return "transcription: "+t





app.run(host= '0.0.0.0', port=5000, debug=True)