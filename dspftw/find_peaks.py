# vim: expandtab tabstop=4 shiftwidth=4
'''
Find indices of peaks
'''
from typing import Any
from numpy import array as nparray
from numpy import argsort, asarray, flatnonzero, inf, zeros
from numpy import lexsort

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

    # Flatten without copying unless necessary.
    arr = asarray(inarray).ravel()
    n = arr.size

    out = []
    if num_peaks <= 0 or n == 0:
        return nparray(out, dtype=int)

    # Select all samples strictly above the threshold.
    cand = flatnonzero(arr > min_height)
    if cand.size == 0:
        return nparray(out, dtype=int)

    # Strongest first; stable sorting preserves lowest-index
    # priority when sample values are equal.
    if arr.dtype.kind in 'iu':
        sort_values = ~arr[cand]
    else:
        sort_values = -arr[cand]

    order = lexsort((cand, sort_values))
    cand = cand[order]

    # Suppress samples within min_dist of each selected peak.
    suppressed = zeros(n, dtype=bool)

    for idx in cand:
        if suppressed[idx]:
            continue

        out.append(int(idx))

        if len(out) >= num_peaks:
            break

        lo = max(0, idx - min_dist)
        hi = min(n, idx + min_dist + 1)
        suppressed[lo:hi] = True

    return nparray(out, dtype=int)


def findpeaks(*args, **kwargs):
    '''
	Alias for find_peaks.
	'''
    return find_peaks(*args, **kwargs)
