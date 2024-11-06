from http_client import HTTP;
from browser import Browser;
import tkinter

if __name__ == '__main__':
  import sys
  Browser().load(sys.argv[1])
  tkinter.mainloop()
