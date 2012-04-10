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

import sys
import os
import re
from collections import deque
from os.path import *

# Configure extra includes here
# eg. extras = [ abspath(join(os.getcwd(), pardir)) ]
extras = [ "/Developer/Panda3D/lib", "/usr/share/panda3d" ]

class Bootstrap():
  """ Bootstrap for setting library paths
      
      Don't import this file into your project, actually copy it into
      your project directory and use it like this:

      import bootstrap
      
      What this does:

      - recurse upwards through the directory tree until finding a 'lib' folder.
      - add the lib folder the python path
      - decend into the lib folder and search for any sub folders named 'lib'
      - add them to the python path

      You can add alternative search locations by passing them into the
      extras array. These will also be searched for 'lib' folders the 
      same way.
  """
  
  __libPattern = "lib$"
  """ Attach dir matching this to the python path """

  __targets = []
  """ List of targets found """

  __queue = deque()
  """ Queue of directories ot process """

  def __seekRoot(self):
    """ Find the closest parent with a lib directory """
    found = False
    path = abspath(os.getcwd())
    while not found:
      for name in os.listdir(path):
        fullname = abspath(join(path, name))
        if isdir(fullname):
          if not re.match(self.__libPattern, name) is None:
            found = True
            self.__targets.append(fullname)
            self.__queue.append(fullname)
            break
      if not found:
        new_path = abspath(join(path, pardir))
        if path == new_path:
          found = True # No where left to look
        else:
          path = new_path

  def __processPath(self, path):
    """ Seek matches in path and enque directories """
    if os.path.exists(path):
      for name in os.listdir(path):
        fullname = abspath(join(path, name))
        if isdir(fullname):
          if not re.match(self.__libPattern, name) is None:
            self.__targets.append(fullname)
          else:
            self.__queue.append(fullname)

  def __addToPath(self):
    """ Add to python path """
    sys.path.extend(self.__targets)

  def load(self, extras):
    """ Load library dirs, including from extras """
    self.__queue.extend(extras)
    self.__targets.extend(extras)
    self.__seekRoot()
    while len(self.__queue) > 0:
      path = self.__queue.popleft()
      self.__processPath(path)
    self.__addToPath()

if not hasattr(Bootstrap, "__done"):
  bootstrap = Bootstrap()
  bootstrap.load(extras)
  Bootstrap.__done = True
