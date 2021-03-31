'''
Reads QPSK signal file and associated symbol file, demodulates QPSK
to produce symbols and compares with symbols from symbol file
'''
import numpy as np
from scipy.signal import fftconvolve
from numpy import array as nparray
from numpy import exp, pi
from .load_signal import load_signal
from .load_data import load_data
from .root_raised_cosine_filter_generator import root_raised_cosine_filter_generator

def test_qpsk_modulation(ifile_samples: str,
                         ifile_symbols: str,
                         sample_type: str = "16t",
                         endianness: str = 'b',
                         num_symbols: int = 0,
                         samples_per_sym: int=2,
                         beta: float=0.25) -> nparray:
    '''
    Parameters
    ----------
    ifile_samples:
        Input file name for signal samples.
    ifile_symbols:
        Input file name for signal samples.
        Will read symbols as int8
    sample_type:
        The size and type of signal samples, such as '8t', '16t', '32t', '32f', '64f'.
        Default: 16t
    endianness:
        Endianness of the file, such as 'big', 'b', 'little', 'l'.
        Default: b
    num_symbols:
        Number of symbols to read.
        Will read 'num_symbols' symbols and num_symbols * samples_per_sym samples
        Default: 0 = read entire file
    samples_per_sym:
        Number of samples per symbol.  Must be an integer at least 2.
        Default: 2
    beta:
        Roll off factor.  Must be a float between 0 and 1.
        Default 0.25

    Returns number of symbol differences
    '''

    # Check Parameters
    # Must have a positive number of symbols to generate
    if num_symbols < 0:
        print("generate_random_qpsk error: num_symbols",num_symbols,"must be nonnegative.")
        return -1

    # Must have a positive number of samples per symbol
    if samples_per_sym <= 0:
        print("generate_random_qpsk error: samples_per_sym",samples_per_sym,"must be positive.")
        return -1

    # Test for valid sample type
    if sample_type not in ("8t", "16t", "32t", "32f", "64f"):
        print("generate_random_qpsk error: Sample type",sample_type," not one of"
        "8t, 16t, 32t, 32f, 64f")
        return -1

    # Test for valid endianness
    if endianness not in ("b", "big", "l", "little"):
        print("generate_random_qpsk error: Sample type",sample_type," not one of"
        "8t, 16t, 32t, 32f, 64f")
        return -1

    # Roll off factor must be between 0 and 1.
    if beta < 0 or beta > 1:
        print("generate_qam error: Beta (",beta,") must be between 0 and 1.")
        return -1

    # Load symbols and signal
    if num_symbols == 0:
        symbol_indices = load_data(ifile_symbols,"int8","b")
        signal = load_signal(ifile_samples,sample_type,"complex",endianness)
    else:
        symbol_indices = load_data(ifile_symbols,"int8","b",num_symbols)
        signal = load_signal(ifile_samples,sample_type,"complex",endianness,num_symbols*samples_per_sym)

    # QPSK constellation as a row vector
    constellation = [exp(2j*pi*np.arange(1,8,2)/8.0)]

    # Filter signal with root raised cosine filter to remove inter-symbol interference
    baud_width = 21
    rrc_filter = root_raised_cosine_filter_generator(baud_width,1,samples_per_sym,beta)
    signal_eq = fftconvolve(signal,rrc_filter,mode="same")

    # Decimate by 'samples_per_symto get complex symbols
    xys = signal_eq[0:samples_per_sym:]

    # Demodulate to get symbol indices
    demod_indices = np.argmin(abs(xys - np.transpose(constellation)),0).astype(int)

    # Compare symbol_indices and demod_indices
    if len(symbol_indices) != len(demod_indices):
        print("symbol_indices length",symbol_indices,"not equal to"
        " demod_indices",demod_indices)
        return -1

    diff_count = 0
    for idx in np.arange(0,len(symbol_indices)).astype(int):
        if symbol_indices[idx] != demod_indices[idx]:
            diff_count += 1

    # Return
    return diff_count
