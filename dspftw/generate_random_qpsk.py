'''
Generate QPSK signal from randomly generated symbols.
QPSK signal is complex basebanded and sampled at 'samples_per_sym'
samples per symbol.  The signal is generated using a root raised cosine
filter with given beta.
'''
import numpy as np
from numpy import array as nparray
from numpy import exp, pi
from .save_signal import save_signal
from .save_data import save_data
from .generate_qam import generate_qam

def generate_random_qpsk(ofile_samples: str,
                         ofile_symbols: str = "",
                         sample_type: str = "16t",
                         endianness: str = 'b',
                         num_symbols: int = 10000,
                         samples_per_sym: int=2,
                         beta: float=0.25) -> nparray:
    '''
    Parameters
    ----------
    ofile_samples:
        Output file name for signal samples.
        Number of samples = num_symbols * samples_per_sym
    ofile_symbols:
        Output file name for signal samples.
        Will write symbols as int8
        Number of bits = 2 * num_symbols
        Number of bytes = 2 * num_symbols / 8
        Default: Empty string, which means do not write symbols to file.
    sample_type:
        The size and type of signal samples, such as '8t', '16t', '32t', '32f', '64f'.
        Default: 16t
    endianness:
        Endianness of the file, such as 'big', 'b', 'little', 'l'.
        Default: b
    num_symbols:
        Number of symbols to generate.
    samples_per_sym:
        Number of samples per symbol.  Must be an integer at least 2.
        Default: 2
    beta:
        Roll off factor.  Must be a float between 0 and 1.
        Default 0.25

    Returns number of samples written to file.
    '''

    # Check Parameters
    # Must have a positive number of symbols to generate
    if num_symbols <= 0:
        print("generate_random_qpsk error: num_symbols",num_symbols,"must be positive.")
        return 0

    # Must have a positive number of samples per symbol
    if samples_per_sym <= 0:
        print("generate_random_qpsk error: samples_per_sym",samples_per_sym,"must be positive.")
        return 0

    # Test for valid sample type
    if sample_type not in ("8t", "16t", "32t", "32f", "64f"):
        print("generate_random_qpsk error: Sample type",sample_type," not one of"
        "8t, 16t, 32t, 32f, 64f")
        return 0

    # Test for valid endianness
    if endianness not in ("b", "big", "l", "little"):
        print("generate_random_qpsk error: Sample type",sample_type," not one of"
        "8t, 16t, 32t, 32f, 64f")
        return 0

    # Roll off factor must be between 0 and 1.
    if beta < 0 or beta > 1:
        print("generate_qam error: Beta (",beta,") must be between 0 and 1.")
        return 0

    # Generate random symbols
    symbol_indices = np.random.randint(0,2,num_symbols)

    # QPSK constellation
    constellation = exp(2j*pi*np.arange(1,8,2)/8.0)

    # Generate QPSK signal
    signal = generate_qam(symbol_indices,constellation,samples_per_sym,beta)

    # Write signal to file
    num_written = save_signal(ofile_samples, signal, sample_type, "complex", endianness)

    # Optionally write symbol indices to file
    if ofile_symbols:
        save_data(ofile_symbols, symbol_indices, "int8")

    # Return
    return num_written
