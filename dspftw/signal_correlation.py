# vim: expandtab tabstop=4 shiftwidth=4

# Cross-Correlation with normalization set to default

from scipy.signal import convolve, correlate

import numpy as np

def signal_correlation(in1, in2, norm=True):
    '''Cross-correlates two arrays and normalizes the output'''
    arrL = in1
    arrS = in2
    # If norm is set to False, unnormalized output will be returned
    outArr = correlate(arrL, arrS, mode='full')
    # Default output is set to normalized
    if norm:
        sPow = np.sqrt(np.sum(arrS*arrS.conj()))
        lPow = np.sqrt(convolve(arrL*arrL.conj(), np.ones(len(arrS)), mode='full'))*sPow
        outArr = outArr/lPow
    return outArr

def sigcorr(*args, **kwargs):
    '''
    Alias for signal_correlation.
    '''
    return signal_correlation(*args, **kwargs)
