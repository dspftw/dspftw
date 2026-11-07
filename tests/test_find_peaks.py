
import unittest

from numpy import arange, array, exp
from numpy.testing import assert_array_equal

from dspftw import find_peaks


class TestFindPeaks(unittest.TestCase):

    def test_endpoints(self):
        result = find_peaks(
            array([5, 1, 0, 0, 1, 6]),
            min_height=0.5, min_dist=2)
        assert_array_equal(result, [5, 0])

    def test_equal_height(self):
        result = find_peaks(
            array([0, 1, 3, 3, 3, 1, 0]),
            min_height=0.5, min_dist=2)
        assert_array_equal(result, [2, 5])

    def test_strict_threshold(self):
        result = find_peaks(
            array([0, 0.7, 0, 0.7, 0]),
            min_height=0.7, min_dist=1)
        assert_array_equal(result, [])

    def test_peak_limit(self):
        result = find_peaks(
            array([5, 1, 0, 0, 1, 6]),
            min_height=0.5, min_dist=2, num_peaks=1)
        assert_array_equal(result, [5])

    def test_zero_peak_limit(self):
        result = find_peaks(
            array([5, 1, 0, 0, 1, 6]),
            min_height=0.5, min_dist=2, num_peaks=0)
        assert_array_equal(result, [])

    def test_empty_input(self):
        result = find_peaks(
            array([]), min_height=0.5, min_dist=2)
        assert_array_equal(result, [])

    def test_gaussian_skirt(self):
        x = arange(81)
        gaussian = exp(-((x - 40) / 10.0)**2)
        result = find_peaks(
            gaussian, min_height=0.1, min_dist=10)
        assert_array_equal(result, [40, 29, 51])

    def test_zero_min_distance(self):
        result = find_peaks(
            array([1, 2, 3, 2, 1]),
            min_height=0.5, min_dist=0)
        assert_array_equal(result, [2, 1, 3, 0, 4])


    def test_randomized_against_original(self):
        from numpy import argmax, inf, pad
        from numpy.random import default_rng

        def original(data, min_height, min_dist, num_peaks):
            out = []
            if num_peaks <= 0:
                return array(out, dtype=int)

            arr = pad(
                array(data).flatten(),
                (min_dist, min_dist),
                mode='constant',
                constant_values=min_height - 1)

            midx = argmax(arr)
            while arr[midx] > min_height:
                out.append(midx - min_dist)
                if len(out) >= num_peaks:
                    break

                arr[max(0, midx - min_dist):
                    midx + min_dist + 1] = min_height - 1
                midx = argmax(arr)

            return array(out, dtype=int)

        rng = default_rng(12345)

        for length in [10, 25, 100, 500]:
            for distance in [0, 1, 3, 10, 20]:
                for height in [-1, 0, 1, 3]:
                    for limit in [1, 3, 10, inf]:
                        data = rng.integers(-3, 6, size=length)

                        expected = original(
                            data, height, distance, limit)
                        actual = find_peaks(
                            data, min_height=height,
                            min_dist=distance, num_peaks=limit)

                        with self.subTest(
                            length=length, distance=distance,
                            height=height, limit=limit):
                            assert_array_equal(actual, expected)

if __name__ == '__main__':
    unittest.main()
