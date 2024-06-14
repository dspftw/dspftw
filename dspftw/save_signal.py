# vim: expandtab tabstop=4 shiftwidth=4

from typing import Any, Tuple
import numpy as np

from .signal_types import FullSignalType
from .rounding import  Rounding
from .writemode import normalize_write_mode

def save_signal(file_name: str, sig: np.array, signal_type: str, number_space: str,
                endianness: str, write_mode: str='w', rounding: Any=0) -> Tuple[int, int]:
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
        Default is w.
    rounding:
        Rounding behavior for two's complement.
        '0' = True Zero (asymmetric), '1' = True One (symmetric)
        Default is 0.

    Returns a tuple of the number of samples written and the number of samples clipped.
    '''

    write_mode = normalize_write_mode(write_mode)
    full_signal_type = FullSignalType(signal_type, number_space, endianness,rounding)

    if len(sig) == 0:
        sig = np.array([])

    if full_signal_type.is_twos_compliment_signal_type():

        if full_signal_type.is_complex():
            # Flatten complex signals to real
            sigflat = np.array([sig.real,sig.imag]).flatten("F")
        else:
            sigflat = np.array(sig).real

        if rounding == Rounding.TRUEZERO.value:
            # Shift number line up
            sigflat += 1 / (2.0*full_signal_type.scale())
        # if self.rounding == Rounding.TRUEONE:
            # sigflat = sigflat # No change

        # Put values from [-1,1) in interval [-2**R/2,2**R/2) and clip others
        # R = two's complement number (e.g. for 8t, R=8)
        sigout, num_clipped = full_signal_type.clip_real_signal(sigflat)
        # Round down to nearest integer
        sigout = np.array(np.floor(sigout), 'int')

        # Modulo 2^8 or 2^16 to create two's complement
        sigout = np.remainder(sigout, 2*full_signal_type.scale())
        # Cast sample as the desired data type
        sigout = np.array(sigout, full_signal_type.numpy_dtype())

    else:
        num_clipped = 0

        if full_signal_type.is_complex():
            # Flatten and cast sample as the desired data type
            sigout = np.array([sig.real,sig.imag],
                              full_signal_type.numpy_dtype()).flatten("F")
        else:
            # Cast sample as the desired data type
            sigout = np.array(sig.real, full_signal_type.numpy_dtype())

    with open(file_name, write_mode.value) as outfile:
        sigout.tofile(outfile)

    num_written = len(sigout) // full_signal_type.items_per_sample()

    return num_written, num_clipped

def savesig(*args, **kwargs):
    '''
    Alias for save_signal.
    '''
    return save_signal(*args, **kwargs)
