# vim: expandtab tabstop=4 shiftwidth=4

from enum import Enum
from typing import Any

from .exceptions import RoundingException
from .truncation import true_zero, true_one

class Rounding(Enum):
    TRUEZERO = 0
    TRUEONE = 1

def normalize_rounding(rounding: Any) -> Rounding:

    if isinstance(rounding,int):
        if rounding == 0:
            return Rounding.TRUEZERO
        if rounding == 1:
            return Rounding.TRUEONE

    if isinstance(rounding,str):
        if rounding in ('0', 'zero'):
            return Rounding.TRUEZERO
        if rounding in ('1', 'one'):
            return Rounding.TRUEONE

    if rounding is true_zero:
        return Rounding.TRUEZERO
    if rounding is true_one:
        return Rounding.TRUEONE

    raise RoundingException(f"Unknown rounding {rounding}")

