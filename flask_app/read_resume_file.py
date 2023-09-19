from datetime import datetime

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

import PyPDF2
import os

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
# NOT_ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key_here'


def pdf_to_text(file_path):
    """Convert a PDF file to text."""
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def save_text_as_file(text, original_filename):
    """Save a given text into a .txt file."""
    # Removing the file extension and adding a timestamp
    filename_without_ext = os.path.splitext(original_filename)[0]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    txt_filename = f"{filename_without_ext}_{timestamp}.txt"
    txt_file_path = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
    return txt_file_path


def allowed_file(filename):
    """

    :param filename:
    :return:
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    """Extract text from the provided PDF file and save it to a .txt file."""
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

    # Saving the extracted text to a .txt file
    txt_file_path = file_path.replace('.pdf', '.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

    return txt_file_path  # Return the path to the .txt file


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/upload', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            flash('File uploaded successfully!')
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Convert the uploaded PDF to text
            extracted_text = pdf_to_text(file_path)
            # Save the extracted text
            save_text_as_file(extracted_text, filename)

            return redirect(url_for('success'))
    return render_template('upload.html')


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5001, debug=True)
