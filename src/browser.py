import tkinter
import tkinter.font

from http_client import HTTP
from layout import Layout, VSTEP
from parser import HTMLParser, Element

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
    # MouseWheel
    self.window.bind("<Button-4>", self.__scrollup)
    self.window.bind("<Button-5>", self.__scrolldown)

  def load(self, url):
    http = HTTP(url)
    content = http.request()
    self.nodes = HTMLParser(content).parse()
    self.display_list = Layout(self.nodes, (WIDTH, HEIGHT)).display_list
    self.draw()

  def draw(self):
    self.canvas.delete("all")
    for x, y, c, font in self.display_list:
      if y > self.scroll + HEIGHT: continue
      if y + VSTEP < self.scroll : continue
      self.canvas.create_text(x, y - self.scroll, text=c, font=font, anchor="nw")

  def __scrolldown(self, e):
    self.scroll += SCROLL_STEP
    self.draw()

  def __scrollup(self, e):
    self.scroll -= SCROLL_STEP
    self.draw()
