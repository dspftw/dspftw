'''
Generate QAM signal with the given samples per symbol,
modulated with the provided constellation and symbol indices.
The signal is generated using a root raised cosine
filter with given beta.
'''
import numpy as np
from numpy import array as nparray
from scipy.signal import fftconvolve
from .root_raised_cosine_filter_generator import root_raised_cosine_filter_generator

def generate_qam(symbol_indices: nparray,
                 constellation: nparray,
                 samples_per_sym: int=2,
                 beta: float=0.25) -> nparray:
    '''
    Parameters
    ----------
    symbol_indices:
        Symbol indices to be modulated.  Each index must be an integer at least 0
        and at most 1 less than the constellation size.
    constellation:
        Array of complex numbers describing the constellation points.
    samples_per_sym:
        Number of samples per symbol (Default 2).  Must be an integer at least 2.
    beta:
        Roll off factor (Default 0.25).  Must be a float between 0 and 1.

    Returns array of len(symbol_indices)*samples_per_sym complex samples.
    '''

    # Check Parameters
    # Symbol indices must be between 0 and length(constellation).
    if max(symbol_indices) < 0:
        print("generate_qam error: All symbol indices must be at least 0")
        return symbol_indices

    if max(symbol_indices) >= len(constellation):
        print("generate_qam error: All symbol indices must be less than"
        "the constellation size (",len(constellation),")")
        return symbol_indices

    # Constellation must have at least 2 points
    if len(constellation) < 2:
        print("generate_qam error: Constellation size (",len(constellation),
        ") must be at least 2.")
        return symbol_indices

    # If user provided sceale, then it must be nonnegative
    if beta < 0 or beta > 1:
        print("generate_qam error: Beta (",beta,") must be between 0 and 1.")
        return symbol_indices

    # Get to work

    # Create symbols from symbol indices
    symbols = constellation[symbol_indices]

    # Create pulse train
    pulse_train = np.kron(symbols, np.append([1], np.zeros(samples_per_sym-1)))

    # Create pulse shaping filter
    baud_width = 21
    pulse_shape = root_raised_cosine_filter_generator(baud_width,1,samples_per_sym,beta)

    # Return
    return fftconvolve(pulse_train, pulse_shape, mode="same")
