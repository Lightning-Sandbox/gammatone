#!/usr/bin/env python3
# Copyright 2014 Jason Heeris, jason.heeris@gmail.com
#
# This file is part of the gammatone toolkit, and is licensed under the 3-clause
# BSD license: https://github.com/detly/gammatone/blob/master/COPYING

import gammatone.fftweight
import numpy as np
import pytest
import scipy.io
from mock import patch
from pkg_resources import resource_stream

REF_DATA_FILENAME = "data/test_specgram_data.mat"
INPUT_KEY = "specgram_inputs"
MOCK_KEY = "specgram_mocks"
RESULT_KEY = "specgram_results"
INPUT_COLS = ("name", "wave", "nfft", "fs", "nwin", "nhop")
MOCK_COLS = ("window",)
RESULT_COLS = ("res",)

# Load test data generated from the reference code
with resource_stream(__name__, REF_DATA_FILENAME) as test_data:
    DATA = scipy.io.loadmat(test_data, squeeze_me=False)
INPUT_MOCK_REF_DICTS = [
    (dict(zip(INPUT_COLS, inputs)), dict(zip(MOCK_COLS, mocks)), dict(zip(RESULT_COLS, refs)))
    for inputs, mocks, refs in zip(DATA[INPUT_KEY], DATA[MOCK_KEY], DATA[RESULT_KEY])
]


@pytest.mark.parametrize("inputs,mocks,refs", INPUT_MOCK_REF_DICTS)
def test_specgram(inputs, mocks, refs):
    args = (inputs["nfft"], inputs["fs"], inputs["nwin"], inputs["nhop"])

    signal = np.asarray(inputs["wave"]).squeeze()
    expected = np.asarray(refs["res"]).squeeze()
    args = [int(a.squeeze()) for a in args]
    window = mocks["window"].squeeze()

    with patch("gammatone.fftweight.specgram_window", return_value=window):
        result = gammatone.fftweight.specgram(signal, *args)

        max_diff = np.max(np.abs(result - expected))
        diagnostic = "Maximum difference: {:6e}".format(max_diff)

        assert np.allclose(result, expected, rtol=1e-6, atol=1e-12), diagnostic
