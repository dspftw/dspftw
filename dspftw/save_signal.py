# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum
from typing import Tuple

import numpy as np

from .exceptions import WriteModeException
from .signal_types import FullSignalType
from .truncation import true_zero

class WriteMode(Enum):
    WRITE = 'wb'
    APPEND = 'ab'

def normalize_write_mode(mode: str) -> WriteMode:
    if mode == 'w':
        return WriteMode.WRITE

    if mode == 'a':
        return WriteMode.APPEND

    raise WriteModeException('Unknown write mode "{}"'.format(mode))

def save_signal(file_name: str, sig: np.array, signal_type: str, number_space: str,
                endianness: str, write_mode: str='w', trunc=true_zero) -> Tuple[int, int]:
    '''
    Function to use numpy package to write PCM data.

    Parameters
    ----------
    file_name:
        The name of the file to write.
    sig:
        numpy.array containing the signal.
    signal_type:
        The size and type of signal samples, such as '8t', '16t', '32t', '32f', '64f'.
    number_space:
        Number space of the file.  Valid values are 'real', 'r', 'complex', 'cplx', 'c'.
    endianness:
        Endianness of the file, such as 'big', 'b', 'little', 'l'.
    write_mode:
        'w' for new or overwrite. 'a' for append.
    trunc:
        Truncation function. or dspftw.true_zero or dspftw.true_one.
        Default is true_zero.

    Returns a tuple of the number of samples written and the number of samples clipped.
    '''

    full_signal_type = FullSignalType(signal_type, number_space, endianness)
    write_mode = normalize_write_mode(write_mode)

    if full_signal_type.is_twos_compliment_signal_type():
        sigflat, num_clipped = full_signal_type.clip_signal(sig)
        sigout = trunc(sigflat)

        # Modulo 2^8 or 2^16 to create two's complement
        sigout = np.remainder(sigout, 2*full_signal_type.scale())
        sigout = np.array(sigout, full_signal_type.numpy_dtype())

    else:
        num_clipped = 0

        if full_signal_type.is_complex():
            # Cast sample as the desired data type
            sigout = np.array([sig.real,sig.imag],
                              full_signal_type.numpy_dtype()).flatten("F")
        else:
            sigout = np.array(sig, full_signal_type.numpy_dtype())

    with open(file_name, write_mode.value) as outfile:
        sigout.tofile(outfile)

    num_written = len(sigout) // full_signal_type.items_per_sample()

    return num_written, num_clipped

def savesig(*args, **kwargs):
    '''
    Alias for save_signal.
    '''
    return save_signal(*args, **kwargs)
