import tkinter
import tkinter.font

from lex import Text, Tag

HSTEP, VSTEP = 9, 18

class Layout:
  def __init__(self, tokens, dimensions):
    self.display_list = []
    self.cursor_x = HSTEP
    self.cursor_y = VSTEP
    self.style = "roman"
    self.weight = "normal"
    self.width, _ = dimensions
    for tok in tokens:
      self.__token(tok)

  def __token(self, tok):
    font = tkinter.font.Font(
      family="Inter",
      size=10,
      weight=self.weight,
      slant=self.style
    )
    if isinstance(tok, Text):
      for word in tok.text.split():
        self.__word(word, font)
    elif tok.tag == "i": self.style = "italic"
    elif tok.tag == "/i": self.style = "roman"
    elif tok.tag in ["b", "strong"]: self.weight = "bold"
    elif tok.tag in ["/b", "/strong"]: self.weight = "normal"

  def __word(self, word, font):
    w = font.measure(word)
    if (self.cursor_x + w > self.width - HSTEP) or (word == "\n"):
      self.cursor_y += font.metrics("linespace") * 1.25
      self.cursor_x = HSTEP
    self.display_list.append((self.cursor_x, self.cursor_y, word, font))
    self.cursor_x += w + font.measure(" ")
