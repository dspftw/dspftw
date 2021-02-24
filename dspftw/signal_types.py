# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum, auto

from numpy import array as nparray

from .endianness import Endianness, normalize_endianness
from .exceptions import NumberSpaceException, SignalTypeException

class SignalType(Enum):
    ST8T = auto()
    ST16T = auto()
    ST32T = auto()
    ST32F = auto()
    ST64F = auto()

class NumberSpace(Enum):
    REAL = auto()
    COMPLEX = auto()

def scale_signal(signal_type: SignalType, data: nparray) -> nparray:
    if signal_type == SignalType.ST8T:
        return data / (2**7)

    if signal_type == SignalType.ST16T:
        return data / (2**15)

    if signal_type == SignalType.ST32T:
        return data / (2**31)

    return data

def normalize_signal_type(signal_type: str) -> SignalType:
    signal_type = signal_type.strip().lower()

    if signal_type == '8t':
        return SignalType.ST8T

    if signal_type in ('16t', '16tl', '16tr'):
        return SignalType.ST16T

    if signal_type in ('32t', '32tl', '32tr'):
        return SignalType.ST32T

    if signal_type in ('32f', '32fl', '32fr'):
        return SignalType.ST32F

    if signal_type in ('64f', '64fl', '64fr'):
        return SignalType.ST64F

    raise SignalTypeException('Unknown signal type "{}"'.format(signal_type))

def normalize_number_space(number_space: str) -> NumberSpace:
    number_space = number_space.strip().lower()

    if number_space in ('c', 'cplx', 'complex'):
        return NumberSpace.COMPLEX

    if number_space in ('r', 'real'):
        return NumberSpace.REAL

    raise NumberSpaceException('Unknown number space "{}"'.format(number_space))

class FullSignalType:
    def __init__(self, signal_type: str, number_space: str, endianness: str) -> None:
        self.signal_type: SignalType = normalize_signal_type(signal_type)
        self.number_space: NumberSpace = normalize_number_space(number_space)
        self.endianness: Endianness = normalize_endianness(endianness)

    def numpy_dtype(self) -> str:
        if self.signal_type == SignalType.ST8T:
            return 'b'

        if self.signal_type == SignalType.ST16T and self.endianness == Endianness.LITTLE:
            return '<i2'

        if self.signal_type == SignalType.ST16T and self.endianness == Endianness.BIG:
            return '>i2'

        if self.signal_type == SignalType.ST32T and self.endianness == Endianness.LITTLE:
            return '<i4'

        if self.signal_type == SignalType.ST32T and self.endianness == Endianness.BIG:
            return '>i4'

        if self.signal_type == SignalType.ST32F and self.endianness == Endianness.LITTLE:
            return '<f4'

        if self.signal_type == SignalType.ST32F and self.endianness == Endianness.BIG:
            return '>f4'

        if self.signal_type == SignalType.ST64F and self.endianness == Endianness.LITTLE:
            return '<f8'

        if self.signal_type == SignalType.ST64F and self.endianness == Endianness.BIG:
            return '>f8'

        raise SignalTypeException('Could not determine numpy dtype')

    def count(self, count: int) -> int:
        if count == -1:
            return -1

        if self.number_space == NumberSpace.REAL:
            return count

        if self.number_space == NumberSpace.COMPLEX:
            return count * 2

        raise SignalTypeException('Could not determine count')

    def offset(self, offset: int) -> int:
        if self.number_space == NumberSpace.REAL:
            return offset

        if self.number_space == NumberSpace.COMPLEX:
            return offset * 2

        raise SignalTypeException('Could not determine offset')

    def post_load(self, data: nparray) -> nparray:
        scaled_signal = scale_signal(self.signal_type, data)

        if self.number_space == NumberSpace.REAL:
            return scaled_signal

        if self.number_space == NumberSpace.COMPLEX:
            return scaled_signal[0::2] + scaled_signal[1::2]*1j

        raise SignalTypeException('Could not perform post_load')
