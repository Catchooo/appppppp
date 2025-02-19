from PIL import Image
import pandas as pd
from fpdf import FPDF

FOLDER = './files/'

def get_new_path(file_path):
    return FOLDER + file_path


def png_to_jpg(png_file_path):
    img = Image.open(png_file_path)

    jpg_file_name = png_file_path.rsplit(FOLDER)[1].rsplit('.')[0]+'.jpg'

    jpg_img = img.convert('RGB')

    new_path = get_new_path(jpg_file_name)
    
    jpg_img.save(new_path)

    return new_path




def jpg_to_png(jpg_file_path):
    img = Image.open(jpg_file_path)

    png_file_name = jpg_file_path.rsplit(FOLDER)[1].rsplit('.')[0]+'.png'

    png_img = img.convert('RGBA')

    new_path = get_new_path(png_file_name)
    
    png_img.save(new_path)

    return new_path


def excel_to_csv(excel_file_path):
    df = pd.read_excel(excel_file_path)

    csv_file_name = excel_file_path.rsplit(FOLDER)[1].rsplit('.')[0]+'.csv'

    new_path = get_new_path(csv_file_name)
    df.to_csv(new_path,index = False)

    return new_path

def csv_to_excel(csv_file_path):
    df = pd.read_csv(csv_file_path)

    excel_file_name = csv_file_path.rsplit(FOLDER)[1].rsplit('.')[0]+'.xlsx'

    new_path = get_new_path(excel_file_name)
    df.to_excel(new_path,index = False)

def txt_to_pdf(txt_file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)

    pdf_file_name = txt_file_path.rsplit(FOLDER)[1].rsplit('.')[0]+'.pdf'


    try:
        with open(txt_file_path, 'r', encoding='UTF-8') as file:
            for line in file:
                pdf.cell(200, 10, txt=line.strip(), ln=True)  
    except FileNotFoundError:
        print(f"Помилка: файл '{txt_file_path}' не знайдено.")
        return

    pdf_file_path = get_new_path(pdf_file_name)

    pdf.output(pdf_file_path, 'F')

    return pdf_file_path


if __name__ == '__main__':
    txt_to_pdf(FOLDER+'file.txt')

