import math

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

from obstacle import Obstacle
from bullet import Bullet
from tank import Tank
from bomb import Bomb
from laser import Laser
from enemy import Enemy
from mirror import Mirror
from endgame import EndGame
from hallOfFame import HallOfFame
from help import Help
from menu import Menu
from CannonGame import CannonGame
from MyScreenManager import MyScreenManager

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Set the screen size
Config.set('graphics', 'width', SCREEN_WIDTH)
Config.set('graphics', 'height', SCREEN_HEIGHT)
Config.write()

# Register custom font
LabelBase.register(name='PixelifySans',
                   fn_regular='./Pixelify_Sans/PixelifySans-VariableFont_wght.ttf')




class CannonApp(App):
  def build(self):
    self.sm = MyScreenManager()
    Window.bind(on_key_down=self.on_key_down)
    return self.sm

  def dp(self, value):
    return dp(value)

  def on_key_down(self, window, key, scancode, codepoint, modifier):
    if key == 98:  # 'b' key has the key code 98
      if self.sm.current != 'menu':  # Only go back if not already on the menu
        self.sm.transition.direction = 'right'
        self.sm.current = 'menu'

  # def on_key_down(self, window, key, scancode, codepoint, modifier):
  #   if key == 98:
  #     print(1)
  #     if self.sm.current != 'menu':  # Only go back if not already on the menu
  #       self.sm.transition.direction = 'right'
  #       self.sm.current = 'menu'

if __name__ == '__main__':
  CannonApp().run()