import imutils
import kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
kivy.require('1.9.0')
import cv2
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
from functools import *
import json
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivy.base import runTouchApp
import sqlite3
from kivy.uix.dropdown import DropDown
from pdf2image import convert_from_path
import cpdf
from fpdf import FPDF
from kivy.uix.popup import Popup
from kivy.config import Config
Config.set('graphics', 'resizable', True)

class MyPopUp(Popup):
    def std_save(self, value):
        self.std_name = value
        self.store = JsonStore('cache.json')
        self.store.put('std', student_name =self.std_name)

    def btnn(self):
        pops = CameraClick()
        pops.open()

def convert(list):
    return tuple(list)

class Creating_json:
    def __init__(self, quest, question_name, a, b, c, d):
        self.quest = quest
        self.question_name = question_name
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def save_to_json(self, filename):
        new_ques = self.quest
        with open(filename) as f:
            person_dict = json.load(f)
            person_dict[new_ques] = {'question': self.question_name, 'a': self.a, 'b': self.b, 'c': self.c,
                                     'd': self.d}
        f.close()
        with open(filename, 'w') as f:
            person_dict[new_ques] = {'question': self.question_name, 'a': self.a, 'b': self.b, 'c': self.c,
                                     'd': self.d}
            json.dump(person_dict, f, indent=2)
        f.close()


class MainWindow(Screen):
    pass

class CheckExamWindow(Screen):
    min_height = NumericProperty(0)
    def set_btn(self):
        show_set_name = []
        mini_height = 0
        con = sqlite3.connect("exam_db.db")
        c = con.cursor()
        # Create to Set Table -----------
        for row in c.execute("select * from set_tbl"):
            show_set_name.append(row[1])
        c.close()
        con.commit()
        con.close()

        for name in show_set_name:
            self.r = Button(text=str(name), text_size= (self.width+80, self.height+80),font_size=(self.width/80)*(self.height/5), size_hint=(.6, None), height=50,
                                font_name='century gothic', color=(1, 1, 1, 1),
                                background_color=(0 / 255, 107 / 255, 56 / 255, 1), background_normal='',halign='left')
            self.b = Button( text_size=self.size, size_hint=(.2, None), height=50,
                            font_name='century gothic', background_normal='itemanalysis_icon1.png')
            self.a = Button( text_size=self.size, size_hint=(.2, None), height=50,
                            font_name='century gothic', background_normal='trash_icon1.png')
            self.ids.check_exam_container.add_widget(self.r)
            self.ids.check_exam_container.add_widget(self.b)
            self.ids.check_exam_container.add_widget(self.a)
            # self.r.bind(on_press=partial(self.edit_question, question))
            mini_height += 50
        self.min_height = mini_height

class CreateExamWindow(Screen):
    def __init__(self, **kwargs):
        super(CreateExamWindow, self).__init__(**kwargs)
        self.store = JsonStore('cache1.json')

    def get_val(self):
        try:
            editing_ques_num = int(self.ids.question_num.text)
            teacher_name = str(self.ids.tech_name.text)
            subject_name = str(self.ids.subj_name.text)
        except:
            editing_ques_num = 0
            teacher_name = ''
            subject_name = ''
        self.store.put('teacher', teacher_name=teacher_name)
        self.store.put('subject', subject_name=subject_name)
        # json_name = subject_name + ".json"
        with open('ques.json') as f:
            data = json.load(f)
        f.close()
        with open('new_ques.json', 'w') as f:
            json.dump(data, f, indent=2)
        f.close()

        for i in range(2, editing_ques_num + 1):
            p = Creating_json("QUESTION " + str(i), "", "", "", "", "")
            p.save_to_json('new_ques.json')


