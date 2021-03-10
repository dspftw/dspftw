# vim: expandtab tabstop=4 shiftwidth=4

from numpy import array as nparray
from numpy import isnan
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

def endianness_suffix(endianness: str) -> str:
    if endianness in ('little', 'l'):
        return 'l'

    return ''

class FilenameLoadTests(unittest.TestCase):
    def generate_signal(self, signal_type: str, endianness: str) -> Tuple[nparray, Dict[str, Any]]:
        with TemporaryDirectory() as tempdir:
            working_dir = Path(tempdir)
            output_path = working_dir.joinpath('test_file.cplx.0.'+signal_type+endianness_suffix(endianness))
            octave_command = f'octave --path {FILE_DIR}/octave {FILE_DIR}/octave/SigGenTest.m {output_path} {signal_type} {endianness}'
            print(octave_command)
            octave_status, _ = getstatusoutput(octave_command)
            self.assertEqual(octave_status, 0)
            return dspftw.filename_load(output_path)

    def test_load_32fl_signal(self):
        signal, metadata = self.generate_signal('32f', 'little')
        self.assertEqual(len(signal), 10_000)
        self.assertFalse(has_nan(signal))
        self.assertEqual(metadata['sample_rate'], 0.0)
