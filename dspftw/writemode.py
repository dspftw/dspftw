# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum

from .exceptions import WriteModeException

class WriteMode(Enum):
    WRITE = 'wb'
    APPEND = 'ab'

def normalize_write_mode(write_mode: str) -> WriteMode:
    write_mode = write_mode.strip().lower()

    if write_mode in ('w', 'write'):
        return WriteMode.WRITE

    if write_mode in ('a', 'append'):
        return WriteMode.APPEND

    raise WriteModeException(f"Unknown write mode {write_mode}")

