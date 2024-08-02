from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, Clock, ObjectProperty
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
import math
import constants

class Bullet(Widget):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.max_velocity = constants.bulletSpeed
    self.time = 0.0
    self.velocity = 0.0
    self.distance = 0.0
    self.distanceX = 0.0
    self.distanceY = 0.0
    self.velocityX = 0.0
    self.velocityY = 0.0
    self.start = 0
    self.radius = constants.bulletRadius

  def move(self):
    #movement of bullet on canvas
    if(self.start):
      x, y = self.pos
      x = constants.startX + self.velocityX*self.time
      y = constants.startY + self.velocityY*self.time-4.9*self.time**2
      self.pos = dp(x), dp(y)

  def set(self, tx, ty):
    # setting velocity and state of bullet depending on touch pos
    self.distanceX = constants.startX - tx
    self.distanceY = constants.startY - ty
    self.distance = math.sqrt(self.distanceX ** 2 + self.distanceY ** 2)
    self.velocity = self.distance / constants.maxDistance
    self.velocity *= self.max_velocity
    self.velocityX = self.velocity * (self.distanceX / self.distance)
    self.velocityY = self.velocity * (self.distanceY / self.distance)
    self.time = 0
    self.start = 1

  def reset(self):
    # setting state of bullet to starting state
    self.velocity = 0.0
    self.time = 0.0
    self.distanceX = 0.0
    self.distanceY = 0.0
    self.pos = dp(constants.startX), dp(constants.startY)
    self.start = 0
