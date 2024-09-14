"""
fastcash.values.countweak

Provides a value set for counting k-mers up to a given maximum count,
and storing a weak bit (the HIGHEST bit)

Provides public constants:
- NAME = "countweak"
- NVALUES
- RCMODE
and functions:
- get_value_from_name
- update
- is_compatible

Other provided attributes should be considered private, as they may change.
"""

from collections import namedtuple
from math import ceil, log2

import numpy as np
from numba import njit, uint64


ValueInfo = namedtuple("ValueInfo", [
    "NAME",
    "NVALUES",
    "RCMODE",
    "get_value_from_name",
    "update",
    "is_compatible",
    "strsymbols",
    "bytesymbols",
    "unit",
    "true_nvalues",
    "bits",
    ])


def initialize(nvalues, rcmode="max"):
    nvalues = int(nvalues)
    bits = int(ceil(log2(nvalues)))
    nvalues = int(nvalues) + 2**bits
    bits += 1
    U64_MINUSONE = uint64(np.iinfo(np.uint64).max)

    def get_value_from_name(name, onetwo=1):
        return 1  # always one count

    @njit(nogil=True, locals=dict(
        old=uint64, new=uint64, updated=uint64))
    def update(old, new):
        """
        update(uint64, uint64) -> uint64
        Update old value (stored) with a new value (increment, or -1 for weak)
        Return upated value.
        """
        if new == U64_MINUSONE:  # -1 marks weak
            updated = uint64(old | (2**(bits - 1)))
        else:
            # assert new > 0
            updated = uint64(min(old + new, nvalues - 2**(bits - 1) - 1))
        return uint64(updated)

    @njit(
        nogil=True, locals=dict(observed=uint64, stored=uint64))
    def is_compatible(observed, stored):
        """
        is_compatible(uint64, uint64) -> bool
        Check wheter an observed value is compatible with a stored value,
        i.e., iff there exists new such that update(observed, new) == stored.
        """
        s = stored % nvalues // 2
        o = observed % nvalues // 2
        return (s >= o)

    return ValueInfo(
        NAME="countweak",
        NVALUES=nvalues,
        RCMODE=rcmode,
        get_value_from_name=get_value_from_name,
        update=update,
        is_compatible=is_compatible,
        strsymbols=dict(),
        bytesymbols=dict(),
        unit=1,
        true_nvalues=nvalues,
        bits=bits,
        )
