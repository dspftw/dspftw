# vim: expandtab tabstop=4 shiftwidth=4

''' Cross-Correlation with normalization
'''

from numpy import array as nparray
from numpy import absolute, arange, asarray, bool_, complex128
from numpy import conjugate, cumsum, divide, empty, int64
from numpy import maximum, minimum, ones, sqrt, zeros
from scipy.signal import convolve, correlate
from scipy.fft import fft, ifft, next_fast_len

from .exceptions import DSPFTWException

BLOCK_DEFAULT = 2**22
BLOCK_SIZE_DEFAULT = 2**16

def _correlate_blocked_full(signal, pattern, block):
    """Compute full correlation using overlap-save FFT blocks."""

    n_signal = len(signal)
    n_pattern = len(pattern)

    # Each FFT processes 'block' new samples plus overlap.
    overlap = n_pattern - 1
    fft_length = next_fast_len(block + overlap)

    # Correlation is convolution with the conjugated,
    # time-reversed reference pattern.
    kernel = conjugate(pattern[::-1]).astype(complex128)
    kernel_fft = fft(kernel, n=fft_length)

    # Full correlation is convolution with zero padding
    # at both ends of the input signal.
    output_length = n_signal + overlap
    output = empty(output_length, dtype=complex128)

    previous = zeros(overlap, dtype=complex128)

    for start in range(0, output_length, block):
        count = min(block, output_length - start)

        # Construct only the current FFT input block.
        segment = zeros(fft_length, dtype=complex128)

        if overlap:
            segment[:overlap] = previous

        end = min(start + count, n_signal)

        if start < n_signal:
            segment[overlap:overlap + end - start] = signal[start:end]

        # Retain the last overlap samples for the next block.
        if overlap:
            previous[:] = segment[count:count + overlap]

        spectrum = fft(segment)
        spectrum *= kernel_fft

        result = ifft(spectrum)

        # Discard the corrupted overlap-save samples.
        output[start:start + count] = result[
            overlap:overlap + count
        ]

    return output


def _normalize_blocked_full(output, signal, pattern, block):
    """Normalize correlation using blockwise convolution with ones."""

    n_signal = len(signal)
    n_pattern = len(pattern)
    overlap = n_pattern - 1

    # Match the original convolution-based normalization.
    pattern_energy = (absolute(
        pattern.astype(complex128)) ** 2).sum()
    pattern_power = sqrt(pattern_energy)

    if pattern_power == 0:
        output[:] = 0
        return output

    for start in range(0, len(output), block):
        count = min(block, len(output) - start)

        # Output index 'start' corresponds to a convolution
        # window beginning at signal index start - overlap.
        first = max(0, start - overlap)
        last = min(n_signal, start + count)

        segment = signal[first:last]

        # Convert only this segment to double precision.
        power = absolute(segment.astype(complex128)) ** 2

        # Convolution with ones gives the window energy.
        energy = convolve(
            power,
            ones(n_pattern),
            mode='full',
            method='fft',
        )

        # Align the local convolution with global output indices.
        offset = start - first
        window_energy = energy[offset:offset + count]

        maximum(window_energy, 0, out=window_energy)
        sqrt(window_energy, out=window_energy)
        window_energy *= pattern_power

        # Identify windows containing actual nonzero signal samples.
        # Count nonzero samples in each convolution window.
        active_samples = power > 0

        counts = empty(len(active_samples) + 1, dtype=int64)
        counts[0] = 0
        cumsum(active_samples, dtype=int64, out=counts[1:])

        indices = offset + arange(count)
        left = maximum(indices - n_pattern + 1, 0)
        right = minimum(indices + 1, len(active_samples))

        active_count = counts[right] - counts[left]

        nonzero = (active_count > 0) & (window_energy > 0)
        output_block = output[start:start + count]
        output_block[~nonzero] = 0
        output_block[nonzero] /= window_energy[nonzero]

    return output


def signal_correlation(in1: nparray, in2: nparray, norm=True,
                       mode='full', method='auto', block=None) -> nparray:
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
    block : int or None, optional
        Number of new input samples processed per FFT block.

        None (default):
            Automatically selects the processing method.
            Signals with at most 2**22 samples use the
            original scipy correlation implementation.
            Larger signals use overlap-save FFT processing
            with a default block size of 2**16 samples.

        0:
            Forces the original scipy implementation.

        Positive integer:
            Forces overlap-save FFT processing using the
            specified block size.

        Blocked processing reduces peak memory usage for
        large signals. The FFT block length is chosen
        automatically to accommodate the reference signal.

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
    if block is not None:
        if isinstance(block, (bool, bool_)) or not isinstance(block, int):
            raise DSPFTWException('block must be a nonnegative integer or None')
        if block < 0:
            raise DSPFTWException('block must be a nonnegative integer or None')
    if block is None:
        if len(arr_l) > BLOCK_DEFAULT:
            block = BLOCK_SIZE_DEFAULT
        else:
            block = 0

    # If norm is set to False, unnormalized output will be returned
    if block is not None and block > 0:
        out_arr = _correlate_blocked_full(arr_l, arr_s, block)

        if norm:
            _normalize_blocked_full(out_arr, arr_l, arr_s, block)

        if mode == 'same':
            start = (len(arr_s) - 1) // 2
            out_arr = out_arr[start:start + len(arr_l)]

        elif mode == 'valid':
            start = len(arr_s) - 1
            out_arr = out_arr[start:start + len(arr_l) - len(arr_s) + 1]
    else:
        out_arr = correlate(arr_l, arr_s, mode=mode, method=method)
    # Default output is set to normalized
    if norm and (block is None or block == 0):
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
