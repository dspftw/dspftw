import numpy as np
from numpy import array as nparray

def decimal_convert_to_base(decimal_number,base,num_digits):
    """
    Given an array of decimal integers, computes an array of numbers with given base
    """

    # Ensure we have integers
    decnum = np.rint(decimal_number).astype(int)
    # Exponent array
    expArr = np.kron(np.ones(decnum.shape,dtype=int),base**np.arange(num_digits-1,-1,-1,dtype=int))
    # Base array
    baseArr = np.kron(decnum,np.ones((1,num_digits),dtype=int))

    # Return
    return ((baseArr//expArr)%base)

def num2base(*args, **kwargs) -> nparray:
    '''
    Alias for decimal_convert_to_base.
    '''
    return decimal_convert_to_base(*args, **kwargs)
