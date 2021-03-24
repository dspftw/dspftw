# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum, auto
from typing import Tuple

import numpy as np

from .endianness import Endianness, normalize_endianness
from .exceptions import NumberSpaceException, SignalTypeException

class SignalType(Enum):
    ST8T  = 'b'
    ST16T = 'i2'
    ST32T = 'i4'
    ST32F = 'f4'
    ST64F = 'f8'

class NumberSpace(Enum):
    REAL = auto()
    COMPLEX = auto()

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
        return self.endianness.value + self.signal_type.value

    def count(self, count: int) -> int:
        if count == -1:
            return -1

        return count * self.items_per_sample()

    def offset(self, offset: int) -> int:
        return offset * self.items_per_sample()

    def post_load(self, data: np.array) -> np.array:
        scaled_signal = data / self.scale()

        if self.is_complex():
            return scaled_signal[0::2] + scaled_signal[1::2]*1j

        return scaled_signal

    def clip_signal(self, signal: np.array) -> Tuple[np.array, int]:
        mult = self.scale()

        if self.is_complex():
            sigflat = np.array([mult*signal.real, mult*signal.imag]).flatten('F')
        else:
            sigflat = np.copy(mult*signal)

        # Count how many will be clipped below
        clip_count = len(np.argwhere(sigflat < -1*mult).flatten())
        # Clipping values that are too low
        sigflat = np.where(sigflat < -1*mult, -1*mult, sigflat)

        # Count how many will be clipped above
        clip_count += len(np.argwhere(sigflat>=mult).flatten())
        # Clipping values that are too high
        sigflat = np.where(sigflat >= mult, mult-1, sigflat)

        return sigflat, clip_count

    def is_complex(self) -> bool:
        if self.number_space == NumberSpace.COMPLEX:
            return True

        return False

    def is_twos_compliment_signal_type(self) -> bool:
        if self.signal_type in (SignalType.ST8T, SignalType.ST16T, SignalType.ST32T):
            return True

        return False

    def scale(self) -> int:
        if self.signal_type == SignalType.ST8T:
            return 2**7

        if self.signal_type == SignalType.ST16T:
            return 2**15

        if self.signal_type == SignalType.ST32T:
            return 2**31

        return 1

    def items_per_sample(self):
        if self.is_complex():
            return 2

        return 1
