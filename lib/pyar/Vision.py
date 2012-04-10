# Copyright 2012 Douglas Linder
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyar
import time
from pandac.PandaModules import *
from direct.task import Task

class Vision(object):
  """ Vision helper """

  def __init__(self):
    self.api = pyar.Api()
    self.width = 640
    self.height = 480

  def next(self):
    rgb = self.api.rgb()
    return rgb

class VisionTexture(Texture):
  """ Texture using the vision class to read data """

  def __init__(self):
    Texture.__init__(self)
    self.__vision = Vision()
    self.setup2dTexture(self.__vision.width, self.__vision.height, Texture.TUnsignedByte, Texture.FRgb)
    self.makeRamImage()
    taskMgr.add(self.updateTextureTask, "updateTextureTask")

  def updateTextureTask(self, t):
    expectedSize = self.getExpectedRamImageSize()
    print("Expected length: " + str(expectedSize))
    rgb = self.__vision.next()
    p = PTAUchar.emptyArray(expectedSize)

    # This actually works
    # for i in range(0, self.__vision.width * self.__vision.height * 3):
    #   p.setElement(i, ord(rgb[i]))

    p.setSubdata(0, expectedSize, rgb)
    print("PTAU length: " + str(p.size()))

    self.setRamImage(CPTAUchar(p))
    return Task.cont
