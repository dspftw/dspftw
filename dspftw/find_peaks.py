# vim: expandtab tabstop=4 shiftwidth=4
'''
Find indices of peaks
'''

from typing import Any
from numpy import array as nparray
from numpy import append, arange, argmax, copy, inf, ones, pad

def find_peaks(inarray: nparray, min_height: float=1, min_dist: int=20, num_peaks: Any=inf) -> nparray:
    '''
    Find indices of peak values in order of greatest value to least

    Parameters
    —————
    inarray:
        numpy.array containing real samples
    min_height: float
        threshold a value must exceed to be considered a peak
        Default: 1
    min_dist: int
        Minimum distance (in samples) allowed between peaks
        Default: 20
    num_peaks: int or numpy.inf
        Maximum number of peak indices to return
        Default: numpy.inf (Return all peaks)

    Returns at most num_peaks indices in a numpy array.
    '''

    # Output will be integer list of indices
    out = nparray([], dtype=int)

    # In case num_peaks <= 0 output emptry array
    if num_peaks <= 0:
        return out

    # Flatten array
    arr = copy(inarray).flatten()

    # Pad with 'min_dist' elements to both ends of 'arr'
    # Prevents possible error when overwriting array with "zero-ed" elements
    arr = pad(arr, (min_dist, min_dist), "constant", constant_values=(min_height-1, min_height-1))

    # Find index with maximum value
    midx = argmax(arr)
    while arr[midx] > min_height:
        # Append maximal index to output array
        out = append(out, midx-min_dist)
        # Check if we reached the maximum number of peaks
        if len(out) >= num_peaks:
            return out

        # "Zero" array values withing min_dist of maximal index
        arr[arange(midx-min_dist, midx+min_dist+1)] = ones(2*min_dist+1)*(min_height-1)

        # Find index with maximum value for next iteration
        midx = argmax(arr)

    return out


def findpeaks(*args, **kwargs):
    '''
	Alias for find_peaks.
	'''
    return find_peaks(*args, **kwargs)
