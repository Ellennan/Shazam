from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
# app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'upload/'

ALLOWED_EXTENSIONS = {'wav', 'mp3'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def interface():
    return render_template('interface.html')


@app.route('/fingerprint')
def fingerprint():
    return render_template('fingerprint.html')


@app.route('/find')
def find():
    return render_template('find.html')


@app.route('/database')
def database():
    from run import database
    songs = database()
    return render_template('database.html', songs=songs)


@app.route('/fingerprint/result', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return redirect(url_for('fingerprint'))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(url_for('fingerprint'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            from run import fingerprint
            result = fingerprint(app.config['UPLOAD_FOLDER'] + filename)
            return render_template('fingerprint_result.html', re=result)


@app.route('/find/result', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return redirect(url_for('find'))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(url_for('find'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            from run import find
            result = find(app.config['UPLOAD_FOLDER'] + filename)
            return render_template('find_result.html', songs=result)


if __name__ == '__main__':
    app.run(debug=True)


#  deploy cmd: waitress-serve --port=8080 --call app:create_app
# http://localhost:8080/
def create_app():
    return app
