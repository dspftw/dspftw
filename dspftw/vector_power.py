import numpy as np
from numpy import array as nparray

def vector_power(vector):
    """
    Compute the average power for a complex ndarray vector
    """

    # Equivalent Octave code: vector*vector'/length(vector)
    # Ensure vector is a complex row vector
    vector = np.array([vector.flatten()]).astype(complex)
    # Return
    return ((vector.dot(np.transpose(vector.conjugate()))).real)[0,0]/float(vector.shape[1])

def vecpow(*args, **kwargs) -> nparray:
    '''
    Alias for vector_power.
    '''
    return vector_power(*args, **kwargs)
