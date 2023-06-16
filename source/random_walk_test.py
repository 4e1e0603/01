# -*- coding: utf-8 -*-

import numpy as np


def test_restricted_moves():
    # Check steps according to transition table
    steps = [] # FIXME Seet the lxsolution for `steps`.
    for F, T in [(0, 2), (1, 3), (2, 0), (3, 1)]:
        nxt = np.where(steps == F)[0] + 1
        nxt = nxt[nxt < len(steps)]
        assert not np.any(np.where(steps[nxt] == T)[0])
        # Restricted move ({F}, {T}) found!'
