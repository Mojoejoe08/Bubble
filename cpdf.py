from fpdf import FPDF
import json
from kivy.storage.jsonstore import JsonStore



class create():
    with open('cache1.json') as f:
        need_list = json.load(f)
    f.close()

    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(True)
    pdf.add_page()
    pdf.rect(5, 5, 200, 287, 'D')
    num = 2
    cho = 4
    name = []
    choice = []
    quest = 1
    letter = ["a. ", "b. ", "c. ", "d. "]

    subj_name = need_list['subject']['subject_name']
    tech_name = need_list['teacher']['teacher_name']

    with open('new_ques.json') as f:
        data = json.load(f)
        for question in data:
            name.append(data[question]['question'])
            choice.append(data[question]['a'])
            choice.append(data[question]['b'])
            choice.append(data[question]['c'])
            choice.append(data[question]['d'])
    f.close()

    pdf.set_font('times', '', 16)
    pdf.cell(55, 10, "Subject:", border=True)
    pdf.cell(135, 10, subj_name, border=True)
    pdf.cell(0, 10, "", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(55, 10, "Teacher:", border=True)
    pdf.cell(135, 10, tech_name, border=True)
    pdf.cell(0, 10, "", new_x="LMARGIN", new_y="NEXT")
    counter = 0
    letter_num = 0
    for i in name:
        pdf.multi_cell(0, 10,str(quest)+". "+i, new_x="LMARGIN", new_y="NEXT")
        while counter%4 < len(choice):
            pdf.cell(95, 10, letter[letter_num] +choice[counter])
            pdf.cell(95,10, letter[letter_num+1] +choice[counter+1])
            pdf.cell(95,10,"",new_x="LMARGIN", new_y="NEXT")
            counter+=2
            letter_num+=2
            if counter%4 == 0:
                break
        letter_num=0
        quest+=1
        pdf.rect(5, 5, 200, 287, 'D')
    pdf.output('questionnaire.pdf')

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

