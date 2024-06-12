#!/usr/bin/env python3
# Copyright 2014 Jason Heeris, jason.heeris@gmail.com
#
# This file is part of the gammatone toolkit, and is licensed under the 3-clause
# BSD license: https://github.com/detly/gammatone/blob/master/COPYING

import numpy as np
import pytest
import scipy.io
from mock import patch
from pkg_resources import resource_stream

import gammatone.fftweight

REF_DATA_FILENAME = "data/test_fft_gammatonegram_data.mat"
INPUT_KEY = "fft_gammatonegram_inputs"
MOCK_KEY = "fft_gammatonegram_mocks"
RESULT_KEY = "fft_gammatonegram_results"
INPUT_COLS = ("name", "wave", "fs", "twin", "thop", "channels", "fmin")
MOCK_COLS = ("wts",)
RESULT_COLS = ("res", "window", "nfft", "nwin", "nhop")
# Load test data generated from the reference code
with resource_stream(__name__, REF_DATA_FILENAME) as test_data:
    DATA = scipy.io.loadmat(test_data, squeeze_me=False)
INPUTS_MOCKS_REFS_DICTS = [
    (dict(zip(INPUT_COLS, inputs)), dict(zip(MOCK_COLS, mocks)), dict(zip(RESULT_COLS, refs)))
    for inputs, mocks, refs in zip(DATA[INPUT_KEY], DATA[MOCK_KEY], DATA[RESULT_KEY])
]


@pytest.mark.parametrize("inputs,mocks,refs", INPUTS_MOCKS_REFS_DICTS)
def test_fft_specgram_window(inputs, mocks, refs):
    args = (refs["nfft"], refs["nwin"])
    nfft = args[0].squeeze()
    nwin = args[1].squeeze()
    expected = refs["window"].squeeze()

    result = gammatone.fftweight.specgram_window(nfft, nwin)
    max_diff = np.max(np.abs(result - expected))
    assert np.allclose(result, expected, rtol=1e-6, atol=2e-3), "Maximum difference: {:6e}".format(max_diff)


@pytest.mark.parametrize("inputs,mocks,refs", INPUTS_MOCKS_REFS_DICTS)
def test_fft_gtgram(inputs, mocks, refs):
    args = (inputs["fs"], inputs["twin"], inputs["thop"], inputs["channels"], inputs["fmin"])
    signal = np.asarray(inputs["wave"]).squeeze()
    expected = np.asarray(refs["res"]).squeeze()
    fft_weights = np.asarray(mocks["wts"])
    window = refs["window"].squeeze()

    # Note that the second return value from fft_weights isn't actually used
    with patch("gammatone.fftweight.fft_weights", return_value=(fft_weights, None)), patch(
        "gammatone.fftweight.specgram_window", return_value=window
    ):
        result = gammatone.fftweight.fft_gtgram(signal, *args)

        max_diff = np.max(np.abs(result - expected))
        diagnostic = "Maximum difference: {:6e}".format(max_diff)

        assert np.allclose(result, expected, rtol=1e-6, atol=1e-12), diagnostic
