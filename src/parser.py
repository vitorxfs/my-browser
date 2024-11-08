from lexer import HTMLLexer

class Text:
  def __init__(self, text, parent):
    self.text = text
    self.children = []
    self.parent = parent

  def __repr__(self):
    return repr(self.text)

class Element:
  def __init__(self, tag, attributes, parent):
    self.tag = tag
    self.attributes = attributes
    self.children = []
    self.parent = parent

  def __repr__(self):
    string_attributes = ""
    for attr in self.attributes:
      string_attributes += " " + attr + "=" + "\"" + self.attributes[attr] + "\""
    return "" + self.tag + string_attributes + ""

class HTMLParser:
  SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
  ]
  HEAD_TAGS = [
    "base", "basefont", "bgsound", "noscript",
    "link", "meta", "title", "style", "script",
  ]

  def __init__(self, body):
    self.body = body
    self.stack = []

  def parse(self):
    buffer=""
    in_tag = False
    for c in self.body:
      if c == "<":
        in_tag = True
        if buffer: self.__add_text(buffer)
        buffer = ""
      elif c == ">":
        in_tag = False
        self.__add_tag(buffer)
        buffer = ""
      else:
        buffer += c
    if not in_tag and buffer:
      self.__add_text(buffer)
    return self.__finish()

  def __add_text(self, text):
    if text.isspace(): return
    self.__implicit_tags(None)
    if len(self.stack) == 0: return
    parent = self.stack[-1]
    node = Text(text, parent)
    parent.children.append(node)

  def __add_tag(self, tag):
    if tag.startswith("!"): return
    tag, attributes = HTMLLexer().get_attributes(tag)
    self.__implicit_tags(tag)
    if tag.startswith("/"):
      if len(self.stack) == 1: return
      node = self.stack.pop()
      parent = self.stack[-1]
      parent.children.append(node)
    elif tag in self.SELF_CLOSING_TAGS:
      parent = self.stack[-1]
      node = Element(tag, attributes, parent)
      parent.children.append(node)
    else:
      parent = self.stack[-1] if self.stack else None
      node = Element(tag, attributes, parent)
      self.stack.append(node)

  def __finish(self):
    if not self.stack:
      self.__implicit_tags(None)
    while len(self.stack) > 1:
      node = self.stack.pop()
      parent = self.stack[-1]
      parent.children.append(node)
    return self.stack.pop()

  def __implicit_tags(self, tag):
    while True:
      open_tags = [node.tag for node in self.stack]
      if open_tags == [] and tag != "html":
        self.__add_tag("html")
      elif open_tags == ["html"] and tag not in ["head", "body", "/html"]:
        if tag in self.HEAD_TAGS:
          self.__add_tag("head")
        else:
          self.__add_tag("body")
      elif open_tags == ["html", "head"] and tag not in ["/head"] + self.HEAD_TAGS:
        self.add_tag("/head")
      else:
        break
