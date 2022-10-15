import kivy
from functools import *
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
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
import uuid
import cpdf


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
        print(teacher_name)
        print(subject_name)
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

    pass


class QuestionnaireWindow(Screen):
    count = 1
    enable_btn = BooleanProperty(False)
    min_height = NumericProperty(0)
    def __init__(self, **kwargs):
        super(QuestionnaireWindow, self).__init__(**kwargs)
        self.store = JsonStore('cache.json')

    def load_items(self):
        mini_height = 0
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
        self.min_height = mini_height +51
        self.enable_btn = True

    def edit_question(self, question, *args):
        self.store.put('cache', editing_que = question)
        self.manager.transition.direction = 'left'
        self.manager.current = 'input_questionnaire'

    def createPdf(self):
        cpdf.create()


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
            print(person_dict)
        with open('new_ques.json', 'w') as f:
            json.dump(person_dict, f, indent=2)
        f.close()
        self.ids.i.text = ""
        self.ids.a.text = ""
        self.ids.b.text = ""
        self.ids.c.text = ""
        self.ids.d.text = ""



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
