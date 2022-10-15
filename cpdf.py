from fpdf import FPDF
import json

def create():
    with open('cache1.json') as f:
        need_list = json.load(f)
    f.close()
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
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
        pdf.multi_cell(0, 10,str(quest)+". "+i, new_x="LMARGIN", new_y="NEXT",border=True)
        while counter%4 < len(choice):
            pdf.cell(95, 10, letter[letter_num] +choice[counter],border=True)
            pdf.cell(95,10, letter[letter_num+1] +choice[counter+1],border=True)
            pdf.cell(95,10,"",new_x="LMARGIN", new_y="NEXT")
            counter+=2
            letter_num+=2
            if counter%4 == 0:
                break
        letter_num=0
        quest+=1
    pdf.rect(5, 5, 200, 287, 'D')
    pdf.output('questionnaire.pdf')
