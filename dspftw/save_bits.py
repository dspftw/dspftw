# vim: expandtab tabstop=4 shiftwidth=4

from typing import IO
from numpy import array as nparray
from numpy import packbits

from .writemode import normalize_write_mode

def save_bits_to(writable: IO, bool_array: nparray, packed=True) -> int:
    '''
    Save bits to a writable object, such as an open file.
    This can be useful when you want to keep writing
    to the same file object, or reopen a file in append
    mode.

    Parameters
    ----------
    writable: file-like IO object
        A file-like object that has a write() method.
    bool_array: numpy.array
        The bool array.
    packed: bool
        Whether to pack the bits into bytes.
        Defaults to True.

    Returns the number of bytes written.

    Example
    -------
    # Opens an output file in append mode.
    with open('some_file.bits', 'a+b') as outfile:
        save_bits_to(outfile, array_of_bits)
    '''

    if packed:
        bytes_to_write = packbits(bool_array).tobytes()  # pylint: disable=E1101

    else:
        bytes_to_write = nparray(bool_array).tobytes()

    writable.write(bytes_to_write)
    return len(bytes_to_write)

def save_bits(file_name: str, bool_array: nparray, packed=True, write_mode: str='w') -> int:
    '''
    Save bits to a file from a bool array.

    Parameters
    ----------
    file_name: string
        The name of the file to save.
    bool_array: numpy.array
        The bool array.
    packed: bool
        Whether to pack the bits into bytes.
        Default is True.
    write_mode: str
        'w' for new or overwrite. 'a' for append.
        Default is w
    Returns the number of bytes written.
    '''

    write_mode = normalize_write_mode(write_mode)

    with open(file_name, write_mode.value) as bit_file:
        return save_bits_to(bit_file, bool_array, packed)

def savebits(*args, **kwargs) -> int:
    '''
    Alias for save_bits.
    '''
    return save_bits(*args, **kwargs)
