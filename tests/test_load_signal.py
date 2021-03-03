# vim: expandtab tabstop=4 shiftwidth=4

from numpy import array as nparray
from numpy import isnan
from pathlib import Path
from subprocess import getstatusoutput
from tempfile import TemporaryDirectory

import os
import unittest

import dspftw

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

def has_nan(signal: nparray) -> bool:
    return any(isnan(signal))

class LoadSignalTests(unittest.TestCase):
    def generate_signal(self, signal_type: str, endianness: str) -> nparray:
        with TemporaryDirectory() as tempdir:
            working_dir = Path(tempdir)
            output_path = working_dir.joinpath('test_file.'+signal_type)
            octave_command = f'octave --path {FILE_DIR}/octave {FILE_DIR}/octave/SigGenTest.m {output_path} {signal_type} {endianness}'
            print(octave_command)
            octave_status, octave_output = getstatusoutput(octave_command)
            print(octave_output)
            self.assertEqual(octave_status, 0)
            return dspftw.load_signal(output_path, signal_type, 'cplx', endianness)

    def test_load_32fl_signal(self):
        signal = self.generate_signal('32f', 'little')
        self.assertEqual(len(signal), 10_000)
        self.assertFalse(has_nan(signal))

    def test_load_8t_signal(self):
        signal = self.generate_signal('8t', 'little')
        self.assertEqual(len(signal), 10_000)
        self.assertFalse(has_nan(signal))
