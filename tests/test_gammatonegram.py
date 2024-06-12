#!/usr/bin/env python3
# Copyright 2014 Jason Heeris, jason.heeris@gmail.com
#
# This file is part of the gammatone toolkit, and is licensed under the 3-clause
# BSD license: https://github.com/detly/gammatone/blob/master/COPYING

import gammatone.gtgram
import numpy as np
import pytest
import scipy.io
from mock import patch
from pkg_resources import resource_stream

REF_DATA_FILENAME = "data/test_gammatonegram_data.mat"
INPUT_KEY = "gammatonegram_inputs"
MOCK_KEY = "gammatonegram_mocks"
RESULT_KEY = "gammatonegram_results"
INPUT_COLS = ("name", "wave", "fs", "twin", "thop", "channels", "fmin")
MOCK_COLS = ("erb_fb", "erb_fb_cols")
RESULT_COLS = ("gtgram", "nwin", "hopsamps", "ncols")


# Load test data generated from the reference code
with resource_stream(__name__, REF_DATA_FILENAME) as test_data:
    DATA = scipy.io.loadmat(test_data, squeeze_me=True)
INPUT_MOCK_REF_DICTS = [
    (dict(zip(INPUT_COLS, inputs)), dict(zip(MOCK_COLS, mocks)), dict(zip(RESULT_COLS, refs)))
    for inputs, mocks, refs in zip(DATA[INPUT_KEY], DATA[MOCK_KEY], DATA[RESULT_KEY])
]


@pytest.mark.parametrize("inputs,mocks,refs", INPUT_MOCK_REF_DICTS)
def test_nstrides(inputs, mocks, refs):
    """Test gamamtonegram stride calculations"""
    args = (inputs["fs"], inputs["twin"], inputs["thop"], mocks["erb_fb_cols"])

    expected = (refs["nwin"], refs["hopsamps"], refs["ncols"])

    results = gammatone.gtgram.gtgram_strides(*args)
    # These are integer values, so use direct equality
    assert results == expected


# TODO: possibly mock out gtgram_strides


@pytest.mark.parametrize("inputs,mocks,refs", INPUT_MOCK_REF_DICTS)
def test_gtgram(inputs, mocks, refs):
    args = (inputs["fs"], inputs["twin"], inputs["thop"], inputs["channels"], inputs["fmin"])
    signal = np.asarray(inputs["wave"])
    expected = np.asarray(refs["gtgram"])
    erb_fb_out = np.asarray(mocks["erb_fb"])

    with patch("gammatone.gtgram.erb_filterbank", return_value=erb_fb_out):
        result = gammatone.gtgram.gtgram(signal, *args)

        max_diff = np.max(np.abs(result - expected))
        diagnostic = "Maximum difference: {:6e}".format(max_diff)

        assert np.allclose(result, expected, rtol=1e-6, atol=1e-12), diagnostic
