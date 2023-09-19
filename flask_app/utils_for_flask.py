import os
from datetime import datetime

import PyPDF2

from flask_app.read_resume_file import app


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
