from flask import Flask,render_template,request,redirect,send_file,send_from_directory
from glob import glob
from io import BytesIO
from zipfile import ZipFile
from scripts.AlarmConfig import main
import os
import shutil

app = Flask(__name__)

@app.route("/")
def index():
    os.system("mkdir csvConfigs")
    os.system("mkdir jsonConfigs")
    os.system("mkdir output")

    os.system("rm -rf csvConfigs/*")
    os.system("rm -rf jsonConfigs/*")
    os.system("rm -rf output/*")
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        file = request.files['file']
        file.save("./csvConfigs/upload.csv")
    return redirect("/download-configs",code=302)

@app.route('/download-configs')
def downloadConfigs():
    main('./csvConfigs/upload.csv')
    shutil.make_archive('output/configs', 'zip', './jsonConfigs')
    path = 'output/configs.zip'


    return send_file(
      path, as_attachment=True
    )
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,threaded=True)