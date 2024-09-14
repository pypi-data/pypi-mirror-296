from uuid import uuid4
from typing import Any
from refactor import logging
from importlib import import_module
from refactor.patterns.creational import Singleton


class Object:
  """
  Object class is base class of all inherited objects in the library.
  """
  
  @property
  def instance(self) -> Any:
    return self

  @property
  def oid(self) -> str:
    return self.__oid__
  
  @property
  def classname(self) -> str:
    return self.__class__.__name__
  
  @property
  def modulename(self) -> str:
    return self.__modulename__
  
  @property
  def logger(self) -> logging.Logger:
    return logging.getLogger(f"{__name__}.{self.classname}")

  def __init__(self, *args, **kwds) -> None:
    self.__oid__ = kwds.get("oid", uuid4().hex)
    self.__modulename__ = kwds.get(
      "__modulename__",
      "refactor" if self.__class__ == Object else self.__module__
    )
    # Support attrs init.
    if "__attrs_init__" in dir(self):
      self.__attrs_init__(*args, **kwds)
    # Register object to manager.
    ObjectManager().register(self)

  def asdict(self, *args, **kwds) -> dict:
    if "cache" not in kwds:
      kwds.update({"cache": list()})
    if self.oid in kwds["cache"]:
      return Reference(oid=self.oid).asdict(*args, **kwds)
    else:
      kwds["cache"].append(self.oid)
      ignores = kwds.get("ignores", ())
      keys = [x for x in dir(self) if not x.startswith("_") and x not in ("object", "logger") and x not in ignores]
      vals = [getattr(self, x) for x in keys]
      vals = [x if not isinstance(x, Object) else x.asdict(*args, **kwds) for x in vals ]
    return dict(zip(keys, vals))
  
  @staticmethod
  def fromdict(data: dict, *args, **kwds) -> Any:
    if "classname" in data and "modulename" in data:
      return getattr(import_module(data.pop("modulename")), data.pop("classname"))(**data)
    else:
      return data



class Reference(Object):
  """
  Reference is used as a proxy to prevent circular object connections.
  """

  @property
  def instance(self) -> Any:
    return ObjectManager().get(self.oid)

  def __init__(self, oid: str, *args, **kwds) -> None:
    self.__oid__ = kwds.get("oid", uuid4().hex)
    self.__modulename__ = kwds.get(
      "__modulename__",
      "refactor.objects" if self.__class__ == Reference else self.__module__
    )

  def asdict(self, *args, **kwds) -> dict:
    return {
      "oid": self.oid,
      "classname": self.classname, 
      "modulename": self.modulename
    }



class ObjectManager(metaclass=Singleton):
  """
  Singleton that keeps and manage all created objects.
  """

  def __init__(self) -> None:
    self.__objects__ = dict[str, Object]()

  def get(self, oid: str) -> Any:
    return self.__objects__.get(oid, None)

  def register(self, obj: Object) -> Any:
    if obj.oid not in self.__objects__:
      self.__objects__.update({obj.oid: obj})
    return self
  
  def unregister(self, oid: str) -> Any:
    if oid in self.__objects__:
      obj = self.__objects__.pop(oid)
      del obj
    return self
