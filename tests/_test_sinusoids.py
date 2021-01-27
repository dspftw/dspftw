# vim: expandtab tabstop=4 shiftwidth=4

import unittest

import numpy as np
import dspftw

class SinusoidTests(unittest.TestCase):
    def test_complex_sinusoid(self):
        def sinusoid(t): return dspftw.complex_sinusoid(A=5, f=10, t=t, phi=0)
        times = np.linspace(0, 10, num=10)
        signal = sinusoid(times)
        self.assertEqual(len(times), len(signal))
