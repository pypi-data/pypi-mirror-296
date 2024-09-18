# -*- coding=utf-8 -*-

from tinymoss import TinyMoss
import time



if __name__ == '__main__':
  
  moss = TinyMoss()
  try:
    moss.startup()
  except KeyboardInterrupt:
    moss.shutdown()
  