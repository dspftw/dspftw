# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum, auto
from os.path import splitext
from re import compile as regex_compile
from typing import Any, Dict, Tuple

from numpy import array as nparray

from .exceptions import FileNameException
from .load_bits import load_bits
from .load_signal import load_signal

signal_filename_pattern = regex_compile(r'\.(?P<number_space>real|cplx)'
                                        r'\.(?P<sample_rate>([0-9]+(\.[0-9]+)?))'
                                        r'\.(?P<extension>8t|16t|16tl|16tr|32t|32tl|32tr|32f|32fl|32fr|64f|64fl|64fr)')

class FileType(Enum):
    SIGNAL = auto()
    BITS = auto()

def get_file_type(filename: str) -> FileType:
    _, extension = splitext(filename)

    if extension in ('.8t',
                     '.16t', '.16tl', '.16tr',
                     '.32t', '.32tl', '.32tr',
                     '.32f', '.32fl', '.32fr',
                     '.64f', '.64fl', '.64fr'):
        return FileType.SIGNAL

    if extension == '.bits':
        return FileType.BITS

    raise FileNameException('Could not determine file type by extension {}'.format(extension))

def get_number_space(filename: str) -> str:
    if '.cplx.' in filename:
        return 'cplx'

    if '.real.' in filename:
        return 'real'

    raise FileNameException('Could not determine if file is real or complex based on filename {}'.format(filename))

def get_endianness(filename: str) -> str:
    _, extension = splitext(filename)

    if extension.endswith('l') or extension.endswith('r'):
        return 'little'

    return 'big'

def get_sample_rate(filename: str) -> float:
    match = signal_filename_pattern.search(filename)

    try:
        return float(match.group('sample_rate'))

    except AttributeError as ex:
        raise FileNameException('Could not determine sample rate from filename {}'.format(filename)) from ex

def get_extension(filename: str) -> str:
    _, extension = splitext(filename)
    return extension[1:]  # remove leading dot

def filename_load_signal(filename: str, count: int, offset: int) -> Tuple[nparray, Dict[str, Any]]:
    signal = load_signal(filename,
                         get_extension(filename),
                         get_number_space(filename),
                         endianness=get_endianness(filename),
                         num_samples=count,
                         start_sample=offset)

    metadata = {
        'filename': filename,
        'sample_rate': get_sample_rate(filename),
    }

    return signal, metadata

def filename_load_bits(filename: str, count: int, offset: int) -> Tuple[nparray, Dict[str, Any]]:
    bits = load_bits(filename, count=count, offset=offset)

    metadata = {
        'filename': filename,
    }

    return bits, metadata

def filename_load(filename: str, count: int=-1, offset: int=0) -> Tuple[nparray, Dict[str, Any]]:
    '''
    Automatically loads a file based on the information in its filename.

    Parameters
    ----------
    filename:
        The file name to load.
    count:
        The number of items to load once the type is determined.
    offset:
        Number of items to skip once the type is determined.

    Returns a numpy array and a metadata dictionary.
    '''
    filename = str(filename)  # in case we get a pathlib.Path
    file_type = get_file_type(filename)

    if file_type == FileType.SIGNAL:
        return filename_load_signal(filename, count, offset)

    if file_type == FileType.BITS:
        return filename_load_bits(filename, count, offset)

    raise FileNameException('Could not determine how to load {}'.format(filename))

def fnload(*args, **kwargs) -> nparray:
    '''
    Alias for filename_load.
    '''
    return filename_load(*args, **kwargs)
