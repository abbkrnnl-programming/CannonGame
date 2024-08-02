from kivy.uix.image import Image
from kivy.metrics import dp, Metrics
from kivy.uix.screenmanager import ScreenManager, Screen

import constants

class Menu(Screen):
  def __init__(self, **kwargs):
    super(Menu, self).__init__(**kwargs)
    with self.canvas:
      self.background = Image(source='sprites/gback1.png')
      self.background.size = dp(constants.backX), dp(constants.backY)
      self.background.pos = (0, dp(constants.lineStart))