import convertor as convert
from flask import request, render_template, Flask, send_file
import os
import shutil

app = Flask('Convertor')

UPLOAD_FOLDER = convert.FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '1234567890'

ALLOWED_EXTENSIONS = ['pdf', 'txt', 'jpg', 'png', 'csv', 'xlsx']

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

def clear_files_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@app.route('/submit', methods=['POST'])
def submit():
    file = request.files['file']
    conversion_type = request.form['conversion']
    filename, file_extension = os.path.splitext(file.filename)

    if file_extension[1:] not in ALLOWED_EXTENSIONS:
        return 'Файл не підтримується нашою системою', 400

    if conversion_type == 'png_to_jpg' and file_extension[1:] != 'png':
        return 'Для конвертації в JPG необхідно завантажити PNG файл', 400
    elif conversion_type == 'jpg_to_png' and file_extension[1:] != 'jpg':
        return 'Для конвертації в PNG необхідно завантажити JPG файл', 400
    elif conversion_type == 'txt_to_pdf' and file_extension[1:] != 'txt':
        return 'Для конвертації в PDF необхідно завантажити TXT файл', 400
    elif conversion_type == 'pdf_to_txt' and file_extension[1:] != 'pdf':
        return 'Для конвертації в TXT необхідно завантажити PDF файл', 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    if conversion_type == 'png_to_jpg':
        converted_filename = convert.png_to_jpg(file_path)
    elif conversion_type == 'jpg_to_png':
        converted_filename = convert.jpg_to_png(file_path)
    elif conversion_type == 'txt_to_pdf':
        converted_filename = convert.txt_to_pdf(file_path)
    elif conversion_type == 'pdf_to_txt':
        converted_filename = convert.pdf_to_txt(file_path)
    else:
        return 'Error'

    clear_files_folder(app.config['UPLOAD_FOLDER'])

    return send_file(converted_filename, as_attachment=True), 200

if __name__ == '__main__':
    app.run(debug=True)
