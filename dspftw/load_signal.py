# vim: expandtab tabstop=4 shiftwidth=4

from sys import byteorder

from os.path import getsize
from typing import Any
from numpy import dtype as npdtype
from numpy import memmap
from numpy import array as nparray
from numpy import fromfile

from .signal_types import FullSignalType

def load_signal(  # pylint: disable=too-many-positional-arguments
    file_name: str,
    signal_type: str,
    number_space: str,
    endianness: str=byteorder,
    num_samples: int=-1,
    start_sample: int=0,
    rounding: Any=0,
    memory_map: bool = False,
    normalize: bool = True,
) -> nparray:
    '''
    Loads a signal from a file in float or two's compliment, real or complex format.

    Parameters
    ----------
    file_name:
        The name of the file to load.
    signal_type:
        The size and type of signal samples, such as '8t', '16t', '32t', '32f', '64f'.
    number_space:
        Number space of the file.  Valid values are 'real', 'r', 'complex', 'cplx', 'c'.
    endianness:
        Endianness of the file, such as 'big', 'b', 'little', 'l'.
        Defaults to the system endianness.
    num_samples:
        The number of samples to load from the file.
    start_sample:
        The number of samples to skip before loading.
    rounding:
        Twos-complement rounding: 0=Asymmetric/Exact Zero, 1=True One.
    memory_map : bool, optional
        If True, load samples using a copy-on-write NumPy memory map.
        The original file is not modified. Default is False.
    normalize : bool, optional
        If True, convert samples using the signal type's normal
        post-processing, including integer normalization.
        Default is True.

        If False, return raw, file-backed two's-complement integer
        samples. This requires memory_map=True and supports 8t,
        16t, and 32t signal types.

        Real integer signals return a one-dimensional array.
        Complex integer signals return an array of shape (N, 2),
        with I samples in column 0 and Q samples in column 1.

        Raw integer arrays preserve the file's integer dtype and
        byte order. No normalization or byte swapping is performed.
        The rounding parameter has no effect on raw samples.

    Returns a numpy array.
    When memory_map=True and normalize=False, returns raw
    two's-complement integers backed by a NumPy memory map.
    For complex signals, the returned array has shape (N, 2)
    rather than a complex floating-point dtype.
    '''
    full_signal_type = FullSignalType(signal_type, number_space, endianness, rounding)
    if not normalize:
        if not memory_map:
            raise ValueError(
                "normalize=False requires memory_map=True"
            )

        if not full_signal_type.is_twos_compliment_signal_type():
            raise ValueError(
                "normalize=False is supported only for "
                "two's-complement signal types"
            )
    dtype = full_signal_type.numpy_dtype()
    offset = full_signal_type.offset(start_sample)
    count = full_signal_type.count(num_samples)

    if offset > getsize(file_name):
        count = 0
        offset = 0

    if memory_map:
        # Copy-on-write: changes to the array never modify the file.
        itemsize = npdtype(dtype).itemsize
        available_bytes = max(0, getsize(file_name) - offset)
        available_items = available_bytes // itemsize

        if count == -1:
            count = available_items
        else:
            count = min(count, available_items)

        if count > 0:
            data = memmap(
                file_name,
                dtype=dtype,
                mode='c',
                offset=offset,
                shape=(count,),
            )
        else:
            # An empty selection cannot be memory-mapped.
            data = fromfile(
                file_name,
                dtype=dtype,
                offset=offset,
                count=0,
            )
    else:
        data = fromfile(
            file_name,
            dtype=dtype,
            offset=offset,
            count=count,
        )


    if not normalize:
        if full_signal_type.is_complex():
            if data.size % 2:
                raise ValueError("Incomplete complex I/Q sample")
            return data.reshape(-1, 2)

        return data

    # Preserve the original byte order for memory-mapped floats.
    # This avoids byte swapping and copying the mapped data.
    if memory_map and full_signal_type.scale() == 1:
        if full_signal_type.is_complex():
            if data.size % 2:
                raise ValueError("Incomplete complex I/Q sample")

            complex_dtype = npdtype(
                data.dtype.byteorder
                + ('c8' if data.dtype.itemsize == 4 else 'c16')
            )
            return data.view(complex_dtype)

        return data

    return full_signal_type.post_load(data)

def loadsig(*args, **kwargs) -> nparray:
    '''
    Alias for load_signal.
    '''
    return load_signal(*args, **kwargs)
