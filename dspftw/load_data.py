# vim: expandtab tabstop=4 shiftwidth=4

from numpy import array as nparray
from numpy import fromfile

from .data_types import FullDataType

def load_data(file_name: str, data_type: str, endianness: str, count: int=-1, offset: int=0) -> nparray:
    full_data_type = FullDataType(data_type, endianness)
    data = fromfile(file_name,
                    dtype=full_data_type.numpy_dtype(),
                    offset=offset,
                    count=count)
    return data

def loaddata(*args, **kwargs) -> nparray:
    return load_data(*args, **kwargs)
