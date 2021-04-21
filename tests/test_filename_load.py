# vim: expandtab tabstop=4 shiftwidth=4

from numpy import array as nparray
from numpy import isnan, linspace
from pathlib import Path
from subprocess import getstatusoutput
from tempfile import TemporaryDirectory
from typing import Any, Dict, Tuple

import os
import unittest

import dspftw

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

def has_nan(signal: nparray) -> bool:
    return any(isnan(signal))

def suffix(signal_type: str, endianness: str) -> str:
    if signal_type == '8t':
        return '8t'

    if endianness in ('little', 'l'):
        return signal_type+'l'

    return signal_type

class FilenameLoadTests(unittest.TestCase):
    def try_save_filename_load(self, signal, signal_type, endianness):
        with TemporaryDirectory() as tempdir:
            temp_path = Path(tempdir)
            file_path = temp_path.joinpath('test_file.cplx.0.'+suffix(signal_type, endianness))
            num_written, _ = dspftw.save_signal(str(file_path), signal, signal_type, 'cplx', endianness)
            self.assertEqual(num_written, len(signal))
            loaded_signal, metadata = dspftw.filename_load(file_path)

            self.assertEqual(metadata['sample_rate'], 0.0)
            self.assertFalse(has_nan(loaded_signal))

            for i in range(len(loaded_signal)):
                self.assertAlmostEqual(loaded_signal[i].real, signal[i].real, places=1)
                self.assertAlmostEqual(loaded_signal[i].imag, signal[i].imag, places=1)

    def test_save_filename_load(self):
        signal = dspftw.complex_sinusoid(A=1, f=10, t=linspace(1, 10, num=10), phi=0)
        signal_types = ('8t', '16t', '32t', '32f', '64f')
        endiannesses = ('little', 'big')

        for signal_type in signal_types:
            for endianness in endiannesses:
                self.try_save_filename_load(signal, signal_type, endianness)
