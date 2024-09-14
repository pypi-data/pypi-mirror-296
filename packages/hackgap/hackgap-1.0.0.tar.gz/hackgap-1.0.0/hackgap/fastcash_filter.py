"""
Module fastcash.fastcash_filter

This module provides
-  FCFilter, a namedtuple to store filter information

It provides jit-compiled factory functions to build an FCFilter.
"""


from collections import namedtuple


FCFilter = namedtuple("FCFilter", [
    # atributes
    "universe",
    "size",
    "nlevels",
    "nsubfilters",
    "hashfuncs",
    "hashtype",
    "choices",
    "subfilterbits",
    "filterbits",
    "mem_bytes",
    "array",

    # public API methods; example: f.store_new(f.array, canonical_code)
    # TODO: put/insert/set/add; get/lookup/check/has get_fill_levels
    # TODO: decision: insert == update, lookup == get_value
    # TODO: new function! get_fprs
    "update",  # (table:uint64[:], key:uint64, value:uint64)
    "insert",  # (table:uint64[:], key:uint64, value:uint64)
    "lookup",  # (table:uint64[:], key:uint64) -> boolean
    "get_value",  # (table:uint64[:], key:uint64) -> boolean
    "get_fprs",  # (table:uint64[:]) -> float[:]
    "get_fill_levels",  # (table:uint64[:]) -> float[:]

    # private API methods (see below)
    "private",
    ])

FCFilter_private = namedtuple("FCFilter_private", [
    # private API methods, may change !
    "lookup_in_subfilter",  # (table:uint64[:], subfilter:uint64, key:uint64) -> uint64
    "insert_in_subfilter",  # (table:uint64[:], subfilter:uint64, key:uint64, value:uint64)
    "lookup_and_insert_in_subfilter",  # (table:uint64[:], subfilter:uint64, key:uint64, value:uint64)
    ])


def create_FCFilter(d):
    """Return FCFilter initialized from values in dictionary d"""
    # The given d does not need to provide mem_bytes; it is computed here.
    # The given d is copied and reduced to the required fields.
    # The hashfuncs tuple is reduced to a single ASCII bytestring.
    d0 = dict(d)
    mem_bytes = 0
    mem_bytes += d0['array'].nbytes
    d0['mem_bytes'] = mem_bytes
    private = {name: d0[name] for name in FCFilter_private._fields}
    d0['private'] = FCFilter_private(**private)
    d1 = {name: d0[name] for name in FCFilter._fields}
    d1['hashfuncs'] = (':'.join(d1['hashfuncs'])).encode("ASCII")
    return FCFilter(**d1)
