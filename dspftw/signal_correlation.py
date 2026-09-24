# vim: expandtab tabstop=4 shiftwidth=4

''' Cross-Correlation with normalization
'''

from numpy import array as nparray
from numpy import absolute, asarray, divide, maximum, ones, sqrt
from numpy import bool_
from scipy.signal import convolve, correlate
from .exceptions import DSPFTWException


def signal_correlation(in1: nparray, in2: nparray, norm=True, mode='full', method='auto') -> nparray:
    '''
    Cross-correlates two arrays and normalizes the output

    Parameters
    ----------
    in1:
        numpy.array containing signal being searched
    in2:
        numpy.array containing reference/template signal
    norm: bool
        Flag to normalize the output.
        Default is True
        When normalized, the full energy of the reference signal is used at
        all lags. Partial reference overlaps are therefore penalized.
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
    '''

    # Long signal
    arr_l = asarray(in1)
    # Short signal
    arr_s = asarray(in2)

    # Check parameters
    if arr_l.ndim != 1 or arr_s.ndim != 1:
        raise DSPFTWException('in1 and in2 must be one-dimensional')

    if len(arr_l) == 0 or len(arr_s) == 0:
        raise DSPFTWException('in1 and in2 must not be empty')

    if len(arr_l) < len(arr_s):
        raise DSPFTWException('in1 must be at least as long as in2')

    if not isinstance(norm, (bool, bool_)):
        raise DSPFTWException('norm must be a boolean')

    if mode not in ('full', 'same', 'valid'):
        raise DSPFTWException("mode must be 'full', 'same', or 'valid'")

    if method not in ('auto', 'direct', 'fft'):
        raise DSPFTWException("method must be 'auto', 'direct', or 'fft'")

    # If norm is set to False, unnormalized output will be returned
    out_arr = correlate(arr_l, arr_s, mode=mode, method=method)
    # Default output is set to normalized
    if norm:
        s_pow = sqrt((absolute(arr_s)**2).sum())
        # Calculate sliding energy of long signal
        l_pow = convolve(
            absolute(arr_l)**2,
            ones(len(arr_s)),
            mode=mode,
            method=method,
        )
        # Protect against potential negative from FFT floating-point roundoff
        maximum(l_pow, 0, out=l_pow)
        # Convert sliding energy to norm
        sqrt(l_pow, out=l_pow)
        l_pow *= s_pow
        iszero = l_pow == 0
        divide(out_arr, l_pow, out=out_arr, where=~iszero)
        out_arr[iszero] = 0
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
