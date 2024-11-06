from http_client import HTTP
import tkinter
import tkinter.font

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 9, 18
SCROLL_STEP = 100

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
    text = self.__lex(content)
    self.display_list = self.__layout(text)
    self.draw()

  def draw(self):
    self.canvas.delete("all")
    for x, y, c, font in self.display_list:
      if y > self.scroll + HEIGHT: continue
      if y + VSTEP < self.scroll : continue
      self.canvas.create_text(x, y - self.scroll, text=c, font=font, anchor="nw")

  def __layout(self, tokens):
    display_list=[]
    cursor_x, cursor_y = HSTEP, VSTEP
    style = "roman"
    weight = "normal"
    for tok in tokens:
      if isinstance(tok, Text):
        font = tkinter.font.Font(
          family="Inter",
          size=10,
          weight=weight,
          slant=style
        )
        for word in tok.text.split():
          w = font.measure(word)
          if (cursor_x + w > WIDTH - HSTEP) or (word == "\n"):
            cursor_y += font.metrics("linespace") * 1.25
            cursor_x = HSTEP
          display_list.append((cursor_x, cursor_y, word, font))
          cursor_x += w + font.measure(" ")
      elif tok.tag == "i": style = "italic"
      elif tok.tag == "/i": style = "roman"
      elif tok.tag in ["b", "strong"]: weight = "bold"
      elif tok.tag in ["/b", "/strong"]: weight = "normal"
    return display_list

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

  def __mousewheel(self, e):
    print("oi")
    delta = int(e.delta)
    print(delta)
    if delta < 0: self.__scrolldown()
    else: self.__scrollup()

class Text:
  def __init__(self, text):
    self.text = text

class Tag:
  def __init__(self, tag):
    self.tag = tag
