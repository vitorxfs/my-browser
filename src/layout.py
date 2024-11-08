import tkinter
import tkinter.font

from parser import Text, Element

HSTEP, VSTEP = 9, 18

FONTS = {}


sizes = {
  'h1': 16,
  'h2': 14,
  'h3': 12,
  'default': 10,
}
weights = {
  'default': 'normal',
}
slants = {
  'default': 'roman'
}

class Layout:
  def __init__(self, tokens, dimensions):
    self.display_list = []
    self.cursor_x = HSTEP
    self.cursor_y = VSTEP
    self.style = slants['default']
    self.weight = weights['default']
    self.size = sizes['default']
    self.width, _ = dimensions
    self.line = []
    self.__recurse(tokens)
    self.__flush()

  def __open_tag(self, tag):
    if tag == "h1":
      self.size = 16

  def __close_tag(self, tag):
    if tag == "h1":
      self.size = 10

  def __recurse(self, tree):
    if isinstance(tree, Text):
      for word in tree.text.split():
        self.__word(word)
    else:
      self.__open_tag(tree.tag)
      for child in tree.children:
        self.__recurse(child)
      self.__close_tag(tree.tag)

  def __word(self, word):
    font = self.__get_font(self.size, self.weight, self.style)
    w = font.measure(word)
    if (self.cursor_x + w > self.width - HSTEP):
      self.__flush()
    self.line.append((self.cursor_x, word, font))
    self.cursor_x += w + font.measure(" ")

  def __flush(self):
    if not self.line: return
    metrics = [font.metrics() for x, word, font in self.line]
    max_ascent = max([metric["ascent"] for metric in metrics])
    baseline = self.cursor_y + 1.25 * max_ascent
    for x, word, font in self.line:
      y = baseline - font.metrics("ascent")
      self.display_list.append((x, y, word, font))
    max_descent = max([metric["descent"] for metric in metrics])
    self.cursor_y = baseline + 1.25 * max_descent
    self.cursor_x = HSTEP
    self.line = []

  def __get_font(self, size, weight, style):
    key = (size, weight, style)
    if key not in FONTS:
      font = tkinter.font.Font(size=size, weight=weight, slant=style)
      label = tkinter.Label(font=font)
      FONTS[key] = (font, label)
    return FONTS[key][0]
