# vim: expandtab tabstop=4 shiftwidth=4

from numpy import arange, inner
from numpy import array as nparray

from .exceptions import DSPFTWException


def base_convert_to_decimal(base_array: nparray, base: int) -> nparray:
    """
    Given an array of columns modulo 'base', computes an array of decimal numbers.

    Parameters
    ----------
    base_array:
        numpy.array of integers in [0, base). Each column represents one
        number, with the most significant digit in the first row.
        A one-dimensional array represents a single number.
    base:
        Base from which to convert. Must be an integer greater than or equal to 2.

    Returns
    -------
    numpy.array
        Decimal representation of each column in base_array.
    """

    if not isinstance(base, int):
        raise DSPFTWException('base must be an integer')

    if base < 2:
        raise DSPFTWException('base must be at least 2')

    arr = base_array.copy()

    # Number of dimensions of array
    dim = len(arr.shape)

    if dim < 1 or dim > 2:
        raise DSPFTWException('base_array must have one or two dimensions')

    # Ensure all digits are integers
    if not ((arr % 1) == 0).all():
        raise DSPFTWException('base_array must contain only integers')

    # Ensure all digits are valid for the specified base
    if ((arr < 0) | (arr >= base)).any():
        raise DSPFTWException('base_array contains an invalid digit')

    # Ensure at least 2 dimensions
    if dim == 1:
        arr = nparray([arr]).transpose()

    # Number of digits
    num_digits = arr.shape[0]

    base_exp = base**arange(num_digits - 1, -1, -1)

    return inner(base_exp, arr.transpose())


def base2num(*args, **kwargs) -> nparray:
    '''
    Alias for base_convert_to_decimal.
    '''
    return base_convert_to_decimal(*args, **kwargs)
