# vim: expandtab tabstop=4 shiftwidth=4

from sys import byteorder

from numpy import array as nparray

from .data_types import FullDataType

def save_data(file_name: str, data: nparray, data_type: str, endianness: str=byteorder) -> int:
    '''
    Saves data to a file.

    Parameters
    ----------
    file_name: string
        The name of the file to save.
    data: numpy.array
        The data to save.
    data_type: string
        The type of data to save, such as 'uint16', 'int8', or 'float64'.
    endianness: string
        The endianness of the data, such as 'b', 'big', 'l', or 'little'.
        Defaults to the system byte order.

    Returns the number of elements saved.
    '''
    full_data_type = FullDataType(data_type, endianness)
    data.astype(full_data_type.numpy_dtype()).tofile(file_name)
    return data.size

def savedata(*args, **kwargs) -> nparray:
    '''
    Alias for save_data.
    '''
    return save_data(*args, **kwargs)
