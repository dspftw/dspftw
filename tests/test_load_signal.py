# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from tempfile import TemporaryDirectory

import unittest

from numpy import array
from numpy.testing import assert_allclose

import dspftw


class LoadSignalTests(unittest.TestCase):
    def test_real_16t(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [-32768, -16384, 0, 16384, 32767],
                dtype='<i2',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '16t',
                'real',
                'little',
            )

            expected = array([
                -1.0,
                -0.5,
                0.0,
                0.5,
                32767 / 32768,
            ])

            assert_allclose(result, expected)
            self.assertEqual(result.dtype.name, 'float64')

    def test_complex_16t(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            # Interleaved I, Q samples
            data = array(
                [16384, -16384, 8192, 24576],
                dtype='<i2',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '16t',
                'complex',
                'little',
            )

            expected = array([
                0.5 - 0.5j,
                0.25 + 0.75j,
            ])

            assert_allclose(result, expected)
            self.assertEqual(result.dtype.name, 'complex128')

    def test_real_32f(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [-1.0, -0.5, 0.0, 0.5, 1.0],
                dtype='<f4',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '32f',
                'real',
                'little',
            )

            assert_allclose(result, data)
            self.assertEqual(result.dtype.name, 'float32')

    def test_complex_32f(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [0.5, -0.5, 0.25, 0.75],
                dtype='<f4',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '32f',
                'complex',
                'little',
            )

            expected = array(
                [0.5 - 0.5j, 0.25 + 0.75j],
                dtype='complex64',
            )

            assert_allclose(result, expected)
            self.assertEqual(result.dtype.name, 'complex64')

    def test_start_sample_and_num_samples(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
                dtype='<f4',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '32f',
                'real',
                'little',
                num_samples=3,
                start_sample=2,
            )

            expected = array(
                [2.0, 3.0, 4.0],
                dtype='float32',
            )

            assert_allclose(result, expected)

    def test_big_endian(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [16384, -16384, 8192],
                dtype='>i2',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '16t',
                'real',
                'big',
            )

            expected = array([
                0.5,
                -0.5,
                0.25,
            ])

            assert_allclose(result, expected)


    def test_true_one_rounding(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            data = array(
                [-32768, -16384, 0, 16384, 32767],
                dtype='<i2',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '16t',
                'real',
                'little',
                rounding=1,
            )

            scale = 32768
            expected = data / scale + 1 / (2 * scale)

            assert_allclose(result, expected)
            self.assertEqual(result.dtype.name, 'float64')

    def test_complex_start_sample_and_num_samples(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir) / 'signal_file'

            # Four complex samples stored as interleaved I, Q values:
            # (1+2j), (3+4j), (5+6j), (7+8j)
            data = array(
                [
                    1.0, 2.0,
                    3.0, 4.0,
                    5.0, 6.0,
                    7.0, 8.0,
                ],
                dtype='<f4',
            )
            data.tofile(file_path)

            result = dspftw.load_signal(
                str(file_path),
                '32f',
                'complex',
                'little',
                num_samples=2,
                start_sample=1,
            )

            expected = array(
                [
                    3.0 + 4.0j,
                    5.0 + 6.0j,
                ],
                dtype='complex64',
            )

            assert_allclose(result, expected)
            self.assertEqual(result.dtype.name, 'complex64')


if __name__ == '__main__':
    unittest.main()
