from lib import lib
from ctypes import *

class Api(object):
  """ Python bindings for the pyar library """

  def __init__(self):
    libar = CDLL(lib())

    # unsigned char *ar_get_rgb(void)
    libar.ar_get_rgb.restype = POINTER(c_char)

    self.libar = libar

  def rgb(self):
    """ Return the rgb handle """
    rgb = self.libar.ar_get_rgb()
    return rgb
