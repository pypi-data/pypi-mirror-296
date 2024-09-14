"""
filter_bi_b3c:
filter bit-interleaved bloom 3 choices (hash funcs)

a Blocked Bloom filter with
- block size 512 (cache line size)
- 3 hash functions addressing bits in the same block
- use bit interleaving for different levels (up to 3)
"""

import numpy as np

from math import ceil
from numba import njit, int64, uint64

from .fastcash_filter import create_FCFilter
from .lowlevel import debug  # the global debugging functions
from .lowlevel.bitarray import bitarray
from .hashfunctions import compile_get_bucket
from .subtable_hashfunctions import populate_hashfunc_tuple


def build_filter(universe, sizes, nsubfilters, hashfunc01, hashfunctuples):
    """
    Allocate an array and compile access methods
    for a multi-level bit interleaved blocked bloom filter.
    Return an FCFilter object.
    """

    U64_MINUSONE = uint64(np.iinfo(np.uint64).max)
    # Get debug printing functions and set basic properties
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    hashtype = "bi_b3c"  # bit interleaving blocked bloom filter using 3 hash functions
    choices = 3
    blocksize = 512
    blockmask = uint64(blocksize - 1)

    if nsubfilters <= 1:
        debugprint0("- Warning: The filter is not specialized for one subfilter")

    nlevels = len(sizes)
    if nlevels > 3:
        raise ValueError("Too many levels specified; at most 3 levels are supported.")
    if len(hashfunctuples) != nlevels:
        raise ValueError(f"{len(hashfunctuples)=} does not equal {nlevels=}")
    if not all(len(hft) == choices for hft in hashfunctuples):
        raise ValueError(f"length of some hash function tuple is not {choices}: {hashfunctuples}")

    size = sum(sizes)
    bits_per_level = [int(s / size * blocksize) for s in sizes]
    bits_per_level[0] = blocksize - sum(bits_per_level[1:])
    bits_per_level = tuple(bits_per_level)
    if min(bits_per_level) < 20:
        raise ValueError(f"One filter is too small: min({bits_per_level}) < 20")
    level_borders = [sum(bits_per_level[:i]) for i in range(nlevels + 1)]
    # for blocksize == 512: [512] -> [0, 512];  # [500, 12] -> [0, 500, 512]
    assert level_borders[-1] == blocksize, f"last level border is not {blocksize}: {level_borders=}"
    while len(level_borders) < 4:
        level_borders.append(blocksize)
    level_borders = tuple(level_borders)

    size_bits = int(ceil(size * 1024 * 1024 * 1024 * 8))  # 2**33 (size given in Gigabytes)
    nblocks_per_subfilter = int(ceil((size_bits // nsubfilters) / blocksize))
    if nblocks_per_subfilter % 2 == 0:
        nblocks_per_subfilter += 1
    subfilterbits = nblocks_per_subfilter * blocksize
    filterbits = subfilterbits * nsubfilters

    filter = bitarray(filterbits, alignment=64)
    debugprint1(f"- filter: {nsubfilters=}; total size {filter.array.size} x {filter.array.dtype} ({filter.array.size * 8 / 2**30:.4f} GiB)")
    debugprint1(f"- filter: level bits: {bits_per_level}")
    debugprint1(f"- filter: level borders: {level_borders}")

    get_value_at = filter.getquick  # (array, startbit)
    set_value_at = filter.setquick  # (array, startbit[, value])
    # get_value_at = filter.get  # (array, startbit, nbits=1)
    # set_value_at = filter.set  # (array, startbit, value, nbits=1)
    popcount = filter.popcount

    # get first and second hash function from the tuple
    firsthashfunc, secondhashfunc = hashfunc01
    get_subfilter = compile_get_bucket(firsthashfunc, universe, nsubfilters)
    # Same hash function that is used for subtables
    debugprint2(f"- subfilter hash function: {firsthashfunc}")
    secondhashfunc = populate_hashfunc_tuple([secondhashfunc], mod_value=nblocks_per_subfilter)[0]
    debugprint2(f"- block hash function: {secondhashfunc}")
    # get_block, _ = build_get_bucket_fpr_from_subkey(secondhashfunc, universe, nblocks_per_subfilter, 1)
    get_block = compile_get_bucket(secondhashfunc, universe, nblocks_per_subfilter)

    # get all hash functions for the filters
    level_hashfuncs = []
    for level, bits in enumerate(bits_per_level):
        hashfuncs = populate_hashfunc_tuple(hashfunctuples[level], mod_value=bits)
        debugprint2(f"- for {level=}, using {hashfuncs=}")
        level_hashfuncs.append([compile_get_bucket(hfi, universe, bits) for hfi in hashfuncs])
    assert len(level_hashfuncs) <= 3
    if len(level_hashfuncs) < 3:
        dummyhf = njit(nogil=True)(lambda *_: U64_MINUSONE)
        dummyhfs = (dummyhf,) * 3
        while len(level_hashfuncs) < 3:
            level_hashfuncs.append(dummyhfs)

    # bf_level_choice
    bf_1_1, bf_1_2, bf_1_3 = level_hashfuncs[0]
    bf_2_1, bf_2_2, bf_2_3 = level_hashfuncs[1]
    bf_3_1, bf_3_2, bf_3_3 = level_hashfuncs[2]

    @njit(nogil=True, locals=dict(
        level=uint64, b1=uint64, b2=uint64, b3=uint64))
    def get_hashfuncs(level, key):
        if level == 0:
            b1 = bf_1_1(key)
            b2 = bf_1_2(key)
            b3 = bf_1_3(key)
        elif level == 1:
            b1 = bf_2_1(key)
            b2 = bf_2_2(key)
            b3 = bf_2_3(key)
        elif level == 2:
            b1 = bf_3_1(key)
            b2 = bf_3_2(key)
            b3 = bf_3_3(key)
        else:
            b1 = b2 = b3 = U64_MINUSONE
        return b1, b2, b3

    @njit(nogil=True, locals=dict(
          key=uint64, sf=uint64))
    def insert(fltr, key, value):
        sf = get_subfilter(key)
        insert_in_subfilter(fltr, sf, key, value)

    @njit(nogil=True, locals=dict(
        key=uint64, sf=uint64))
    def lookup(fltr, key):
        sf = get_subfilter(key)
        return (lookup_in_subfilter(fltr, sf, key) == nlevels)

    @njit(nogil=True, locals=dict(
        sf=uint64, block=uint64,
        level=uint64, key=uint64,
        pos1=uint64, pos2=uint64, pos3=uint64))
    def insert_in_subfilter_in_level(fltr, sf, block, level, key, value):
        bf1, bf2, bf3 = get_hashfuncs(level, key)
        offset = subfilterbits * sf + block * blocksize + level_borders[level]
        # assert offset < filterbits
        pos1 = offset + bf1
        pos2 = offset + bf2
        pos3 = offset + bf3
        # assert pos1 < filterbits
        # assert pos2 < filterbits
        # assert pos3 < filterbits
        set_value_at(fltr, pos1, value)
        set_value_at(fltr, pos2, value)
        set_value_at(fltr, pos3, value)

    @njit(nogil=True, locals=dict(
        sf=uint64, block=uint64,
        level=uint64, key=uint64,
        pos1=uint64, pos2=uint64, pos3=uint64,
        v1=uint64, v2=uint64, v3=uint64))
    def lookup_in_subfilter_in_level(fltr, sf, block, level, key):
        bf1, bf2, bf3 = get_hashfuncs(level, key)
        offset = subfilterbits * sf + block * blocksize + level_borders[level]
        # assert offset < filterbits
        pos1 = offset + bf1
        pos2 = offset + bf2
        pos3 = offset + bf3
        # assert pos1 < filterbits
        # assert pos2 < filterbits
        # assert pos3 < filterbits
        v1 = get_value_at(fltr, pos1)
        v2 = get_value_at(fltr, pos2)
        v3 = get_value_at(fltr, pos3)
        return (v1 & v2 & v3)

    @njit(nogil=True, locals=dict(
          sf=uint64, block=uint64, level=int64, key=uint64))
    def insert_in_subfilter(fltr, sf, key, value):
        block = get_block(key)
        # assert block < nblocks_per_subfilter
        for level in range(nlevels):
            if lookup_in_subfilter_in_level(fltr, sf, block, level, key) == 0:
                insert_in_subfilter_in_level(fltr, sf, block, level, key, value)
                return level
        return int64(nlevels)

    @njit(nogil=True, locals=dict(
          sf=uint64, key=uint64, block=uint64))
    def lookup_in_subfilter(fltr, sf, key):
        block = get_block(key)
        # assert block < nblocks_per_subfilter
        for level in range(nlevels):
            if lookup_in_subfilter_in_level(fltr, sf, block, level, key) == 0:
                return level
        return nlevels

    @njit(nogil=True, locals=dict(
          sf=uint64, key=uint64, level=uint64))
    def lookup_and_insert_in_subfilter(fltr, sf, key, value=1):
        level = insert_in_subfilter(fltr, sf, key, value)
        return (level == nlevels)

    @njit(nogil=True, locals=dict(
        s0=int64, s1=int64, s2=int64, r0=int64, r1=int64, r2=int64, bv=int64, rr=int64))
    def get_fill_levels(fltr, fullstats=False):
        r0, r1, r2 = int64(0), int64(0), int64(0)
        s0, s1, s2 = int64(0), int64(0), int64(0)
        f0, f1, f2 = 0.0, 0.0, 0.0
        rowhist = np.zeros(blocksize + 1, dtype=np.int64)
        colsums = np.zeros(blocksize, dtype=np.int64)

        for sf in range(nsubfilters):
            offset = subfilterbits * sf
            for block in range(nblocks_per_subfilter):
                if nlevels >= 1:
                    r0 = popcount(fltr, offset + level_borders[0], offset + level_borders[1])
                    s0 += r0
                if nlevels >= 2:
                    r1 = popcount(fltr, offset + level_borders[1], offset + level_borders[2])
                    s1 += r1
                if nlevels >= 3:
                    r2 = popcount(fltr, offset + level_borders[2], offset + level_borders[3])
                    s2 += r2
                rowhist[int64(r0 + r1 + r2)] += 1
                if not fullstats:
                    continue
                rr = 0
                for bit in range(blocksize):
                    bv = int64(get_value_at(fltr, offset + bit))
                    colsums[bit] += bv
                    rr += bv
                if rr != (r0 + r1 + r2):
                    print(sf, block, offset, level_borders, (r0 + r1 + r2), rr, fltr[offset:offset + 8])
                    assert rr == (r0 + r1 + r2), "rr is not r0+r1+r2"
                offset += blocksize
        if nlevels >= 1:
            f0 = s0 / (nsubfilters * nblocks_per_subfilter * bits_per_level[0])
        if nlevels >= 2:
            f1 = s1 / (nsubfilters * nblocks_per_subfilter * bits_per_level[1])
        if nlevels >= 3:
            f2 = s2 / (nsubfilters * nblocks_per_subfilter * bits_per_level[2])
        colfrac = colsums / (nsubfilters * nblocks_per_subfilter)
        coltup = (colfrac[0:level_borders[1]], colfrac[level_borders[1]:level_borders[2]], colfrac[level_borders[2]:level_borders[3]])
        return (f0, f1, f2), (s0, s1, s2), rowhist, coltup

    @njit(nogil=True)
    def get_fprs(fltr):
        # TODO: DUMMY, actually compute the false positive rates for each level!
        return np.full(nlevels, -1.0, dtype=np.float64)

    array = filter.array
    update = insert
    get_value = lookup
    return create_FCFilter(locals())
