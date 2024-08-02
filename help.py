from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.core.text import LabelBase
from kivy.uix.label import Label


LabelBase.register(name='PixelifySans',
                   fn_regular='./Pixelify_Sans/PixelifySans-VariableFont_wght.ttf')

class Help(Screen):
    def __init__(self, **kwargs):
        super(Help, self).__init__(**kwargs)
