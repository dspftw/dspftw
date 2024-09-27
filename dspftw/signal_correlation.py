# vim: expandtab tabstop=4 shiftwidth=4

''' Cross-Correlation with normalization
'''

from scipy.signal import convolve, correlate

import numpy as np

def signal_correlation(in1: np.array, in2: np.array, norm=True, mode='full', method='auto') -> np.array:
    '''
    Cross-correlates two arrays and normalizes the output

    Parameters
    ----------
    in1:
        numpy.array containing first signal
    in2:
        numpy.array containing second signal
    norm: bool
        Flag to normalize the output.
        Default is True
    mode: string
        Size of output. Options 'full', 'same', 'valid'
        Default is 'full'
        full:   Entire cross-correlation of inputs
        same:   Output is the same size at in1
        valid:  Only output values that do not depend on zero padding
    method: string
        Calculation method. Options 'auto', 'direct', 'fft'
        Default is 'auto'
        auto:   Automatically determine the best method
        direct: Use correlation definition
        fft:    Use Fast Fourier Transform for possibly faster computation

    Returns the correlation vector as a numpy array.
    Warning: Normalization does not check for division by 0 errors.
    '''

    arr_l = np.array(in1)
    arr_s = np.array(in2)
    # If norm is set to False, unnormalized output will be returned
    out_arr = correlate(arr_l, arr_s, mode=mode, method=method)
    # Default output is set to normalized
    if norm:
        s_pow = np.sqrt(np.sum(arr_s*arr_s.conj()))
        l_pow = np.sqrt(convolve(arr_l*arr_l.conj(), np.ones(len(arr_s)), mode=mode, method=method))*s_pow
        out_arr = out_arr/l_pow
    return out_arr

def sigcorr(*args, **kwargs):
    '''
    Alias for signal_correlation.
    '''
    return signal_correlation(*args, **kwargs)

def signal_correlate(*args, **kwargs):
    '''
    Alias for signal_correlation.
    '''
    return signal_correlation(*args, **kwargs)
