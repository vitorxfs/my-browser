class HTMLLexer:
  def get_attributes(self, text):
    parts = text.split()
    tag = parts[0].casefold()
    if len(parts) < 2: return tag, {}

    attributes = {}
    buffer = ""
    in_quotes = False
    quote_type = ""
    key = ""
    for c in " ".join(parts[1:]):
      if in_quotes:
        if c == quote_type:
          attributes[key] = buffer
          quote_type = ""
          in_quotes = False
          key = ""
          buffer = ""
          continue
      else:
        if c == "=":
          key = buffer
          buffer = ""
          continue
        elif c in ["'", "\""]:
          in_quotes = True
          quote_type = c
          buffer = ""
          continue
        elif c.isspace():
          if key:
            attributes[key] = buffer or ""
            key = ""
            buffer = ""
            continue
          else:
            buffer = ""
            continue
      buffer += c
    return tag, attributes
