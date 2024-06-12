#!/usr/bin/env python3
# Copyright 2014 Jason Heeris, jason.heeris@gmail.com
#
# This file is part of the gammatone toolkit, and is licensed under the 3-clause
# BSD license: https://github.com/detly/gammatone/blob/master/COPYING

import gammatone.filters
import numpy as np
import pytest
import scipy.io
from pkg_resources import resource_stream

REF_DATA_FILENAME = "data/test_erbspace_data.mat"
INPUT_KEY = "erbspace_inputs"
RESULT_KEY = "erbspace_results"
INPUT_COLS = ("f_low", "f_high", "num_f")
RESULT_COLS = ("cfs",)

# Load test data generated from the reference code
with resource_stream(__name__, REF_DATA_FILENAME) as test_data:
    DATA = scipy.io.loadmat(test_data, squeeze_me=False)

INPUT_REF_DICTS = [
    (dict(zip(INPUT_COLS, map(np.squeeze, inputs))), dict(zip(RESULT_COLS, map(np.squeeze, refs))))
    for inputs, refs in zip(DATA[INPUT_KEY], DATA[RESULT_KEY])
]


@pytest.mark.parametrize("inputs,refs", INPUT_REF_DICTS)
def test_ERB_space_known_values(inputs, refs):
    args = (inputs["f_low"], inputs["f_high"], inputs["num_f"])
    expected = refs["cfs"]

    result = gammatone.filters.erb_space(*args)
    assert np.allclose(result, expected, rtol=1e-6, atol=1e-10)
