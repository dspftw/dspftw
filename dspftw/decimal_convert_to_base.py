# vim: expandtab tabstop=4 shiftwidth=4

from numpy import arange, kron, rint, ones
from numpy import array as nparray

def decimal_convert_to_base(decimal_number: nparray, base: int, num_digits: int):
    """
    Given an array of decimal integers, computes an array of numbers with given base
    Parameters
    ----------
    decimal_number:
        numpy.array of base 10 integers.
    base: int
        convert to integers using this base.
    num_digits: int
        number of digits output per input integer.

    Returns a numpy int array.
    """

    # Ensure we have integers
    decnum = rint(decimal_number).astype(int)
    # Exponent array
    exp_arr = kron(ones(decnum.shape,dtype=int),base**arange(num_digits-1,-1,-1,dtype=int))
    # Base array
    base_arr = kron(decnum,ones((1,num_digits),dtype=int))

    # Return
    return ((base_arr//exp_arr)%base)

def num2base(*args, **kwargs) -> nparray:
    '''
    Alias for decimal_convert_to_base.
    '''
    return decimal_convert_to_base(*args, **kwargs)
