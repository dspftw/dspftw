# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum, auto

from numpy import array as nparray

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

def scale_data(data_type: DataType, data: nparray) -> nparray:
    if data_type == DataType.DT8T:
        return data / (2**7)

    if data_type == DataType.DT16T:
        return data / (2**15)

    if data_type == DataType.DT32T:
        return data / (2**31)

    return data

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

    def numpy_dtype(self) -> str:
        if self.data_type == DataType.DT8T:
            return 'b'

        if self.data_type == DataType.DT16T and self.endianness == Endianness.LITTLE:
            return '<i2'

        if self.data_type == DataType.DT16T and self.endianness == Endianness.BIG:
            return '>i2'

        if self.data_type == DataType.DT32T and self.endianness == Endianness.LITTLE:
            return '<i4'

        if self.data_type == DataType.DT32T and self.endianness == Endianness.BIG:
            return '>i4'

        if self.data_type == DataType.DT32F and self.endianness == Endianness.LITTLE:
            return '<f4'

        if self.data_type == DataType.DT32F and self.endianness == Endianness.BIG:
            return '>f4'

        if self.data_type == DataType.DT64F and self.endianness == Endianness.LITTLE:
            return '<f8'

        if self.data_type == DataType.DT64F and self.endianness == Endianness.BIG:
            return '>f8'

        raise DataTypeException('Could not determine numpy dtype')

    def count(self, count) -> int:
        if self.number_space == NumberSpace.REAL:
            return count

        if self.number_space == NumberSpace.COMPLEX:
            return count * 2

        raise DataTypeException('Could not determine count')

    def offset(self, offset) -> int:
        if self.number_space == NumberSpace.REAL:
            return offset

        if self.number_space == NumberSpace.COMPLEX:
            return offset * 2

        raise DataTypeException('Could not determine offset')

    def post_load(self, data: nparray) -> nparray:
        scaled_data = scale_data(self.data_type, data)

        if self.number_space == NumberSpace.REAL:
            return scaled_data

        if self.number_space == NumberSpace.COMPLEX:
            return scaled_data[0::2] + scaled_data[1::2]*1j

        raise DataTypeException('Could not perform post_load')
