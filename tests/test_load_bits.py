# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from dspftw import load_bits

class LoadBitsTests(unittest.TestCase):
    def test_load_bits(self):
        with TemporaryDirectory() as tempdir:
            tempdir_path = Path(tempdir)
            tempfile = tempdir_path.joinpath('test.bits')
            tempfile.write_bytes(b'\x00\x01\x02\x03')

            bits = load_bits(str(tempfile.resolve()))
