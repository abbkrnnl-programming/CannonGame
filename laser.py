from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse
from kivy.graphics.context_instructions import Color

import constants


class Laser(Widget):
    def __init__(self, **kwargs):
        super(Laser, self).__init__(**kwargs)
        self.points = [dp(constants.lineX), dp(constants.lineY), dp(constants.lineX), dp(constants.lineY)]
        self.width = dp(constants.lineWidth)
        self.time = 0
        self.diffY = 0.0
        self.diifX = 0.0
        self.k = 0.0
        self.b = 0.0
        self.start = 0
        self.damaged = 0
        self.change = 0
        self.cnt = 0
        with self.canvas:
            Color(rgba = [1, 0, 0, 1])
            self.line = Line(points = self.points, width = self.width)

    def set(self, x, y):
        # setting laser points based on user touch and indicating if laser touches the mirror
        self.change = 0
        self.cnt = 0
        self.start = 1
        self.line.width = dp(constants.lineWidth)
        self.width = dp(constants.lineWidth)
        self.diffX = constants.lineX - x
        self.diffY = constants.lineY - y
        self.k = self.diffY / self.diffX
        self.b = constants.lineY - constants.lineX * self.k
        if (constants.mirrorHeight-self.b)/self.k >= constants.mirrorWidth and (constants.mirrorHeight-self.b)/self.k <= constants.screenHeight:
            self.points = [dp(constants.lineX), dp(constants.lineY), dp((constants.mirrorHeight-self.b)/self.k), dp(constants.mirrorHeight)]
            self.change = 1
        elif self.k * constants.screenWidth + self.b <= constants.screenHeight:
            self.points = [dp(constants.lineX), dp(constants.lineY), dp(constants.screenWidth), dp(self.k * constants.screenWidth + self.b)]
        else:
            self.points = [dp(constants.lineX), dp(constants.lineY), dp((constants.screenHeight-self.b)/self.k), dp(constants.screenHeight)]
        self.line.points = self.points
        self.damaged = 0

    def ricochet(self):
        # making laser go ricochet
        self.start = 1
        self.line.width = dp(constants.lineWidth)
        self.width = dp(constants.lineWidth)
        endY = constants.mirrorHeight
        endX = (endY-self.b)/self.k
        startY = (endY-constants.lineY) + endY
        startX = constants.lineX
        self.diffX = endX - startX
        self.diffY = endY - startY
        self.k = self.diffY / self.diffX
        self.b = startY - constants.lineX * self.k
        self.points = [dp(endX), dp(endY), dp((0-self.b)/self.k), 0]
        self.line.points = self.points


    def reset(self):
        #reset of laser position and state
        self.change = 0
        self.cnt = 0
        self.start = 0
        self.points = [dp(constants.lineX), dp(constants.lineY), dp(constants.lineX), dp(constants.lineY)]
        self.line.points = self.points
        self.line.width = dp(constants.lineWidth)
        self.width = dp(constants.lineWidth)

    def line_intersects(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # check for intersection of laser with other obstacles
        # Calculate the direction of the lines
        d1 = (x2 - x1, y2 - y1)
        d2 = (x4 - x3, y4 - y3)
        # Solve for intersection
        denominator = d1[0] * d2[1] - d1[1] * d2[0]
        if denominator == 0:
            return False  # Lines are parallel
        t = ((x3 - x1) * d2[1] - (y3 - y1) * d2[0]) / denominator
        u = ((x3 - x1) * d1[1] - (y3 - y1) * d1[0]) / denominator

        return 0 <= t <= 1 and 0 <= u <= 1