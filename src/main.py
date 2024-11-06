from http_client import HTTP;

def showText(body):
  in_tag = False
  for c in body:
    if c == "<":
      in_tag = True
    elif c == ">":
      in_tag = False
    elif not in_tag:
      print(c, end="")

def load(url):
  content = url.request()
  showText(content)

if __name__ == '__main__':
  import sys
  load(HTTP(sys.argv[1]))
