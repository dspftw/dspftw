# vim: expandtab tabstop=4 shiftwidth=4

from io import BufferedReader
from numpy import array as nparray
from typing import Iterable

def read_to_bools(reader: BufferedReader) -> Iterable[bool]:
    for byte in reader.read():
        for offset in range(8):
            yield byte & (0x80>>offset) == 0x80 >> offset

def load_bits(file_name: str, count: int=-1, offset: int=0) -> nparray:
    '''
    Loads bits from a file int a bool array.

    Parameters
    ----------
    file_name: string
        The name of the file to load.
    count: int
        The number of bits to load.
        Default is all.
    offset: int
        The number of bits to skip before loading.
        Default is zero.

    Returns a numpy bool array.
    '''
    with open(file_name, 'rb') as bit_file:
        byte_offset = offset // 8
        bit_file.seek(byte_offset)
        bit_offset_into_byte = offset % 8
        reader = BufferedReader(bit_file)
        bools = read_to_bools(reader)
        bool_array = nparray(list(bools), dtype=bool)

    if count == -1:
        return bool_array[bit_offset_into_byte:]

    return bool_array[bit_offset_into_byte:bit_offset_into_byte+count]

def loadbits(*args, **kwargs) -> nparray:
    '''
    Alias for load_bits.
    '''
    return load_bits(*args, **kwargs)
