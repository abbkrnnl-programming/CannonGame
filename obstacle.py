from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.metrics import dp, Metrics
from bullet import Bullet

import constants

class Obstacle(Widget):
    def __init__(self, **kwargs):
        super(Obstacle, self).__init__(**kwargs)
        self.size = dp(constants.obstacleSize), dp(constants.obstacleSize)
        self.pos = (constants.lineStart, constants.lineStart)
        self.image = Image(source='./sprites/stone4.jpeg', size=self.size, pos=self.pos)
        self.iron = 0

    def CollisionDetection(self, bullet, bomb):
        # check for collision
        if self.collide_widget(bullet) or self.collide_widget(bomb):
            return True
