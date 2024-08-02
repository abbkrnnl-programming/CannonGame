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
from ironObstacle import IronObstacle
from mirror import Mirror
from endgame import EndGame
from hallOfFame import HallOfFame
from help import Help
from menu import Menu

import constants
import math

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

class CannonGame(Screen):
  end_screen = ObjectProperty() # end screen appears on gameOver = True state


  def __init__(self, **kwargs):
    super(CannonGame, self).__init__(**kwargs)
    self.obstacles = []
    self.iron_obstacles = []
    self.score = 100
    self.gameOver= False
    self.projectile = 1 # Default projectile type (bullet)
    self.record_init()

    # canvas elements init
    with self.canvas:
      self.background = Image(source='sprites/gback1.png')
      self.background.size = dp(constants.backX), dp(constants.backY)
      self.background.pos = (0, dp(constants.lineStart))
      self.enemy = Enemy()
      self.obstacle_init()
      self.clock = Clock.schedule_interval(self.update, 1/20)
      self.mirror = Mirror()
    with self.canvas.after:
      self.bullet = Bullet(pos=(dp(constants.startX), dp(constants.startY)))
      self.bomb = Bomb(pos=(0, constants.endPos))
      self.laser = Laser()
      self.laser.line.points = [constants.lineStart, constants.lineStart, constants.lineEnd, constants.lineEnd]
      self.tank = Tank()
      self.score_label_back = Label(text=f"Score: {self.score}", font_size='32sp',
                                    pos=(dp(constants.scoreX+2), dp(constants.scoreY-2)), font_name='PixelifySans', color=(0, 0, 0, 1))
      self.score_label = Label(text=f"Score: {self.score}", font_size='32sp',
                               pos=(dp(constants.scoreX), dp(constants.scoreY)), font_name='PixelifySans')


  def record_init(self):
    # Read records from file for future updates
    self.file = open('./records.txt', 'r+')
    self.record = []
    for line in self.file:
      if(len(line) > 2):
        line = line[:-1]
      line = int(line)
      self.record.append(line)
    self.file.close()

  def record_update(self):
    # Update records with the current score
    self.record.append(self.score)
    self.record.sort(reverse=True)
    if len(self.record) > 10:
      del self.record[-1]
    self.file = open('./records.txt', 'r+')
    for rec in self.record:
      self.file.write(str(rec)+'\n')
    self.file.close()
    self.manager.update_records()

  def obstacle_init(self):
    # Initialize obstacles
    with self.canvas.before:
      startY = 120
      for i in range(5):
        for j in range(15):
          size = constants.obstacleSize
          obstacle = Obstacle()
          startX = 600
          obstacle.pos = dp(startX + i * size), dp(startY + j * size)
          obstacle.image.pos = dp(startX + i * size), dp(startY + j * size)
          self.obstacles.append(obstacle)
      size = constants.obstacleIronSize
      for i in range(2):
        for j in range(30):
          obstacle = Obstacle()
          obstacle.size = dp(size), dp(size)
          startX = 560
          obstacle.pos = dp(startX + i * size), dp(startY + j * size)
          obstacle.image = Image(source='./sprites/steel.jpeg', size=obstacle.size, pos=obstacle.pos)
          obstacle.iron = 1
          self.obstacles.append(obstacle)
      for i in range(1):
        for j in range(30):
          obstacle = Obstacle()
          obstacle.size = dp(size), dp(size)
          startX = 800
          obstacle.pos = dp(startX + i * size), dp(startY + j * size)
          obstacle.image = Image(source='./sprites/steel.jpeg', size=obstacle.size, pos=obstacle.pos)
          obstacle.iron = 1
          self.obstacles.append(obstacle)

  def SetBullet(self):
    # Set projectile type to bullet
    self.projectile = 1
    self.bullet.pos = dp(constants.startX), dp(constants.startY)
    self.bomb.pos = 0, constants.endPos
    self.laser.reset()
    self.laser.line.points = [constants.lineStart, constants.lineStart, constants.lineEnd, constants.lineEnd]

  def SetBomb(self):
    # Set projectile type to bomb
    self.projectile = 2
    self.bullet.pos = 0, constants.endPos
    self.bomb.pos = dp(constants.startBombX), dp(constants.startBombY)
    self.laser.line.points = [constants.lineStart, constants.lineStart, constants.lineEnd, constants.lineEnd]


  def SetLaser(self):
    # Set projectile type to laser
    self.projectile = 3
    self.bullet.pos = 0, constants.endPos
    self.bomb.pos = 0, constants.endPos
    self.laser.line.points = self.laser.points

  def ResetGame(self):
    # Reset the game to initial state
    removed_obstacle = []
    for obstacle in self.obstacles:
      removed_obstacle.append(obstacle)
    for obstacle in removed_obstacle:
      obstacle.pos = 0, constants.delPos
      obstacle.image.pos = 0, constants.delPos
    self.obstacle_init()
    self.SetBullet()
    self.clock.cancel()
    self.enemy.health = 5
    self.enemy.damage(0)
    self.score = 100
    self.score_label.text = f"Score: {self.score}"
    self.score_label_back.text = f"Score: {self.score}"
    self.gameOver = False
    self.end_screen.opacity = 0

  def update(self, dt):
    # Update the game state
    if not self.gameOver:
      # movement of projectile
      self.bullet.time += dt
      if self.projectile == 1:
        self.bullet.move()
      elif self.projectile == 2:
        self.bomb.time += dt
        self.bomb.move()
      else:
        if self.laser.width <= 1:
          self.laser.reset()
        else:
          self.laser.width -= 1
          self.laser.line.width = self.laser.width


      x, y = self.bullet.pos
      if self.projectile == 2:
        x, y = self.bomb.pos
      if self.bomb.exploded:
        # change of bomb color (tick effect) and explosion of bomb
        if self.bomb.cur_color == 0:
          self.bomb.cur_color = 1
          self.bomb.color = [1, 1, 1, 1]
        else:
          self.bomb.cur_color = 0
          self.bomb.color = [0, 0, 0, 1]
        self.bomb.tick += dt
        if self.bomb.tick >= 1.0:
          self.obstacles_remove(x, y)
          self.bomb.explosion.pos = 0, constants.endPos
          self.bomb.reset()
        if self.bomb.tick + dt >= 1.0:
          self.bomb.explosion.pos = x-dp(self.bomb.radius), y-dp(self.bomb.radius)
      if(x > dp(SCREEN_WIDTH) or y < 0 or y > dp(SCREEN_HEIGHT)):
        if self.projectile == 1:
          self.bullet.reset()
        elif self.projectile == 2 and self.bomb.exploded is False:
          self.bomb.reset()

      # checking for collision with monster and mirror
      if self.bullet.collide_widget(self.enemy.image):
        self.obstacles_remove(x, y)
        self.bullet.reset()
        self.enemy.damage(2)
      if self.bomb.collide_widget(self.enemy.image) and self.bomb.exploded is False:
        self.bomb.exploded = True

      if self.bullet.collide_widget(self.mirror.image):
        self.bullet.reset()
      if self.bomb.collide_widget(self.mirror.image) and self.bomb.exploded is False:
        self.bomb.exploded = True

      # check for collision with obstacles
      removed_obstacle = []
      for obstacle in self.obstacles:
        if obstacle.CollisionDetection(self.bullet, self.bomb):
          if self.projectile == 2 and self.bomb.exploded is False:
            self.bomb.exploded = True
          elif self.projectile == 1 and obstacle.iron == 1:
            self.bullet.reset()
          elif self.projectile == 1:
            self.obstacles_remove(x, y)
            self.bullet.reset()

        if self.projectile == 3:
          size = obstacle.size[0]
          x1, y1 = obstacle.pos
          if self.laser_intersection(x1, y1, size):
            removed_obstacle.append(obstacle)
      for obstacle in removed_obstacle:
        obstacle.pos = 0, constants.delPos
        obstacle.image.pos = 0, constants.delPos

      # check for collision of laser with enemy
      if self.projectile == 3:
        size = self.enemy.image.size[0]
        x1, y1 = self.enemy.image.pos
        if self.laser_intersection(x1, y1, size) and self.laser.damaged == 0:
          if self.laser.change == 0:
            self.enemy.damage(2)
          else:
            self.enemy.damage(3)
          self.laser.damaged = 1

        if self.laser.change == 1:
          self.laser.cnt += 1
        if self.laser.change == 1 and self.laser.cnt == 1:
          self.laser.ricochet()
          self.score += 1
          self.score_label.text = f"Score: {self.score}"
          self.score_label_back.text = f"Score: {self.score}"

    if self.enemy.health <= 0 and self.gameOver == False:
      # end screen appearence
      self.gameOver = True
      self.record_update()
      if self.gameOver:
        self.end_screen.opacity = 1
      self.SetBullet()

  def laser_intersection(self, x, y, size):
    x1, y1 = x, y
    x2, y2 = x1 + size, y1
    x3, y3 = x1 + size, y1 + size
    x4, y4 = x1, y1 + size
    lx1, ly1, lx2, ly2 = self.laser.points
    if (self.laser.line_intersects(lx1, ly1, lx2, ly2, x1, y1, x2, y2) or
            self.laser.line_intersects(lx1, ly1, lx2, ly2, x2, y2, x3, y3) or
            self.laser.line_intersects(lx1, ly1, lx2, ly2, x3, y3, x4, y4) or
            self.laser.line_intersects(lx1, ly1, lx2, ly2, x4, y4, x1, y1)):
      return 1
    return 0

  def obstacles_remove(self, x, y):
    # deleting obstacles in range of projectile
    removed_obstacle = []
    radius = dp(self.bullet.radius)
    if self.projectile == 2:
      radius = dp(self.bomb.radius)

    for obstacle in self.obstacles:
      tx, ty = obstacle.pos
      diff = self.bullet.size[0]
      distance = math.sqrt((x - tx - diff) ** 2 + (y - ty - diff) ** 2)
      if distance <= radius and not(obstacle.iron == 1 and self.projectile == 1):
        removed_obstacle.append(obstacle)
        obstacle.image.size = 0, 0

    tx, ty = self.enemy.image.pos
    size = self.enemy.image.size[0]
    distance = math.sqrt((x - tx - size) ** 2 + (y - ty - size) ** 2)
    if distance <= radius and not self.bullet.collide_widget(self.enemy.image):
      self.enemy.damage(1)

    for obstacle in removed_obstacle:
      obstacle.pos = 0, constants.delPos
      obstacle.image.pos = 0, constants.delPos

  def set(self, tx, ty):
    # setting projectile's parameters

    if self.projectile == 1:
      self.bullet.set(tx, ty)
    elif self.projectile == 2:
      self.bomb.set(tx, ty)
      self.bomb.cur_color = 0
      self.bomb.color = [0, 0, 0, 1]
    else:
      self.laser.set(tx, ty)
    self.clock.cancel()
    self.clock = Clock.schedule_interval(self.update, 1 / 20)

  def on_touch_up(self, touch):
    # getting touch state and updating score
    x, y = touch.pos
    dp_x = x / Metrics.density
    dp_y = y / Metrics.density
    if x < dp(constants.startX) and y < dp(constants.startY) and self.gameOver is False:
      if self.projectile == 1:
        self.score -= 1
      else:
        self.score -= 2
      self.score_label.text = f"Score: {self.score}"
      self.score_label_back.text = f"Score: {self.score}"
      self.set(dp_x, dp_y)