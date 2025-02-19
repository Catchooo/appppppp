import convertor as convert
from flask import request, render_template,Flask,send_file
import os

app = Flask('Convertor')

UPLOAD_FOLDER = convert.FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '1234567890'

ALLOWED_EXTENSIONS = ['pdf','txt','jpg','png','csv','xlsx']

@app.route('/',methods = ['GET','POST'])
def index():
    return render_template('index.html')

#todo після того як буде прописаний основний функціонал функції нижче прописати алгоритм який буде очищувати нашу папку files від непотрібних файлів
# ! прописати валідацію на те чи можемо конвертувати файл в залежності від вибраної опції, приклад: вибрано опція png to jpg, якщо користувач надішле не png файл програма викине помилку 
@app.route('/submit',methods = ['POST'])
def submit():

    file = request.files['file']
    conversion_type = request.form['conversion']

    if file.filename.split('.')[1] in ALLOWED_EXTENSIONS:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
        file.save(file_path)
    else:
        return 'Файл не підтримується нашою системою', 400
    

    if conversion_type == 'png_to_jpg':
        converted_filename = convert.png_to_jpg(file_path)
    elif conversion_type == 'jpg_to_png':
        converted_filename = convert.jpg_to_png(file_path)
    # todo прописати код для інших опцій які є у випадючому списку        
    else:
        return 'Error'


    return send_file(converted_filename,as_attachment=True), 200




if __name__ =='__main__':
    app.run(debug=True)