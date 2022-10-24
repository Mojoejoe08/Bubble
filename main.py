import kivy
from functools import *
import json
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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



class scrollerPage(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open('new_ques.json') as f:
            queees = json.load(f)
        f.close()
        self.data = [{"text": str(x)} for x in queees]


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
    pass

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
    enable_btn = BooleanProperty(False)
    min_height = NumericProperty(0)
    def __init__(self, **kwargs):
        super(QuestionnaireWindow, self).__init__(**kwargs)
        self.store = JsonStore('cache.json')

    def load_items(self):
        mini_height = 0
        self.ids.main_load.remove_widget(self.ids.load_items)
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
        self.enable_btn = True

    def edit_question(self, question, *args):
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
        self.ids.preview_img.remove_widget(self.ids.load)
        clear = {}
        with open('cache.json','w') as f:
            json.dump(clear,f)

class PreviewAWindow(Screen):
    pass

class NewSetWindow(Screen):
    def get_name_set(self,value):
        self.name_set = value
        print(self.name_set)

    def spinner_clicked(self, value):
        self.num_item =  value
        print(self.num_item)

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
