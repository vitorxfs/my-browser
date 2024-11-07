import tkinter
import tkinter.font

from lex import Text, Tag

HSTEP, VSTEP = 9, 18

FONTS = {}

sizes = {
  'h1': 16,
  '/h1': 10,
  'h2': 14,
  '/h2': 10,
  'h3': 12,
  '/h3': 10,
  'default': 10
}
weights = {
  'strong': 'bold',
  'b': 'bold',
  '/strong': 'normal',
  '/b': 'normal',
  'default': 'normal',
}
slants = {
  'i': 'italic',
  'i': 'roman',
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
    for tok in tokens: self.__token(tok)
    self.__flush()

  def __token(self, tok):
    font = self.__get_font(self.size, self.weight, self.style)
    if isinstance(tok, Text):
      for word in tok.text.split():
        self.__word(word, font)
    else:
      if tok.tag in sizes: self.size = sizes[tok.tag]
      if tok.tag in slants: self.style = slants[tok.tag]
      if tok.tag in weights: self.weight = weights[tok.tag]
      if tok.tag in ['br', '/p', '/h1', '/h2', '/h3', '/aside']: self.__flush()

  def __word(self, word, font):
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
