from http_client import HTTP
import tkinter

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 9, 18

class Browser:
  def __init__(self):
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(
      self.window,
      width=WIDTH,
      height=HEIGHT
    )
    self.canvas.pack()

  def load(self, url):
    http = HTTP(url)
    content = http.request()
    text = self.__lex(content)
    self.display_list = self.__layout(text)
    self.draw()

  def draw(self):
    for x, y, c in self.display_list:
      self.canvas.create_text(x, y, text=c)

  def __layout(self, text):
    display_list=[]
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
      display_list.append((cursor_x, cursor_y, c))
      cursor_x += HSTEP
      if cursor_x >= WIDTH - HSTEP:
        cursor_y += VSTEP
        cursor_x = HSTEP
    return display_list

  def __lex(self, body):
    text=""
    in_tag = False
    for c in body:
      if c == "<":
        in_tag = True
      elif c == ">":
        in_tag = False
      elif not in_tag:
        text += c
    return text