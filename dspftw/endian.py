# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum

class Endian(Enum):
    BIG = 0
    LITTLE = 1

little_endian = Endian.LITTLE
big_endian = Endian.BIG
