from kivy.uix.image import Image
from kivy.metrics import dp, Metrics

import constants

class Enemy():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = Image(source='sprites/enemy.png', pos=(dp(constants.enemyX), dp(constants.enemyY)), size = (dp(constants.bulletRadius), dp(constants.bulletRadius)))
        self.health = 5
        self.healthImage = Image(source='sprites/full.jpg', pos = (dp(constants.enemyX+5), dp(constants.enemyY-10)), size = (constants.healthWidth, constants.healthHeight))

    def damage(self, damage):
        # change of images depending on health of monster
        self.health = max(0, self.health-damage)
        if self.health == 4:
            self.healthImage.source = 'sprites/80.jpg'
        elif self.health == 3:
            self.healthImage.source = 'sprites/60.jpg'
        elif self.health == 2:
            self.healthImage.source = 'sprites/40.png'
        elif self.health == 1:
            self.healthImage.source = 'sprites/20.png'
        elif self.health == 0:
            self.healthImage.source = 'sprites/0.png'
        else:
            self.healthImage.source = 'sprites/full.jpg'