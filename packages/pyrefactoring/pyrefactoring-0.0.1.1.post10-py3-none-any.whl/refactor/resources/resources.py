import io
import rawpy
import base64
import hashlib
import pillow_heif
import pandas as pd
from PIL import Image
from typing import Any
from refactor.objects import Object
from refactor.resources.loaders import ResourceLoaders
# Support HEIC/HEIF image.
pillow_heif.register_heif_opener()



class Resource(Object):
  """
  Load resource as raw bytes.
  """
  @property
  def data(self) -> Any:
    return self.__data__
  
  @property
  def hash(self) -> str:
    return hashlib.md5(self.data).hexdigest()
  
  @property
  def base64(self) -> str:
    return str(base64.b64encode(self.data))
  
  @property
  def size(self) -> int:
    return len(self.data)

  def __init__(self, source: Any, *args, **kwds) -> None:
    super().__init__(*args, **kwds)
    self.__data__ = ResourceLoaders().load(source, *args, **kwds)



class ImageResource(Resource):
  """
  Load resource as PIL Image. 
  Supports for RAW and Apple HEIC/HEIF image.
  """
  @property
  def image(self) -> Image.Image:
    return self.__image__

  def __init__(self, source: Any, *args, **kwds) -> None:
    super().__init__(source, *args, **kwds)
    buffer = io.BytesIO(self.data)
    try:
      self.__image__ = Image.open(buffer)
    except:
      buffer.seek(0)
      try:
        with rawpy.imread(buffer) as raw:
          thumb = raw.extract_thumb()
        if thumb.format == rawpy.ThumbFormat.JPEG:
          buffer = io.BytesIO(thumb.data)
          self.__image__ = Image.open(buffer)
        elif thumb.format == rawpy.ThumbFormat.BITMAP:
          self.__image__ = Image.fromarray(thumb.data)
      except:
        raise AssertionError(f'Cannot load image asset from {str(source):20s}')
      


__PD_READERS__ = (
  pd.read_csv, pd.read_excel, pd.read_json, pd.read_xml, pd.read_sql, pd.read_stata, pd.read_sql_query,
  pd.read_sql_table, pd.read_spss, pd.read_html, pd.read_parquet, pd.read_hdf, pd.read_pickle, pd.read_gbq,
  pd.read_fwf, pd.read_orc, pd.read_feather, pd.read_sas, pd.read_table
)

class DataframeResource(Resource):
  """
  Load data resource as pandas dataframe.
  """
  @property
  def dataframe(self) -> pd.DataFrame:
    return self.__dataframe__

  def __init__(self, source: Any, *args, **kwargs) -> None:
    super().__init__(source, *args, **kwargs)
    for reader in __PD_READERS__:
      buffer = io.BytesIO(self.data)
      try:
        self.__dataframe__ = reader(buffer)
        return
      except:
        continue
    raise AssertionError(f"Cannot load dataframe from {str(source):20s}")
