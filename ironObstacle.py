from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.metrics import dp, Metrics
from kivy.properties import StringProperty, NumericProperty, Clock, ObjectProperty
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.core.text import LabelBase
from kivy.uix.label import Label

class IronObstacle(Widget):
    def __init__(self, **kwargs):
        super(IronObstacle, self).__init__(**kwargs)
        self.size = dp(20), dp(20)
        self.pos = (0,0)
        # self.image = Image(source='./sprites/steel2.webp', size=self.size, pos = self.pos)
        self.image = Image(source='./sprites/steel.jpeg', size=self.size, pos=self.pos)
        self.id = 0

    def CollisionDetection(self, bullet, bomb):
        #check for collision
        if self.collide_widget(bullet) or self.collide_widget(bomb):
            return True