#!/usr/bin/env python3
# Copyright 2014 Jason Heeris, jason.heeris@gmail.com
#
# This file is part of the gammatone toolkit, and is licensed under the 3-clause
# BSD license: https://github.com/detly/gammatone/blob/master/COPYING

import numpy as np
import pytest
import scipy.io
from pkg_resources import resource_stream

import gammatone.filters

REF_DATA_FILENAME = "data/test_erb_filter_data.mat"
INPUT_KEY = "erb_filter_inputs"
RESULT_KEY = "erb_filter_results"
INPUT_COLS = ("fs", "cfs")
RESULT_COLS = ("fcoefs",)
# Load test data generated from the reference code
with resource_stream(__name__, REF_DATA_FILENAME) as test_data:
    DATA = scipy.io.loadmat(test_data, squeeze_me=False)
INPUT_REF_DICTS = [
    (dict(zip(INPUT_COLS, map(np.squeeze, inputs))), dict(zip(RESULT_COLS, map(np.squeeze, refs))))
    for inputs, refs in zip(DATA[INPUT_KEY], DATA[RESULT_KEY])
]


@pytest.mark.parametrize("inputs,refs", INPUT_REF_DICTS)
def test_make_ERB_filters_known_values(inputs, refs):
    args = (inputs["fs"], inputs["cfs"])
    fs = args[0]
    cfs = args[1]
    expected = refs["fcoefs"]

    result = gammatone.filters.make_erb_filters(fs, cfs)
    assert np.allclose(result, expected, rtol=1e-6, atol=1e-12)
