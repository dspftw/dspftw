# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum

from .exceptions import EndiannessException

class Endianness(Enum):
    BIG = '>'
    LITTLE = '<'

def normalize_endianness(endianness: str) -> Endianness:
    endianness = endianness.strip().lower()

    if endianness in ('l', 'little'):
        return Endianness.LITTLE

    if endianness in ('b', 'big'):
        return Endianness.BIG

    raise EndiannessException('Unknown endianness "{}"'.format(endianness))
