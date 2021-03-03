# vim: expandtab tabstop=4 shiftwidth=4

from numpy import array as nparray
from numpy import floor, ceil, sqrt, log2, log10, arange
from matplotlib import pyplot as plt

from .decimal_convert_to_base import decimal_convert_to_base
from .vector_power import vector_power

def constellation_plot(constellation: nparray, binary_mode: int=0, scale: int=100):
    """
    Plots symbol numbers at corresponding constellation points

    Parameters
    ----------
    constellation:
       QAM constellation as a row numpy array vector of complex numbers
    binary_mode:
       Mode for printing symbols: 0 = decimals (default), 1 = binary
    scale:
       Size of characters on plot (default 100)

    Returns power normalized constellation as a numpy array
    """

    # Ensure constellation is a 1-dimensional complex array
    con = constellation.flatten().astype(complex)
    # Constellation size
    con_size = len(con)

    # Check Parameters
    # Constellations must contain at least 1 element
    if con_size < 1:
        print("constellation_plot error: Constellation size (",con_size,") must be at least 1.")
        return constellation

    # If user provided mode, then it must be 0 or 1
#    if (binary_mode != 0) and (binary_mode != 1):
    if binary_mode not in (0,1):
        print("constellation_plot error: User input mode (",binary_mode,") must be either 0 or 1.")
        return constellation

    # If user provided sceale, then it must be nonnegative
    if scale < 0:
        print("constellation_plot error: User input scale (",scale,") must be nonnegative.")
        return constellation

    # Number of bits per symbol
    bps = ceil(log2(con_size)).astype(int)

    # Plotting logic
    plt.suptitle("Scatterplot of {0}-point constellation".format(con_size))
    for k in arange(0,con_size):
        # Determine plot scale
        if binary_mode == 0: # Decimal Mode
            # Number of decimal digits in k
            if k == 0:
                ndigit = 1
            else:
                ndigit = floor(log10(k))+1
            size = scale*ndigit
            txt = "${0}$".format(k)
        elif binary_mode == 1: # Binary Mode
            size = scale*bps
            tmp = decimal_convert_to_base(k,2,bps).flatten()
            # Convert binary array to string
            txt = "$"
            for idx in arange(0,bps):
                txt = "{0}{1}".format(txt,tmp[idx])
            txt = "{0}$".format(txt)
        plt.scatter(con[k].real,con[k].imag,s=size,marker=txt,c='k')
    plt.show()

    # Return power normalized constellation
    return (con/sqrt(vector_power(con))).flatten()

def conplot(*args, **kwargs) -> nparray:
    '''
    Alias for constellation_plot.
    '''
    return constellation_plot(*args, **kwargs)
