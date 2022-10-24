from fpdf import FPDF
import json
from kivy.storage.jsonstore import JsonStore


from pdf2image import  convert_from_path

def convert_pdf(pdf_path, save_dir, res=400):
    pages = convert_from_path(pdf_path, res,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')

    name_with_extension = pdf_path.rsplit('/')[-1]
    name = name_with_extension.rsplit('.')[0]
    img_list = []

    for idx, page in enumerate(pages):
        page.save(f'{save_dir}/{name}_{idx}.png','PNG')
        img_list.append(f'{save_dir}/{name}_{idx}.png')

    with open('cache.json','w') as f:
        json.dump(img_list,f,indent=2)
    f.close()

