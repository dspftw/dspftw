# vim: expandtab tabstop=4 shiftwidth=4

import unittest

import numpy as np
import dspftw

class PlottingTests(unittest.TestCase):
    def test_plot_signal(self):
        def my_sinusoid(t): return dspftw.complex_sinusoid(A=5, f=5, t=t, phi=0)

        times = np.linspace(0, 1, num=25)
        my_signal = my_sinusoid(times)

        fig = dspftw.plot_signal(my_signal, times)
        self.assertNotEqual(fig, None)
