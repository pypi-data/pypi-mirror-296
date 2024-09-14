from typing import Any
from refactor.objects import Object
from json import JSONEncoder, JSONDecoder
from refactor.patterns.creational import Singleton



class JsonSerializer(JSONEncoder, JSONDecoder, metaclass=Singleton):
  """
  (De)serialize objects from/to JSON data.
  """

  def __init__(self) -> None:
    self.__cached__ = list()
    JSONEncoder.__init__(self, default=self.__encoding__)
    JSONDecoder.__init__(self, object_hook=self.__decoding__)

  def __encoding__(self, data):
    return data.asdict(cache=self.__cached__) if isinstance(data, Object) else super().default(data)
  
  def encode(self, o: Any) -> str:
    self.__cached__.clear()
    return super().encode(o)
  
  def __decoding__(self, data: dict):
    return Object.fromdict(data)
