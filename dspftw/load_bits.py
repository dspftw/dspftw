# vim: expandtab tabstop=4 shiftwidth=4

from bitstring import BitArray
from numpy import array as nparray

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
    bits = BitArray(file_name)
    bit_ints = (int(b) for b in bits.split(''))
    bool_array = nparray(bit_ints, dtype=bool)

    if count == -1:
        return bool_array[offset:]

    return bool_array[offset:offset+count]

def loadbits(*args, **kwargs) -> nparray:
    '''
    Alias for load_bits.
    '''
    return load_bits(*args, **kwargs)
