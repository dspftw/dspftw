# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from tempfile import TemporaryDirectory

import unittest

from numpy import linspace

import dspftw

class SaveLoadSignalTests(unittest.TestCase):
    def try_save_load(self, signal, signal_type, endianness, offset):
        with TemporaryDirectory() as tempdir:
            temp_path = Path(tempdir)
            file_path = temp_path.joinpath('signal_file')

            num_written, _ = dspftw.save_signal(str(file_path), signal, signal_type, 'cplx', endianness)
            self.assertEqual(num_written, len(signal))

            loaded_signal = dspftw.load_signal(str(file_path), signal_type, 'cplx', endianness, start_sample=offset)

            for i in range(len(loaded_signal)):
                self.assertAlmostEqual(loaded_signal[i].real, signal[i+offset].real, places=1)
                self.assertAlmostEqual(loaded_signal[i].imag, signal[i+offset].imag, places=1)

    def test_save_load(self):
        signal = dspftw.complex_sinusoid(A=1, f=10, t=linspace(1, 10, num=10), phi=0)
        signal_types = ('8t', '16t', '32t', '32f', '64f')
        endiannesses = ('little', 'big')
        offsets = (0, 1, 5)

        for signal_type in signal_types:
            for endianness in endiannesses:
                for offset in offsets:
                    self.try_save_load(signal, signal_type, endianness, offset)
