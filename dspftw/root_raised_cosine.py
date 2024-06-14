# vim: expandtab tabstop=4 shiftwidth=4

from numpy import pi, sin, cos, where, zeros
from numpy import array as nparray

def root_raised_cosine(time_array: nparray, spd: float, beta: float=0.25) -> nparray:
    '''
    Compute the values of the root raised cosine function at points in time_array.

    Parameters
    ----------
    time_array: nparray
        Input time values.
    spd: float
        Symbol period in seconds.  Reciprocal of the symbol rate.
    beta: float
        Roll off factor.  In the interval (0,1]
        Default is 0.25.

    Returns a numpy float array.
    '''

    # Define threshhold for zero
    zero_thresh = 10**-10

    # Create output array
    func_val = zeros(len(time_array))

    # Initial denominator values
    denominator = pi*time_array/spd*(1-16*(beta**2)*(time_array**2)/(spd**2))

    # Compute output at points where denominator1 is not zero
    nzidx = where(abs(denominator) >= zero_thresh)
    vals=time_array[nzidx]
    numerator1 = (sin(pi*vals/spd*(1-beta)) + 4*beta*vals/spd*cos(pi*vals/spd*(1+beta)))
    denominator1 = denominator[nzidx]
    func_val[nzidx] = numerator1/denominator1

    # Compute output at points where denominator1 is zero
    zidx = where(abs(denominator) < zero_thresh)
    vals=time_array[zidx]
    numerator2 = pi*(1-beta)*cos(pi*vals*(1-beta)/spd)/spd + 4*beta*cos(pi*vals*(1+beta)/spd)/spd - 4*pi*vals*beta*(1+beta)*sin(pi*vals*(1+beta)/spd)/(spd**2)
    denominator2 = pi*((spd**2)-48*(vals**2)*(beta**2))/(spd**3)
    func_val[zidx] = numerator2/denominator2

    return func_val

def rrcfunct(*args, **kwargs) -> nparray:
    '''
    Alias for root_raised_cosine.
    '''
    return root_raised_cosine(*args, **kwargs)
