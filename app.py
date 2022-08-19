from flask import Flask,render_template,request
from werkzeug.utils import secure_filename
from scripts.AlarmConfig import main

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # main('./csvConfigs/upload.csv')
        fileName = file.filename
        file.save(f"./csvConfigs/{secure_filename(fileName)}")
    return 'file uploaded successfully'