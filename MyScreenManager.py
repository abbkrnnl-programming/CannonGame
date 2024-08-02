from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase

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


class MyScreenManager(ScreenManager):
  def __init__(self, **kwargs):
    super(MyScreenManager, self).__init__(**kwargs)
  def update_records(self):
    # Update of Hall of Fame
    hallOfFame = self.get_screen('records')
    hallOfFame.records_update()