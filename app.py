from flask import Flask,render_template,request,redirect,send_file,send_from_directory
from glob import glob
from io import BytesIO
from zipfile import ZipFile
from scripts.AlarmConfig import main
import os

app = Flask(__name__)

@app.route("/")
def index():
    os.system("rm -rf csvConfigs/*")
    os.system("rm -rf jsonConfigs/*")
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
    target = './jsonConfigs'

    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for file in glob(os.path.join(target, '*.json')):
            zf.write(file, os.path.basename(file))
    stream.seek(0)

    return send_from_directory(
        stream,
        as_attachment=True,
        attachment_filename='archive.zip'
    )
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,threaded=True)