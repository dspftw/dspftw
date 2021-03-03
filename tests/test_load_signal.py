# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from subprocess import getstatusoutput
from tempfile import TemporaryDirectory

import os
import unittest

import dspftw

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

class LoadSignalTests(unittest.TestCase):
    def generate_signal(self, signal_type: str, endianness: str) -> None:
        with TemporaryDirectory() as tempdir:
            working_dir = Path(tempdir)
            output_path = working_dir.joinpath('test_file.'+signal_type)
            octave_command = f'octave {FILE_DIR}/octave/SigGenTest.m {output_path} {signal_type} {endianness}'
            print(octave_command)
            octave_status, octave_output = getstatusoutput(octave_command)
            print(octave_output)
            self.assertEqual(octave_status, 0)
            return dspftw.load_signal(output_path, signal_type, 'cplx', endianness)

    def test_load_signal(self):
        sig = self.generate_signal('32f', 'little')
        self.assertGreater(len(sig), 0)