class QuestionnaireWindow(Screen):
    count = 1
    min_height = NumericProperty(0)

    def load_items(self):
        mini_height = 0
        # self.ids.main_load.remove_widget(self.ids.load_items)
        with open('new_ques.json', 'r') as f:
            ques_list = json.load(f)
            for question in ques_list:
                self.r = Button(text=str(question), text_size=self.size, size_hint=(1, None),height= 50,
                                font_name='century gothic', color=(0, 0, 0, 1),
                                background_color=(0 / 255, 107 / 255, 56 / 255, 1), background_normal='')
                self.ids.container.add_widget(self.r)
                self.r.bind(on_press=partial(self.edit_question, question))
                mini_height+=50
        f.close()
        self.min_height = mini_height

    def edit_question(self, question, *args):
        self.store = JsonStore('cache.json')
        self.store.put('cache', editing_que = question)
        self.manager.transition.direction = 'left'
        self.manager.current = 'input_questionnaire'

    def createPdf(self):
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
        pdf.cell(0, 10, "", new_x="LMARGIN", new_y="NEXT")
        counter = 0
        letter_num = 0
        for i in name:
            pdf.multi_cell(0, 10, str(quest) + ". " + i, new_x="LMARGIN", new_y="NEXT")
            while counter % 4 < len(choice):
                pdf.cell(95, 10, letter[letter_num] + choice[counter])
                pdf.cell(95, 10, letter[letter_num + 1] + choice[counter + 1])
                pdf.cell(95, 10, "", new_x="LMARGIN", new_y="NEXT")
                counter += 2
                letter_num += 2
                if counter % 4 == 0:
                    break
            letter_num = 0
            quest += 1
            pdf.rect(5, 5, 200, 287, 'D')
        pdf.output('questionnaire.pdf')
        cpdf.convert_pdf('/Users/Administrator/PycharmProjects/AutoMark/questionnaire.pdf',
                         '/Users/Administrator/PycharmProjects/AutoMark/img/')

class InputQuestionWindow(Screen):

    def insert_val(self):
        try:
            question_in = str(self.ids.i.text)
            input_a = str(self.ids.a.text)
            input_b = str(self.ids.b.text)
            input_c = str(self.ids.c.text)
            input_d = str(self.ids.d.text)
        except:
            question_in = ''
            input_a = ''
            input_b = ''
            input_c = ''
            input_d = ''
        self.store = JsonStore('cache.json')
        self.ques_num = self.store.get('cache')['editing_que']

        with open('new_ques.json') as f:
            person_dict = json.load(f)
            person_dict[self.ques_num] = {'question': question_in, 'a': input_a, 'b': input_b, 'c': input_c,
                                     'd': input_d}
        with open('new_ques.json', 'w') as f:
            json.dump(person_dict, f, indent=2)
        f.close()
        self.ids.i.text = ""
        self.ids.a.text = ""
        self.ids.b.text = ""
        self.ids.c.text = ""
        self.ids.d.text = ""

class PreviewQWindow(Screen):
    minn_height = NumericProperty(0)
    def img_show(self):
        mini_height = 0
        with open('cache.json', 'r') as f:
            img_list = json.load(f)
            for img in img_list:
                self.r = Image(source=img,size_hint = (1,None),height = 550, allow_stretch=True)
                self.ids.image_layout.canvas.add(Color(1, 1, 1))
                self.ids.image_layout.canvas.add(Rectangle(size=self.size,pos = self.pos))
                self.ids.image_layout.add_widget(self.r)
                mini_height +=550
        self.minn_height = mini_height
        clear = {}
        with open('cache.json','w') as f:
            json.dump(clear,f)

class PreviewAWindow(Screen):
    pass

class NewSetWindow(Screen):
    def set_tbl_save(self):
        self.store = JsonStore('cache.json')
        set_name = self.ids.name_set.text
        num_item = int(self.ids.num_item.text)
        self.store.put('setname', set_name=set_name)
        self.store.put('setquan', item_quantity=num_item)
        con = sqlite3.connect("exam_db.db")
        c = con.cursor()
        # Create to Set Table -----------
        c.execute(
            "create table if not exists set_tbl([set_ID] integer primary key ,set_name text,set_quantity integer)")
        # Insert to Set Table -----------
        c.execute("insert into set_tbl(set_name,set_quantity) VALUES(?,?)",(set_name,num_item))
        c.close()
        con.commit()
        con.close()

