from flask import Flask, render_template, request, redirect, url_for
import os
import glob
from utils import * 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_latest_file():
    list_of_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def remove_files():
    files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    for f in files:
        os.remove(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
  return render_template('index.html')

  
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        remove_files()
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('display', filename=filename))
    else:
        return "Invalid file format or file too large"

@app.route('/display')
def display():
    latest_file = get_latest_file()
    if latest_file and os.path.isfile(latest_file):
        filename = os.path.basename(latest_file)
        title, paragraphs = get_story(latest_file)
        # paragraphs = ["S", "U", "A", "T", filename, latest_file]
        return render_template('display.html', filename=filename, title=title, paragraphs=paragraphs)
    else:
        return "No uploaded files or file not found"

if __name__ == '__main__':
    app.run(debug=False)
