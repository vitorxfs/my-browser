import tkinter
import tkinter.font

from http_client import HTTP
from layout import Layout, VSTEP
from lex import Text, Tag

SCROLL_STEP = 100

WIDTH, HEIGHT = 800, 600

class Browser:
  def __init__(self):
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(
      self.window,
      width=WIDTH,
      height=HEIGHT
    )
    self.canvas.pack()
    self.scroll = 0
    self.window.bind("<Down>", self.__scrolldown)
    self.window.bind("<Up>", self.__scrollup)
    ## MouseWheel
    self.window.bind("<Button-4>", self.__scrollup)
    self.window.bind("<Button-5>", self.__scrolldown)

  def load(self, url):
    http = HTTP(url)
    content = http.request()
    tokens = self.__lex(content)
    self.display_list = Layout(tokens, (WIDTH, HEIGHT)).display_list
    self.draw()

  def draw(self):
    self.canvas.delete("all")
    for x, y, c, font in self.display_list:
      if y > self.scroll + HEIGHT: continue
      if y + VSTEP < self.scroll : continue
      self.canvas.create_text(x, y - self.scroll, text=c, font=font, anchor="nw")

  def __lex(self, body):
    out = []
    buffer=""
    in_tag = False
    for c in body:
      if c == "<":
        in_tag = True
        if buffer: out.append(Text(buffer))
        buffer = ""
      elif c == ">":
        in_tag = False
        out.append(Tag(buffer))
        buffer = ""
      else:
        buffer += c
    if not in_tag and buffer:
      out.append(Text(buffer))
    return out

  def __scrolldown(self, e):
    self.scroll += SCROLL_STEP
    self.draw()

  def __scrollup(self, e):
    self.scroll -= SCROLL_STEP
    self.draw()
