import numpy as np
from numpy import array as nparray
from numpy import exp, sin, cos, floor, ceil, pi, max, sqrt, log2, log10
from decimal_convert_to_base import *
from vector_power import *

def constellation_plot(constellation, binary_mode=0, scale=100):
    """
    Usage: [normalized_constellation] = constellation_plot(constellation, binary_mode, scale)
    Input:
    constellation - QAM constellation as a row ndarray vector of complex numbers
    binary_mode   - Mode for printing symbols: 0 = decimals (default), 1 = binary
    scale         - Character size (default 100)
    Output:
    normalized_constellation - Power normalized constellation
    """

    # Ensure constellation is a 1-dimensional complex array
    con = constellation.flatten().astype(complex)
    # Constellation size
    M = len(con)

    # Check Parameters
    # Constellations must contain at least 1 element
    if (M < 1):
        print("constellation_plot error: Constellation size (",M,") must be at least 1.")
        return constellation

    # If user provided mode, then it must be 0 or 1
    if ( (binary_mode != 0) and (binary_mode != 1) ):
        print("constellation_plot error: User input mode (",mode,") must be either 0 or 1.")
        return constellation

    # If user provided sceale, then it must be nonnegative
    if (scale < 0):
        print("constellation_plot error: User input scale (",scale,") must be nonnegative.")
        return constellation

    # Import plot capabilities
    from matplotlib import pyplot as plt

    # Number of bits per symbol
    bps = ceil(log2(M)).astype(int)

    # Plotting logic
    plt.suptitle("Scatterplot of {0}-point constellation".format(M))
    for k in np.arange(0,M):
        # Determine plot scale
        if (binary_mode == 0): # Decimal Mode
            # Number of decimal digits in k
            if (k == 0):
                ndigit = 1
            else:
                ndigit = floor(log10(k))+1
            size = scale*ndigit
            txt = "${0}$".format(k)
        elif (binary_mode == 1): # Binary Mode
            size = scale*bps
            tmp = decimal_convert_to_base(k,2,bps).flatten()
            # Convert binary array to string
            txt = "$"
            for idx in np.arange(0,bps):
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
