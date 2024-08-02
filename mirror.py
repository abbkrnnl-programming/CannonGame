
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.metrics import dp, Metrics

import constants

class Mirror(Widget):
    def __init__(self, **kwargs):
        super(Mirror, self).__init__(**kwargs)
        self.size = dp(constants.bombRadius), dp(constants.obstacleIronSize)
        self.pos = dp(constants.mirrorWidth), dp(constants.mirrorHeight)
        self.image = Image(source='./sprites/mirror.png', size=self.size, pos=self.pos)
        self.id = 0