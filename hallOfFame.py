from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.uix.label import Label

LabelBase.register(name='PixelifySans',
                   fn_regular='./Pixelify_Sans/PixelifySans-VariableFont_wght.ttf')

import constants


class HallOfFame(Screen):
  def __init__(self, **kwargs):
    super(HallOfFame, self).__init__(**kwargs)
    self.record_list()
    self.X = constants.labelX
    self.Y = constants.labelY
    self.spacing = constants.labelSpacing
    with self.canvas:
      self.records = []
      self.records_init()

  def record_list(self):
    # getting records to work with them in future
    file = open('./records.txt', 'r+')
    self.record = []
    for line in file:
      self.record.append(line)
    print(self.record)
    file.close()

  def records_init(self):
    # presenting records depending on rank
    cnt = 1
    for record in self.record:
      rec = record[:2]
      if cnt == 1:
        score_label = Label(text=f"1ST                     00{rec}", font_size='24sp',
                            pos=(dp(self.X), dp(self.Y - cnt * self.spacing)), font_name='PixelifySans', color=(1, 0.6, 0.2, 1))
      elif cnt == 2:
        score_label = Label(text=f"2ND                     00{rec}", font_size='24sp',
                            pos=(dp(self.X), dp(self.Y - cnt * self.spacing)), font_name='PixelifySans', color=(0.4, 0.6, 1, 1))
      elif cnt == 3:
        score_label = Label(text=f"3RD                     00{rec}", font_size='24sp',
                            pos=(dp(self.X), dp(self.Y - cnt * self.spacing)), font_name='PixelifySans', color=(0.4, 0.6, 1, 1))
      elif cnt == 10:
        score_label = Label(text=f"{cnt}TH                     00{rec}", font_size='24sp',
                            pos=(dp(self.X-5), dp(self.Y - cnt * self.spacing)), font_name='PixelifySans', color=(0.8, 0.9, 1, 1)) #0.7, 0.9, 1, 1
      else:
        score_label = Label(text=f"{cnt}TH                     00{rec}", font_size='24sp',
                            pos=(dp(self.X), dp(self.Y - cnt * self.spacing)), font_name='PixelifySans', color=(0.8, 0.9, 1, 1))
      self.records.append(score_label)
      cnt += 1

  def records_update(self):
    # updating hall of fame
    cnt = 1
    self.record_list()
    for record in self.records:
      rec = self.record[cnt-1]
      rec = rec[:2]
      if cnt == 1:
        record.text = f"1ST                     00{rec}"
      elif cnt == 2:
        record.text = f"2ND                     00{rec}"
      elif cnt == 3:
        record.text = f"3RD                     00{rec}"
      else:
        record.text = f"{cnt}TH                     00{rec}"
      cnt += 1


