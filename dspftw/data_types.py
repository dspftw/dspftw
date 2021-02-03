# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum, auto

from .exceptions import DataTypeException

class DataType(Enum):
    DT8T = auto()
    DT16T = auto()
    DT32T = auto()
    DT32F = auto()
    DT64F = auto()

class Endianness(Enum):
    BIG = auto()
    LITTLE = auto()

class NumberSpace(Enum):
    REAL = auto()
    COMPLEX = auto()

def normalize_data_type(data_type: str) -> DataType:
    data_type = data_type.strip().lower()

    if data_type == '8t':
        return DataType.DT8T

    if data_type == '16t':
        return DataType.DT16T

    if data_type == '32t':
        return DataType.DT32T

    if data_type == '32f':
        return DataType.DT32F

    if data_type == '64f':
        return DataType.DT64F

    raise DataTypeException('Unknown data type "{}"'.format(data_type))

def normalize_endianness(endianness: str) -> Endianness:
    endianness = endianness.strip().lower()

    if endianness in ('l', 'little'):
        return Endianness.LITTLE

    if endianness in ('b', 'big'):
        return Endianness.BIG

    raise DataTypeException('Unknown endianness "{}"'.format(endianness))

def normalize_number_space(number_space: str) -> NumberSpace:
    number_space = number_space.strip().lower()

    if number_space in ('c', 'cplx', 'complex'):
        return NumberSpace.COMPLEX

    if number_space in ('r', 'real'):
        return NumberSpace.REAL

    raise DataTypeException('Unknown number space "{}"'.format(number_space))

class FullDataType:
    def __init__(self, data_type: str, endianness: str, number_space: str) -> None:
        self.data_type: DataType = normalize_data_type(data_type)
        self.endianness: Endianness = normalize_endianness(endianness)
        self.number_space: NumberSpace = normalize_number_space(number_space)
