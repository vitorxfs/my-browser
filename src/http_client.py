import socket

def splitUrl(url):
  # Separates the scheme (http/https) from the url (example.org)
  scheme, url = url.split('://', 1)
  assert scheme == "http"
  if "/" not in url:
    url = url + "/"
  host, url = url.split("/", 1)
  path = "/" + url
  return (scheme, host, path)

def buildRequest(method, path, host):
  request = "{} {} HTTP/1.0\r\n".format(method, path)
  request += "HOST: {}\r\n".format(host)
  request += "\r\n"
  return request

def readResponse(s):
  response = s.makefile("r", encoding="utf8", newline="\r\n")
  statusline = response.readline()
  version, status, explanation = statusline.split(" ", 2)
  headers = {}
  while True:
    line = response.readline()
    if line == "\r\n":
      break
    header, value = line.split(":", 1)
    headers[header.casefold()] = value.strip()
  assert "transfer-encoding" not in headers
  assert "content-encoding" not in headers
  content = response.read()

  return (status, headers, content, (version, status, explanation))

class HTTP:
  def __init__(self, url):
    self.scheme, self.host, self.path = splitUrl(url)

  def request(self):
    s = socket.socket(
      family=socket.AF_INET,
      type=socket.SOCK_STREAM,
      proto=socket.IPPROTO_TCP,
    )
    s.connect((self.host, 80))
    request = buildRequest("GET", self.path, self.host)
    print(request)
    s.send(request.encode("utf8"))
    status, headers, content, details = readResponse(s)
    s.close()
    return content