class AnswerKeyWindow(Screen):
    aw = {}
    check = []
    min_height = NumericProperty(0)
    def load(self):
        mini_height = 0
        self.store = JsonStore('cache.json')
        self.item_num = self.store.get('setquan')['item_quantity']
        print(self.item_num)

        for i in range(self.item_num):
            self.b = Label(text=f'{i+1}.', color=(0, 0, 0, 1),size_hint=(.2, None),height=60)
            self.l = CheckBox(group=f'answer{i}', size_hint=(.2, None),height=60, color=(0, 0, 0, 1), active=False)
            self.o = CheckBox(group=f'answer{i}', size_hint=(.2, None),height=60, color=(0, 0, 0, 1), active=False)
            self.w = CheckBox(group=f'answer{i}', size_hint=(.2, None),height=60, color=(0, 0, 0, 1), active=False)
            self.n = CheckBox(group=f'answer{i}', size_hint=(.2, None),height=60, color=(0, 0, 0, 1), active=False)

            self.ids.num_bub.add_widget(self.b)
            self.ids.num_bub.add_widget(self.l)
            self.ids.num_bub.add_widget(self.o)
            self.ids.num_bub.add_widget(self.w)
            self.ids.num_bub.add_widget(self.n)

            self.l.bind(active=self.on_check_Active_A)
            self.o.bind(active=self.on_check_Active_B)
            self.w.bind(active=self.on_check_Active_C)
            self.n.bind(active=self.on_check_Active_D)
            mini_height += 60
        self.min_height = mini_height

    def on_check_Active_A(self, checkboxInstance, isActive):
        if isActive:
            AnswerKeyWindow.check.append("a")
            print(AnswerKeyWindow.check)
        else:
            AnswerKeyWindow.check.remove('a')

    def on_check_Active_B(self, checkboxInstance, isActive):
        if isActive:
            AnswerKeyWindow.check.append("b")
            print(AnswerKeyWindow.check)
        else:
            AnswerKeyWindow.check.remove('b')

    def on_check_Active_C(self, checkboxInstance, isActive):
        if isActive:
            AnswerKeyWindow.check.append("c")
            print(AnswerKeyWindow.check)
        else:
            AnswerKeyWindow.check.remove('c')

    def on_check_Active_D(self, checkboxInstance, isActive):
        if isActive:
            AnswerKeyWindow.check.append("d")
            print(AnswerKeyWindow.check)
        else:
            AnswerKeyWindow.check.remove('d')


    def d2l(self):

        counter = 0
        for i in AnswerKeyWindow.check:
            if i == "a":
                AnswerKeyWindow.aw[counter] = AnswerKeyWindow.aw.setdefault(counter, 0)
            if i == "b":
                AnswerKeyWindow.aw[counter] = AnswerKeyWindow.aw.setdefault(counter, 1)
            if i == "c":
                AnswerKeyWindow.aw[counter] = AnswerKeyWindow.aw.setdefault(counter, 2)
            if i == "d":
                AnswerKeyWindow.aw[counter] = AnswerKeyWindow.aw.setdefault(counter, 3)
            counter += 1

        key = AnswerKeyWindow.check

        if len(key) != 75:
            for i in range(len(key), 75):
                key.append(f"NULL")

        print(key)
        con = sqlite3.connect("exam_db.db")
        c = con.cursor()
        # Create to Key Table -----------
        c.execute(
            "create table if not exists key_tbl([key_ID] integer primary key ,[1] text,[2] text, [3] text, [4] text, [5] text, [6] text, [7] text,[8] text,[9] text,[10] text,[11] text,[12] text,[13] text,[14] text,[15] text,[16] text,[17] text,[18] text,[19] text,[20] text,[21] text,[22] text,[23] text,[24] text,[25] text,[26] text,[27] text, [28] text, [29] text, [30] text, [31] text, [32] text,[33] text,[34] text,[35] text,[36] text,[37] text,[38] text,[39] text,[40] text,[41] text,[42] text,[43] text,[44] text,[45] text,[46] text,[47] text,[48] text,[49] text,[50] text,[51] text,[52] text, [53] text, [54] text, [55] text, [56] text, [57] text,[58] text,[59] text,[60] text,[61] text,[62] text,[63] text,[64] text,[65] text,[66] text,[67] text,[68] text,[69] text,[70] text,[71] text,[72] text,[73] text,[74] text,[75] text)")
        # Inset to Key Table -------------
        c.execute(
            "insert into key_tbl('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75') VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            key)
        c.close()
        con.commit()
        con.close()


class StudentWindow(Screen):
    def btn(self):
        pops = MyPopUp()
        pops.open()

class CameraClick(Popup):
    def save_ans(self):
        ANSWER_KEY = {}
        show_set_name = []
        mini_height = 0
        con = sqlite3.connect("exam_db.db")
        c = con.cursor()
        # Create to Set Table -----------
        for row in c.execute("select * from key_tbl"):
            show_set_name = row
        c.close()
        con.commit()
        con.close()

        counter = 0
        for i in show_set_name:
            if isinstance(i, int):
                continue
            if i == "a":
                ANSWER_KEY[counter] = ANSWER_KEY.setdefault(counter, 0)
            if i == "b":
                ANSWER_KEY[counter] = ANSWER_KEY.setdefault(counter, 1)
            if i == "c":
                ANSWER_KEY[counter] = ANSWER_KEY.setdefault(counter, 2)
            if i == "d":
                ANSWER_KEY[counter] = ANSWER_KEY.setdefault(counter, 3)
            counter += 1

        print(ANSWER_KEY)

        correct = 0
        counter = 0
        answer_input = []
        image = cv2.imread('img/OMR_10_23_25items_withlight_celis.jpg')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)
        # find contours in the edge map, then initialize
        # the contour that corresponds to the document
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        docCnt = None
        # ensure that at least one contour was found
        if len(cnts) > 0:
            # sort the contours according to their size in
            # descending order
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
            # loop over the sorted contours
            for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                # if our approximated contour has four points,
                # then we can assume we have found the paper
                if len(approx) == 4:
                    docCnt = approx
                    break

        # apply a four point perspective transform to both the
        # original image and grayscale image to obtain a top-down
        # birds eye view of the paper
        paper = four_point_transform(image, docCnt.reshape(4, 2))
        warped = four_point_transform(gray, docCnt.reshape(4, 2))
        warped = cv2.resize(warped, (2048, 1536), interpolation=cv2.INTER_AREA)
        width = image.shape[0]
        height = image.shape[1]
        print('height:' + str(height) + 'width:' + str(width))
        blur = cv2.GaussianBlur(warped, (3, 3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 40))
        dilate = cv2.dilate(thresh, kernel, iterations=1)

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

        aw = []
        bw = []
        cw = []
        dw = []
        cont_list = []
        let = ['a', 'b', 'c']
        h = 0
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            if h > 100 and w > 100:
                # if h <0 and w <0:
                cv2.rectangle(paper, (x, y), (x + (w), y + h), (36, 255, 12), 2)
                print(f'x' + str(x) + 'y' + str(y) + 'w' + str(w) + 'h' + str(h))
                aw.append(x)
                bw.append(y)
                cw.append(w)
                dw.append(h)
        print(len(ANSWER_KEY))
        if len(ANSWER_KEY) > 0:
            a = 36
            b = 24
            c = 300
            d = 1300
            num25 = paper[b:b + d, a:a + c]
            num25 = cv2.cvtColor(num25, cv2.COLOR_BGR2GRAY)

            thresh = cv2.threshold(num25, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            # find contours in the thresholded image, then initialize
            # the list of contours that correspond to questions
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            questionCnts = []
            # loop over the contours
            for c in cnts:
                # compute the bounding box of the contour, then use the
                # bounding box to derive the aspect ratio
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)
                # in order to label the contour as a question, region
                # should be sufficiently wide, sufficiently tall, and
                # have an aspect ratio approximately equal to 1
                if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                    questionCnts.append(c)
            # sort the question contours top-to-bottom, then initialize
            # the total number of correct answers
            questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
            print(len(questionCnts))

            # each question has 5 possible answers, to loop over the
            # question in batches of 5
            for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
                # sort the contours for the current question from
                # left to right, then initialize the index of the
                # bubbled answer
                cnts = contours.sort_contours(questionCnts[i:i + 4])[0]
                bubbled = None
                # loop over the sorted contours
                for (j, c) in enumerate(cnts):
                    # construct a mask that reveals only the current
                    # "bubble" for the question
                    mask = np.zeros(thresh.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    # apply the mask to the thresholded image, then
                    # count the number of non-zero pixels in the
                    # bubble area
                    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                    total = cv2.countNonZero(mask)
                    # if the current total has a larger number of total
                    # non-zero pixels, then we are examining the currently
                    # bubbled-in answer
                    if bubbled is None or total > bubbled[0]:
                        bubbled = (total, j)

                # initialize the contour color and the index of the
                # *correct* answer
                color = (0, 0, 255)
                k = ANSWER_KEY[counter]
                answer_input.append(bubbled[1])
                # check to see if the bubbled answer is correct
                if k == bubbled[1]:
                    color = (0, 255, 0)
                    correct += 1
                print(counter)
                counter += 1

        if len(ANSWER_KEY) > 25:
            a = 390
            b = 24
            c = 300
            d = 1300
            num50 = paper[b:b + d, a:a + c]

            num50 = cv2.cvtColor(num50, cv2.COLOR_BGR2GRAY)

            thresh = cv2.threshold(num50, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            # find contours in the thresholded image, then initialize
            # the list of contours that correspond to questions
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            questionCnts = []
            # loop over the contours
            for c in cnts:
                # compute the bounding box of the contour, then use the
                # bounding box to derive the aspect ratio
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)
                # in order to label the contour as a question, region
                # should be sufficiently wide, sufficiently tall, and
                # have an aspect ratio approximately equal to 1
                if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                    questionCnts.append(c)
            # sort the question contours top-to-bottom, then initialize
            # the total number of correct answers
            questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
            # each question has 5 possible answers, to loop over the
            # question in batches of 5

            for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
                # sort the contours for the current question from
                # left to right, then initialize the index of the
                # bubbled answer
                cnts = contours.sort_contours(questionCnts[i:i + 4])[0]
                bubbled = None
                # loop over the sorted contours
                for (j, c) in enumerate(cnts):
                    # construct a mask that reveals only the current
                    # "bubble" for the question
                    mask = np.zeros(thresh.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    # apply the mask to the thresholded image, then
                    # count the number of non-zero pixels in the
                    # bubble area
                    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                    total = cv2.countNonZero(mask)
                    # if the current total has a larger number of total
                    # non-zero pixels, then we are examining the currently
                    # bubbled-in answer
                    if bubbled is None or total > bubbled[0]:
                        bubbled = (total, j)

                # initialize the contour color and the index of the
                # *correct* answer
                color = (0, 0, 255)
                n = ANSWER_KEY[counter]
                print(counter)
                answer_input.append(bubbled[1])
                # check to see if the bubbled answer is correct
                if n == bubbled[1]:
                    color = (0, 255, 0)
                    correct += 1

                counter += 1

        if len(ANSWER_KEY) > 50:
            a = 750
            b = 24
            c = 300
            d = 1300
            num75 = paper[b:b + d, a:a + c]

            num75 = cv2.cvtColor(num75, cv2.COLOR_BGR2GRAY)

            thresh = cv2.threshold(num75, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            # find contours in the thresholded image, then initialize
            # the list of contours that correspond to questions
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            questionCnts = []
            # loop over the contours
            for c in cnts:
                # compute the bounding box of the contour, then use the
                # bounding box to derive the aspect ratio
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)
                # in order to label the contour as a question, region
                # should be sufficiently wide, sufficiently tall, and
                # have an aspect ratio approximately equal to 1
                if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                    questionCnts.append(c)
            # sort the question contours top-to-bottom, then initialize
            # the total number of correct answers
            questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
            # each question has 5 possible answers, to loop over the
            # question in batches of 5

            for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
                # sort the contours for the current question from
                # left to right, then initialize the index of the
                # bubbled answer
                cnts = contours.sort_contours(questionCnts[i:i + 4])[0]
                bubbled = None
                # loop over the sorted contours
                for (j, c) in enumerate(cnts):
                    # construct a mask that reveals only the current
                    # "bubble" for the question
                    mask = np.zeros(thresh.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    # apply the mask to the thresholded image, then
                    # count the number of non-zero pixels in the
                    # bubble area
                    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                    total = cv2.countNonZero(mask)
                    # if the current total has a larger number of total
                    # non-zero pixels, then we are examining the currently
                    # bubbled-in answer
                    if bubbled is None or total > bubbled[0]:
                        bubbled = (total, j)

                # initialize the contour color and the index of the
                # *correct* answer
                color = (0, 0, 255)
                n = ANSWER_KEY[counter]
                answer_input.append(bubbled[1])
                # check to see if the bubbled answer is correct
                if n == bubbled[1]:
                    color = (0, 255, 0)
                    correct += 1
                counter += 1

        print(answer_input)
        key = answer_input

        if len(key) != 75:
            for i in range(len(key), 75):
                key.append(f"NULL")

        print(key)
        con = sqlite3.connect("exam_db.db")
        c = con.cursor()
        # Create to Key Table -----------
        c.execute(
            "create table if not exists stud_ans_tbl([key_ID] integer primary key ,[1] text,[2] text, [3] text, [4] text, [5] text, [6] text, [7] text,[8] text,[9] text,[10] text,[11] text,[12] text,[13] text,[14] text,[15] text,[16] text,[17] text,[18] text,[19] text,[20] text,[21] text,[22] text,[23] text,[24] text,[25] text,[26] text,[27] text, [28] text, [29] text, [30] text, [31] text, [32] text,[33] text,[34] text,[35] text,[36] text,[37] text,[38] text,[39] text,[40] text,[41] text,[42] text,[43] text,[44] text,[45] text,[46] text,[47] text,[48] text,[49] text,[50] text,[51] text,[52] text, [53] text, [54] text, [55] text, [56] text, [57] text,[58] text,[59] text,[60] text,[61] text,[62] text,[63] text,[64] text,[65] text,[66] text,[67] text,[68] text,[69] text,[70] text,[71] text,[72] text,[73] text,[74] text,[75] text)")
        # Inset to Key Table -------------
        c.execute(
            "insert into stud_ans_tbl('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75') VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            key)
        c.close()
        con.commit()
        con.close()
        print('counter:' + str(counter))
        print('correct:' + str(correct))
        score = (correct / counter) * 100
        print('score' + str(score))
        self.store = JsonStore('cache.json')
        student_name = self.store.get('std')['student_name']

        con = sqlite3.connect("exam_db.db")
        c = con.cursor()
        # Create to Set Table -----------
        c.execute(
            "create table if not exists student_score_tbl([student_ID] integer primary key ,student_name text,score integer)")
        # Insert to Set Table -----------
        c.execute("insert into student_score_tbl(student_name,score) VALUES(?,?)", (student_name, score))
        c.close()
        con.commit()
        con.close()


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("bubble.kv")

class IMark(App):
    def build(self):
        Window.size = (400, 700)
        Window.clearcolor = (1, 1, 1, 1)
        self.size = Window.size
        self.editing_pump = ''
        return kv


if __name__ == "__main__":
    IMark().run()
