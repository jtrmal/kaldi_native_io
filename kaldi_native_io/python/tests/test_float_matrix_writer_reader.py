#!/usr/bin/env python3

# Copyright      2022  Xiaomi Corporation (authors: Fangjun Kuang)

import os

import numpy as np

import kaldi_native_io

base = "float_matrix"
wspecifier = f"ark,scp,t:{base}.ark,{base}.scp"
rspecifier = f"scp:{base}.scp"


def test_float_matrix_writer():
    with kaldi_native_io.FloatMatrixWriter(wspecifier) as ko:
        ko.write("a", np.array([[1, 2], [3, 4]], dtype=np.float32))
        ko["b"] = np.array([[10, 20, 30], [40, 50, 60]], dtype=np.float32)


def test_sequential_float_matrix_reader():
    with kaldi_native_io.SequentialFloatMatrixReader(rspecifier) as ki:
        for key, value in ki:
            if key == "a":
                assert np.array_equal(
                    value, np.array([[1, 2], [3, 4]], dtype=np.float32)
                )
            elif key == "b":
                assert np.array_equal(
                    value,
                    np.array([[10, 20, 30], [40, 50, 60]], dtype=np.float32),
                )
            else:
                raise ValueError(f"Unknown key {key} with value {value}")


def test_random_access_float_matrix_reader():
    with kaldi_native_io.RandomAccessFloatMatrixReader(rspecifier) as ki:
        assert "b" in ki
        assert "a" in ki
        assert np.array_equal(
            ki["a"], np.array([[1, 2], [3, 4]], dtype=np.float32)
        )
        assert np.array_equal(
            ki["b"], np.array([[10, 20, 30], [40, 50, 60]], dtype=np.float32)
        )


def main():
    test_float_matrix_writer()
    test_sequential_float_matrix_reader()
    test_random_access_float_matrix_reader()

    os.remove(f"{base}.scp")
    os.remove(f"{base}.ark")


if __name__ == "__main__":
    main()