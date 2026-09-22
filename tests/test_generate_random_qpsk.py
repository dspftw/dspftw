# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
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
    def test_generate_random_qpsk_seed(self):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            samples_path = temp_path.joinpath('samples')
            symbols_path = temp_path.joinpath('symbols')

            dspftw.generate_random_qpsk(
                samples_path,
                symbols_path,
                num_symbols=20,
                seed=12345,
            )

            symbols = np.fromfile(symbols_path, dtype=np.int8)

            expected_symbols = np.array(
                [2, 0, 3, 1, 0, 3, 2, 2, 3, 1,
                 3, 1, 2, 2, 0, 0, 0, 2, 2, 3],
                dtype=np.int8,
            )

            np.testing.assert_array_equal(symbols, expected_symbols)
            num_symbol_differences = dspftw.test_qpsk_modulation(
                samples_path,
                symbols_path,
            )
            self.assertEqual(num_symbol_differences, 0)
