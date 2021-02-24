# vim: expandtab tabstop=4 shiftwidth=4

from numpy import pi, sin, ceil, append, arange, zeros
from numpy import array as nparray

from .root_raised_cosine import root_raised_cosine

def root_raised_cosine_filter_generator(symbol_width: int, symbol_rate: float, sample_rate: float, beta: float=0.25) -> nparray:
    '''
    Compute the taps of a root raised cosine (RRC) filter.

    Parameters
    ----------
    symbol_width: int
        Number of bauds wide for the output filter.  An odd integer will ensure the initial and final taps are at baud boundaries.
    symbol_rate: float
        Symbol rate in Hz.
    sample_rate: float
        Sample rate in Hz.
    beta: float
        Roll off factor.  In the interval (0,1]
        Default is 0.25.

    Returns a numpy float array.
    '''

    # Set the symbol period
    Ts = 1.0/symbol_rate

    # Create the input time values
    time_array = arange(-ceil((symbol_width/2.0)*Ts*sample_rate), ceil((symbol_width/2.0)*Ts*sample_rate+1), dtype=float)/sample_rate

    # Create filter values
    if beta == 0:
        filter_val = zeros(time_array.shape)
        tlen = len(time_array)

        # Define filter everywhere except center tap
        idx = append(arange((tlen-1)//2, dtype=int), arange((tlen-1)//2+1, tlen, dtype=int))
        filter_val[idx] = sin(pi*time_array[idx]/Ts) / (pi*time_array[idx]/Ts)

        # Define filter at center tap
        filter_val[(tlen-1)//2] = 1

    else:
        filter_val = root_raised_cosine(time_array,Ts,beta)

    return filter_val

def rrcfiltgen(*args, **kwargs) -> nparray:
    '''
    Alias for root_raised_cosine_filter_generator.
    '''
    return root_raised_cosine_filter_generator(*args, **kwargs)
