# vim: expandtab tabstop=4 shiftwidth=4

import unittest

import numpy as np
import dspftw

class PlottingTests(unittest.TestCase):
    def test_plot_complex(self):
        complex_data = np.array([1+0j, 0+1j, -1+0j, 0-1j])
        fig = dspftw.plot_complex(complex_data)
        self.assertNotEqual(fig, None)
