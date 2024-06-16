# vim expandtab tabstop=4 shiftwidth=4

from numpy import pi, sinc, sin, cos, arange, where, zeros
from numpy import ceil  # pylint: disable=no-name-in-module
from numpy import array as nparray

def raised_cosine_filter_generator(symbol_width: int, symbol_rate: float, sample_rate: float, beta: float=0.25) -> nparray:
    '''
    Compute the taps of a raised cosine (RC) filter.

    Parameters
    ----------
    symbol_width: int
        Number of bauds wide for the output filter.
        An odd integer will ensure the initial and filanl taps are at baud boundaries.
    symbol_rate: float
        Symbol rate in Hz.
    sample_rate: float
        Sample rate in Hz.
    beta: float
        Roll off factor. In the interval (0,1]
        Default is 0.25.

    Returns a numply float array.
    '''

    # Define threshold for zero
    zero_thresh = 10**-10

    # Samples per baud
    spb = sample_rate/symbol_rate

    # Create the input time values
    time_array = arange(-ceil((symbol_width/2.0)*spb),ceil((symbol_width/2.0)*spb+1),dtype=float)/sample_rate

    # Create the filter values
    if beta == 0:
        filter_val = sinc(time_array)
    else:
        filter_val = zeros(time_array.shape)

        # Non-zero denominator
        nzidx = where(abs(1-(2*beta*time_array)**2) >= zero_thresh)
        inval = time_array[nzidx]
        filter_val[nzidx] = sinc(inval)*cos(pi*beta*inval)/(1-(2*beta*inval)**2)

        # Zero denominator: Using l'Hopital's rule
        zidx = where(abs(1-(2*beta*time_array)**2) < zero_thresh)
        inval = time_array[zidx]
        filter_val[zidx] = sinc(inval)*pi*sin(pi*beta*inval)/(8*beta*inval)

    return filter_val

def rcfiltgen(*args, **kwargs) -> nparray:
    '''
    Alias for raised_cosine_filter_generator.
    '''
    return raised_cosine_filter_generator(*args, **kwargs)



