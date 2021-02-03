# vim: expandtab tabstop=4 shiftwidth=4

from numpy import array as nparray
from numpy import fromfile

from .data_types import FullDataType

def load_signal(file_name: str, data_type: str, endianness: str, number_space: str, num_samples: int=0, start_sample: int=0) -> nparray:
    full_data_type = FullDataType(data_type, endianness, number_space)
    data = fromfile(file_name,
                    dtype=full_data_type.numpy_dtype(),
                    offset=full_data_type.offset(start_sample),
                    count=full_data_type.count(num_samples))
    return full_data_type.post_load(data)

def loadsig(*args, **kwargs) -> nparray:
    return load_signal(*args, **kwargs)
