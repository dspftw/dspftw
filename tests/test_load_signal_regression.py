
# vim: expandtab tabstop=4 shiftwidth=4

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import numpy as np
from numpy.testing import assert_array_equal

import dspftw


class LoadSignalRegressionTests(unittest.TestCase):
    """Verify load_signal against the original conversion behavior."""

    SAMPLE_TYPES = {
        '8t': 'i1',
        '16t': 'i2',
        '32t': 'i4',
        '32f': 'f4',
        '64f': 'f8',
    }

    OUTPUT_DTYPES = {
        '8t': (np.float64, np.complex128),
        '16t': (np.float64, np.complex128),
        '32t': (np.float64, np.complex128),
        '32f': (np.float32, np.complex64),
        '64f': (np.float64, np.complex128),
    }

    @staticmethod
    def reference_conversion(raw, signal_type, number_space, rounding):
        """Independent copy of the original post_load algorithm."""
        scales = {
            '8t': 2**7,
            '16t': 2**15,
            '32t': 2**31,
            '32f': 1,
            '64f': 1,
        }

        scale = scales[signal_type]
        scaled = raw / scale

        if signal_type in ('8t', '16t', '32t') and rounding == 1:
            scaled += 1 / (2 * scale)

        if number_space == 'complex':
            return scaled[0::2] + scaled[1::2] * 1j

        return scaled

    @staticmethod
    def make_data(signal_type, dtype):
        """Generate representative input values."""
        if signal_type in ('8t', '16t', '32t'):
            info = np.iinfo(dtype)
            values = [
                info.min,
                info.min // 2,
                -1,
                0,
                1,
                info.max // 2,
                info.max,
                17,
                -17,
                3,
                -3,
                0,
            ]
        else:
            values = [
                -1.0, -0.5,
                -0.125, -0.0,
                0.0, 0.125,
                0.5, 1.0,
                0.75, -0.75,
                0.25, -0.25,
            ]

        return np.array(values, dtype=dtype)

    def test_all_formats(self):
        for signal_type, dtype_code in self.SAMPLE_TYPES.items():
            for number_space in ('real', 'complex'):
                for endianness, prefix in (
                    ('little', '<'),
                    ('big', '>'),
                ):
                    rounding_modes = (
                        (0, 1)
                        if signal_type in ('8t', '16t', '32t')
                        else (0,)
                    )

                    for rounding in rounding_modes:
                        with self.subTest(
                            signal_type=signal_type,
                            number_space=number_space,
                            endianness=endianness,
                            rounding=rounding,
                        ):
                            dtype = np.dtype(prefix + dtype_code)
                            raw = self.make_data(signal_type, dtype)

                            with TemporaryDirectory() as tempdir:
                                file_path = Path(tempdir) / 'signal_file'
                                raw.tofile(file_path)

                                for start, count in (
                                    (0, -1),
                                    (0, 3),
                                    (2, 3),
                                    (4, 2),
                                ):
                                    with self.subTest(
                                        start=start,
                                        count=count,
                                    ):
                                        result = dspftw.load_signal(
                                            str(file_path),
                                            signal_type,
                                            number_space,
                                            endianness,
                                            num_samples=count,
                                            start_sample=start,
                                            rounding=rounding,
                                        )

                                        items_per_sample = (
                                            2 if number_space == 'complex'
                                            else 1
                                        )
                                        first = start * items_per_sample

                                        if count == -1:
                                            selected = raw[first:]
                                        else:
                                            last = (
                                                first
                                                + count * items_per_sample
                                            )
                                            selected = raw[first:last]

                                        expected = self.reference_conversion(
                                            selected,
                                            signal_type,
                                            number_space,
                                            rounding,
                                        )

                                        assert_array_equal(result, expected)

                                        expected_dtype = self.OUTPUT_DTYPES[
                                            signal_type
                                        ][number_space == 'complex']

                                        self.assertEqual(
                                            result.dtype,
                                            np.dtype(expected_dtype),
                                        )


if __name__ == '__main__':
    unittest.main()
