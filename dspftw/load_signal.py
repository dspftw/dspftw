# vim: expandtab tabstop=4 shiftwidth=4

from sys import byteorder

from numpy import array as nparray
from numpy import fromfile

from .signal_types import FullSignalType

def load_signal(file_name: str, signal_type: str, number_space: str, endianness: str=byteorder, num_samples: int=-1, start_sample: int=0) -> nparray:
    '''
    Loads a signal from a file in float or two's compliment, real or complex format.

    Parameters
    ----------
    file_name:
        The name of the file to load.
    signal_type:
        The size and type of signal samples, such as '8t', '16t', '32t', '32f', '64f'.
    number_space:
        Number space of the file.  Valid values are 'real', 'r', 'complex', 'cplx', 'c'.
    endianness:
        Endianness of the file, such as 'big', 'b', 'little', 'l'.
        Defaults to the system endianness.
    num_samples:
        The number of samples to load from the file.
    start_sample:
        The number of samples to skip before loading.

    Returns a numpy array.
    '''
    full_signal_type = FullSignalType(signal_type, number_space, endianness)
    data = fromfile(file_name,
                    dtype=full_signal_type.numpy_dtype(),
                    offset=full_signal_type.offset(start_sample),
                    count=full_signal_type.count(num_samples))
    return full_signal_type.post_load(data)

def loadsig(*args, **kwargs) -> nparray:
    '''
    Alias for load_signal.
    '''
    return load_signal(*args, **kwargs)
