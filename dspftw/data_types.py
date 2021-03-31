# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum

from .endianness import Endianness, normalize_endianness
from .exceptions import DataTypeException

class DataType(Enum):
    U8   = 'u1'
    U16  = 'u2'
    U32  = 'u4'
    U64  = 'u8'
    I8   = 'i1'
    I16  = 'i2'
    I32  = 'i4'
    I64  = 'i8'
    F32  = 'f4'
    F64  = 'f8'
    F128 = 'f16'

def normalize_data_type(data_type: str) -> DataType:
    data_type = data_type.strip().lower()

    if data_type in ('u8', 'uint8'):
        return DataType.U8

    if data_type in ('u16', 'uint16'):
        return DataType.U16

    if data_type in ('u32', 'uint32'):
        return DataType.U32

    if data_type in ('u64', 'uint64'):
        return DataType.U64

    if data_type in ('i8', 'int8'):
        return DataType.I8

    if data_type in ('i16', 'int16'):
        return DataType.I16

    if data_type in ('i32', 'int32'):
        return DataType.I32

    if data_type in ('i64', 'int64'):
        return DataType.I64

    if data_type in ('f32', 'float32'):
        return DataType.F32

    if data_type in ('f64', 'float64'):
        return DataType.F64

    if data_type in ('f128', 'float128'):
        return DataType.F128

    raise DataTypeException('Unknown data type {}'.format(data_type))

class FullDataType:
    def __init__(self, data_type: str, endianness: str) -> None:
        self.data_type: DataType = normalize_data_type(data_type)
        self.endianness: Endianness = normalize_endianness(endianness)

    def numpy_dtype(self) -> str:
        return self.endianness.value + self.data_type.value
