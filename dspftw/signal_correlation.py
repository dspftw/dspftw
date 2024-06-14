# vim: expandtab tabstop=4 shiftwidth=4

''' Cross-Correlation with normalization set to default
'''

from scipy.signal import convolve, correlate

import numpy as np

def signal_correlation(in1: np.array, in2: np.array, norm=True):
    '''
    Cross-correlates two arrays and normalizes the output
    Parameters
    ----------
    in1: 
        numpy.array containing first signal
    in2:
        numpy.array containing second signal
    norm: bool
        flag to normalize the output.
        default is True

    Returns the correlation vector as a numpy array.
    '''

    arr_l = in1
    arr_s = in2
    # If norm is set to False, unnormalized output will be returned
    out_arr = correlate(arr_l, arr_s, mode='full')
    # Default output is set to normalized
    if norm:
        s_pow = np.sqrt(np.sum(arr_s*arr_s.conj()))
        l_pow = np.sqrt(convolve(arr_l*arr_l.conj(), np.ones(len(arr_s)), mode='full'))*s_pow
        out_arr = out_arr/l_pow
    return out_arr

def sigcorr(*args, **kwargs):
    '''
    Alias for signal_correlation.
    '''
    return signal_correlation(*args, **kwargs)
