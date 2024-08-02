import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, Clock, ObjectProperty
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse
from kivy.graphics.context_instructions import Color
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

import constants


class Bomb(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_velocity = constants.bombSpeed
        self.time = 0.0
        self.velocity = 0.0
        self.distance = 0.0
        self.distanceX = 0.0
        self.distanceY = 0.0
        self.velocityX = 0.0
        self.velocityY = 0.0
        self.start = 0
        self.radius = constants.bombRadius
        self.exploded = False # tracks explosion of bomb
        self.tick = 0 # tracks time went from explosion of bomb
        self.cur_color = 0
        self.color = [0, 0, 0, 1]
        with self.canvas:
            Color(rgba=[1, 1, 1, 1])
            self.explosion = Ellipse(pos=(0, constants.endPos), size=(dp(2*constants.bombRadius), dp(2*constants.bombRadius)))

    def move(self):
        # movement of bomb on canvas
        if self.start:
            x, y = self.pos
            x = constants.startX + self.velocityX*self.time
            y = constants.startY + self.velocityY*self.time - 4.9*self.time**2
            self.pos = dp(x), dp(y)

    def set(self, tx, ty):
        # setting velocity and state of bomb on touch pos
        self.distanceX = constants.startX - tx
        self.distanceY = constants.startY - ty
        self.distance = math.sqrt(self.distanceX ** 2 + self.distanceY ** 2)
        self.velocity = self.distance / constants.maxDistance
        self.velocity *= self.max_velocity
        self.velocityX = self.velocity * (self.distanceX / self.distance)
        self.velocityY = self.velocity * (self.distanceY / self.distance)
        self.time = 0
        self.start = 1
        self.exploded = False
        self.tick = 0
        self.explosion.pos = (0, constants.endPos)

    def reset(self):
        # setting starting characteristics of bomb
        self.velocity = 0.0
        self.time = 0.0
        self.distanceX = 0.0
        self.distanceY = 0.0
        self.pos = dp(constants.startBombX), dp(constants.startBombY)
        self.start = 0
        self.exploded = False
        self.tick = 0
        self.cur_color = 0
        self.color = [0, 0, 0, 1]
        self.explosion.pos = (0, constants.endPos)