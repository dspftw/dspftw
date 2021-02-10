# vim: expandtab tabstop=4 shiftwidth=4

from sys import byteorder

from numpy import array as nparray
from numpy import fromfile

from .data_types import FullDataType

def load_data(file_name: str, data_type: str, endianness: str=byteorder, count: int=-1, offset: int=0) -> nparray:
    '''
    Loads data from a file.

    Parameters
    ----------
    file_name: string
        The name of the file to load.
    data_type: string
        The type of data to load, such as 'uint16', 'int8', or 'float64'.
    endianness: string
        The endianness of the data, such as 'b', 'big', 'l', or 'little'.
        Defaults to the system byte order.
    count: int
        The number of data elements to load.  Defaults to the whole file.
    offset: int
        The number of initial data elements to skip in the file.  Defaults to zero.

    Returns a numpy array.
    '''
    full_data_type = FullDataType(data_type, endianness)
    data = fromfile(file_name,
                    dtype=full_data_type.numpy_dtype(),
                    offset=offset,
                    count=count)
    return data

def loaddata(*args, **kwargs) -> nparray:
    '''
    Alias for load_data.
    '''
    return load_data(*args, **kwargs)
