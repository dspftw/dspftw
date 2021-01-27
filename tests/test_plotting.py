# vim: expandtab tabstop=4 shiftwidth=4

import unittest

import numpy as np
import dspftw

class PlottingTests(unittest.TestCase):
    def test_plot_complex(self):
        complex_data = np.array([1+0j, 0+1j, -1+0j, 0-1j])
        fig = dspftw.plot_complex(complex_data)
        self.assertNotEqual(fig, None)

    def test_plot_signal(self):
        def my_sinusoid(t): return dspftw.complex_sinusoid(A=5, f=5, t=t, phi=0)

        times = np.linspace(0, 1, num=25)
        my_signal = my_sinusoid(times)

        fig = dspftw.plot_signal(my_signal, times)
        self.assertNotEqual(fig, None)
