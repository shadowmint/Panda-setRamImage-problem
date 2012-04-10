from lib import lib
from ctypes import *

class Api(object):
  """ Python bindings for the pyar library """

  def __init__(self):
    libar = CDLL(lib())

    # int8_t *ar_get_rgb()
    libar.ar_get_rgb.restype = POINTER(c_char)

    self.libar = libar

  def rgb(self):
    """ Return the rgb handle """
    rgb = self.libar.ar_get_rgb()
    return rgb
