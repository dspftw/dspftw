# vim: expandtab tabstop=4 shiftwidth=4

from io import BufferedWriter
from numpy import array as nparray
from typing import Iterable

def bools_to_bytes(bools: Iterable[bool]) -> Iterable[bytes]:
    for boolean in bools:
        if boolean:
            yield b'\x01'

        else:
            yield b'\x00'

def pack_bools_to_bytes(bools: Iterable[bool]) -> Iterable[bytes]:
    offset = 0
    current_byte = 0x00

    for boolean in bools:
        current_bit = 0x00

        if boolean == True:
            current_bit = 0x01

        current_byte = current_byte | (current_bit << (7 - (offset % 8)))
        offset += 1

        if offset % 8 == 0:
            yield current_byte.to_bytes(1, 'big')
            current_byte = 0x00

    if offset % 8 != 0:
        yield current_byte.to_bytes(1, 'big')

def save_bits(file_name: str, bool_array: nparray, packed=True) -> int:
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
        Defaults to True.

    Returns the number of bytes saved.
    '''
    with open(file_name, 'wb') as bit_file:
        writer = BufferedWriter(bit_file)
        count = 0

        if packed:
            for byte in pack_bools_to_bytes(bool_array):
                writer.write(byte)
                count += 1

        else:
            for byte in bools_to_bytes(bool_array):
                writer.write(byte)
                count += 1

        writer.flush()

    return count

def savebits(*args, **kwargs) -> int:
    '''
    Alias for save_bits.
    '''
    return save_bits(*args, **kwargs)
