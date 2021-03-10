# vim: expandtab tabstop=4 shiftwidth=4

import numpy as np

def true_zero(sigflat: np.array) -> np.array:
    return np.array(np.round(sigflat), 'int')

def true_one(sigflat: np.array) -> np.array:
    return np.array(sigflat, 'int')
