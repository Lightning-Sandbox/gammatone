#!/usr/bin/env python3
# Copyright 2014 Jason Heeris, jason.heeris@gmail.com
#
# This file is part of the gammatone toolkit, and is licensed under the 3-clause
# BSD license: https://github.com/detly/gammatone/blob/master/COPYING
from __future__ import division

import gammatone.fftweight
import numpy as np
import pytest
import scipy.io
from pkg_resources import resource_stream

REF_DATA_FILENAME = "data/test_fft2gtmx_data.mat"
INPUT_KEY = "fft2gtmx_inputs"
RESULT_KEY = "fft2gtmx_results"
INPUT_COLS = ("nfft", "sr", "nfilts", "width", "fmin", "fmax", "maxlen")
RESULT_COLS = ("weights", "gain")

# Load test data generated from the reference code
with resource_stream(__name__, REF_DATA_FILENAME) as test_data:
    DATA = scipy.io.loadmat(test_data, squeeze_me=False)

INPUT_REF_DICTS = [
    (dict(zip(INPUT_COLS, map(np.squeeze, inputs))), dict(zip(RESULT_COLS, map(np.squeeze, refs))))
    for inputs, refs in zip(DATA[INPUT_KEY], DATA[RESULT_KEY])
]


@pytest.mark.parametrize("inputs,refs", INPUT_REF_DICTS)
def test_fft_weights(inputs, refs):
    args = tuple(inputs[col] for col in INPUT_COLS)
    expected = (refs["weights"], refs["gain"])

    args = list(args)
    expected_weights = expected[0]
    expected_gains = expected[1]

    # Convert nfft, nfilts, maxlen to ints
    args[0] = int(args[0])
    args[2] = int(args[2])
    args[6] = int(args[6])

    weights, gains = gammatone.fftweight.fft_weights(*args)

    assert gains.shape == expected_gains.shape
    assert np.allclose(gains, expected_gains, rtol=1e-6, atol=1e-12)

    assert weights.shape == expected_weights.shape
    assert np.allclose(weights, expected_weights, rtol=1e-6, atol=1e-12)
