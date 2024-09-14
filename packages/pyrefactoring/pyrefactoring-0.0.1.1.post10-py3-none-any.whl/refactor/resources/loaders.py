import io
import base64
import urllib
from typing import Any
from pathlib import Path
from abc import ABC, abstractmethod
import urllib.request
from refactor.patterns.creational import Singleton


def load_file(source: Any, *args, **kwds) -> bytes:
  return Path(source).expanduser().resolve().read_bytes()

def load_url(source: Any, *args, **kwds) -> bytes:
  with urllib.request.urlopen(source) as url:
    return url.read()
  
def load_base64(source: Any, *args, **kwds) -> bytes:
  return base64.b64decode(source, validate=True)

def load_bytes(source: Any, *args, **kwds) -> bytes:
  return io.BytesIO(source).read()


class ResourceLoaders(metaclass=Singleton):
  """
  Manage resource loaders.
  """
  def __init__(self):
    self.__loaders__ = [load_file, load_url, load_base64, load_bytes]

  def load(self, source: Any, *args, **kwds) -> bytes:
    for loader in self.__loaders__:
      try:
        return loader(source, *args, **kwds)
      except:
        continue
    raise AssertionError(f"Cannot load resource {str(source):20s}")
