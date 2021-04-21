# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from tempfile import TemporaryDirectory

import unittest
import dspftw

class GenerateRandomQPSKTests(unittest.TestCase):
    def test_generate_random_qpsk(self):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            samples_path = temp_path.joinpath('samples')
            symbols_path = temp_path.joinpath('symbols')
            num_samples = dspftw.generate_random_qpsk(samples_path, symbols_path)
            self.assertTrue(num_samples > 0)
            num_symbol_differences = dspftw.test_qpsk_modulation(samples_path, symbols_path)
            self.assertEqual(num_symbol_differences, 0)
