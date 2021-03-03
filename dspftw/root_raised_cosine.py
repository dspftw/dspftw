# vim: expandtab tabstop=4 shiftwidth=4

from numpy import pi, sin, cos, where, zeros
from numpy import array as nparray

def root_raised_cosine(time_array: nparray, Ts: float, beta: float=0.25) -> nparray:
    '''
    Compute the values of the root raised cosine function at points in time_array.

    Parameters
    ----------
    time_array: nparray
        Input time values.
    Ts: float
        Symbol period in seconds.  Reciprocal of the symbol rate.
    beta: float
        Roll off factor.  In the interval (0,1]
        Default is 0.25.

    Returns a numpy float array.
    '''

    # Define threshhold for zero
    zr = 10**-10

    # Create output array
    func_val = zeros(len(time_array))

    # Initial denominator values
    denominator = pi*time_array/Ts*(1-16*(beta**2)*(time_array**2)/(Ts**2))

    # Compute output at points where denominator1 is not zero
    nzidx = where(abs(denominator) >= zr)
    numerator1 = (sin(pi*time_array[nzidx]/Ts*(1-beta)) + 4*beta*time_array[nzidx]/Ts*cos(pi*time_array[nzidx]/Ts*(1+beta)))
    denominator1 = denominator[nzidx]
    func_val[nzidx] = numerator1/denominator1

    # Compute output at points where denominator1 is zero
    zidx = where(abs(denominator) < zr)
    numerator2 = pi*(1-beta)*cos(pi*time_array[zidx]*(1-beta)/Ts)/Ts + 4*beta*cos(pi*time_array[zidx]*(1+beta)/Ts)/Ts - 4*pi*time_array[zidx]*beta*(1+beta)*sin(pi*time_array[zidx]*(1+beta)/Ts)/(Ts**2)
    denominator2 = pi*((Ts**2)-48*(time_array[zidx]**2)*(beta**2))/(Ts**3)
    func_val[zidx] = numerator2/denominator2

    return func_val

def rrcfunct(*args, **kwargs) -> nparray:
    '''
    Alias for root_raised_cosine.
    '''
    return root_raised_cosine(*args, **kwargs)
