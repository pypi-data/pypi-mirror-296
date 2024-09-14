"""
fastcash/hackgap/hackgap_count.py:
count k-mers in FASTA or FASTQ file(s), optionally with pre-filter(s)

in fastcash/data, run this:

# ecoli test .fq.gz data: 25-mers: 384_478_810 (37_247_299 distinct), no filter vs. 2 filters
hackgap -DD count --files ecoli_DRR*.gz -o ecoli-25-all -k 25 -n 40_000_000 --subtables  9 --threads-read 2 --threads-split 3 --statistics details --maxcount 15
hackgap -DD count --files ecoli_DRR*.gz -o ecoli-25-fil -k 25 -n  5_000_000 --subtables 21 --threads-read 2 --threads-split 4 --statistics details --maxcount 15 --filtersizes 0.02 0.006 0.003

# same for 27-mers, no filter vs. 3 filters
hackgap -DD count --files ecoli_DRR*.gz -o ecoli-27-all -k 27 -n 40_000_000 --subtables 9 --threads-read 2 --threads-split 3 --statistics details --maxcount 15
hackgap -DD count --files ecoli_DRR*.gz -o ecoli-27-fil -k 27 -n 10_000_000 --subtables 9 --threads-read 2 --threads-split 3 --statistics details --maxcount 15 --filtersizes 00.02 0.006 0.003

# other tests (personal genome):
hackgap -D count --files /scratch/rahmann/*.fastq.gz  --out null   -k 27 -n 2_700_000_000 --subtables 25 --threads-read 2 --threads-split 4 --statistics details --maxcount 63 --filtersizes 4.5 1.8 1.5
hackgap -D count --files /scratch/rahmann/*.fastq.gz  --out all-25 -k 25 -n 6_587_359_683 --fill 0.9 --maxcount 63 --statistics summary -b 4 --subtables 25 --threads-read 2 --threads-split 4
"""


import sys
import os
from math import ceil
from importlib import import_module

import numpy as np
from numpy.random import randint
from numpy.random import seed as randomseed

from ..lowlevel import debug
from ..lowlevel.conpro import ConsumerProducer, CPInputMode, run_cps, diagnose_wait_times
from ..mathutils import print_histogram  # print_histogram_tail
from ..srhash import get_nbuckets, print_statistics
from ..io.hashio import save_hash, load_hash
from ..io.generalio import cptask_read_file
from ..cptasks_kmers import (
    compile_cptask_scatter_kmers_from_linemarked,
    compile_cptask_insert_filtered_subkeys,
    compile_cptask_update_existing_subkeys,
    )
from ..parameters import get_valueset_and_parameters, parse_parameters
from ..filter_bi_b3c import build_filter
from ..mask import create_mask
from ..subtable_hashfunctions import (
    hashfunc_tuple_from_str,
    compile_get_subtable_subkey_from_key,
    )
from .hackgap_weak import calculate_weak_set


DEFAULT_HASHTYPE = "s3c_fbcbvb"


def check_basic_parameters(args):
    if not args.markweak:
        valueinfo = ("count", str(args.maxcount + 1))
    else:
        valueinfo = ("countweak", str(args.maxcount + 1))
    (values, _, rcmode, mask) = get_valueset_and_parameters(
        valueinfo, mask=args.mask, rcmode=args.rcmode)
    k = mask.k
    if not isinstance(k, int):
        debugprint0(f"- Error: k-mer size {k=} not an integer")
        sys.exit(1)
    debugprint1(f"- value set: {valueinfo}")
    return (values, valueinfo, rcmode, mask)


def check_threads(args):
    adjust = (args.subtables is None) or (args.threads_split is None) or (args.threads_read is None)
    # 1. Define number of subtables
    cpus = os.cpu_count()
    subtables = args.subtables
    if subtables is None:
        subtables = max(min(cpus // 2 - 1, cpus - 3, 19), 1)
        if (subtables % 2) == 0:
            subtables += 1
    if subtables < 1:
        debugprint0(f"- Error: At least one subtable is required, but {subtables=}")
        sys.exit(1)
    if subtables % 2 == 0:
        debugprint0(f"- Error: Number of subtables must be odd, but {subtables=}")
        sys.exit(1)
    # 2. Define threads for reading files
    threads_read = args.threads_read
    if threads_read is None:
        threads_read = int(ceil(subtables / 10))  # who knows?
    # 3. Define threads for
    threads_split = args.threads_split
    if threads_split is None:
        threads_split = 2 * threads_read
    if adjust and (subtables + threads_read + threads_split >= cpus):
        threads_read = 1
        threads_split = 2
    # 4. Return results
    assert threads_read >= 1
    assert threads_split >= 1
    return (subtables, threads_read, threads_split)


def check_filtersizes(args):
    fs = args.filtersizes
    if fs is None:
        if args.filterfiles is not None:
            debugprint0("- Error: No filter sizes were specified, but filter files were given.")
            sys.exit(1)
        return None, None
    else:
        if not (1 <= len(fs) <= 3):
            debugprint0(f"- Error: Only 1 to 3 levels of filters are supported, but {len(fs)} sizes were given: {fs}.")
            sys.exit(1)
        if any(s <= 0.0 for s in fs):
            jfs = " ".join(map(str, fs))
            debugprint0(f"- Error: Each filter size in GiB must be strictly positive in '--filtersizes {jfs}'.")
            sys.exit(1)
        files = args.filterfiles if args.filterfiles is not None else args.files
    return fs, files


def initialize_hashtable(args, hashtype, universe, subtables, values, h0):
    parameters = parse_parameters(None, args)
    (nobjects, hashtype, aligned, hashfunc_str, bucketsize, nfingerprints, fill) = parameters
    debugprint2(f"- Parameters: {parameters}")

    if hashtype == "default":
        hashtype = DEFAULT_HASHTYPE
    debugprint1(f"- using hash type '{hashtype}'.")
    hashmodule = import_module("..hash_" + hashtype, __package__)
    build_hash = hashmodule.build_hash
    nvalues = values.NVALUES
    update_value = values.update
    n = get_nbuckets(nobjects, bucketsize, fill) * bucketsize
    debugprint1(f"- allocating hash table (with {subtables} subtables) for {n=} objects in total.")
    debugprint1(f"- hash function string: '{hashfunc_str}'...")
    h = build_hash(universe, n, subtables, bucketsize,
        hashfunc_str, nvalues, update_value,
        aligned=aligned, nfingerprints=nfingerprints,
        maxwalk=args.maxwalk, shortcutbits=args.shortcutbits,
        force_h0=h0)
    return h


def create_new_index(nsubtables, args):
    """
    Initialize a filter and a hash table.
    Make sure they have the same 0-th hash function mapping to subtables.
    """
    (values, valueinfo, rcmode, mask) = check_basic_parameters(args)
    h0 = hashfunc_tuple_from_str(args.hashfunctions, number=1, mod_value=nsubtables)[0]
    universe = int(4 ** mask.k)
    sizes, filterfiles = check_filtersizes(args)
    if sizes:
        levelhfs = [("random", "random", "random") for _ in sizes]
        fltr = build_filter(universe, sizes, nsubtables, (h0, "random"), levelhfs)
        debugprint0(f"- memory for filter: {fltr.mem_bytes / (2**30):.3f} GiB")
    else:
        fltr = None
    h = initialize_hashtable(args, args.type, universe, nsubtables, values, h0)
    debugprint0(f"- memory for hash table: {h.mem_bytes / (2**30):.3f} GiB")
    if not args.walkseed:
        args.walkseed = randint(0, high=2**32 - 1, dtype=np.uint64)
    randomseed(args.walkseed)
    debugprint2(f"- walkseed: {args.walkseed}")
    return (h, fltr, values, valueinfo, mask, rcmode)


def load_exisiting_hash(hashname):
    h, values, infotup = load_hash(hashname)
    (hashinfo, valueinfo, optinfo, appinfo) = infotup
    mask = create_mask(appinfo['mask'])
    rcmode = appinfo.get('rcmode', values.RCMODE)
    if not isinstance(rcmode, str):
        rcmode = rcmode.decode("ASCII")
    return (h, None, values, valueinfo, mask, rcmode, infotup)


def process_files(stage, fltr, h, fnames, mask, rcmode, *,
        maxfailures=0, maxwalk=1000,
        threads_read=1, threads_split=1, countvalue=1):

    # 1. Define jobs to read files
    read_jobs = ConsumerProducer(
        name='file_reader',
        tasks=[(cptask_read_file, fname, None, mask.w) for fname in fnames],
        nworkers=threads_read,
        noutbuffers_per_worker=(4 * threads_split),
        specific_outbuffers_per_worker=True,
        datatype=np.uint8,
        infotype=np.int64,
        dataitems_per_buffer=2**16,
        infoitems_per_buffer=(2**16 // 200),
        infoitemsize=4,  # linemarks use 4 numbers per sequence
        )

    # 2. Define jobs to split k-mers
    _universe = 4**(mask.k)
    nsubtables = h.subtables
    if fltr is not None:
        assert nsubtables == fltr.nsubfilters
    hf0 = h.hashfuncs.split(":")[0]
    (hashfunc0, _) = compile_get_subtable_subkey_from_key(hf0, _universe, nsubtables)

    n_splitter_jobs = threads_split
    nbuffers_per_worker_per_subtable = 4  # 3!
    nbuffers_per_subtable = n_splitter_jobs * nbuffers_per_worker_per_subtable
    outbufsize = 2**16  # 2**16
    cptask_split = compile_cptask_scatter_kmers_from_linemarked(
        mask, rcmode, hashfunc0,
        nsubtables, nbuffers_per_subtable, outbufsize)

    splitter_jobs = ConsumerProducer(
        name='kmer_splitter',
        input=read_jobs,
        tasks=[(cptask_split, )] * n_splitter_jobs,
        noutbuffers_per_worker=(nsubtables * nbuffers_per_worker_per_subtable),
        datatype=np.uint64,
        dataitems_per_buffer=outbufsize,
        dataitemsize=1,
        )
    # in0 = [splitter_jobs.inbuffers, splitter_jobs.incontrol, splitter_jobs.ininfos]
    # out0 = [splitter_jobs.outbuffers[0], splitter_jobs.outcontrol[0], splitter_jobs.outinfos[0]]

    # 3. Define inserter jobs (one per subfilter/subtable)
    if stage == 1:
        # filter k-mers
        constant_value = countvalue if (fltr is None) else 0
        cptask_insert = compile_cptask_insert_filtered_subkeys(
            h, fltr, constant_value, maxfailures, maxwalk)
        ht = h.hashtable
        fa = fltr.array if fltr is not None else None
        actual_jobs = ConsumerProducer(
            name='kmer_filter_inserter',
            input=splitter_jobs,
            input_mode=(CPInputMode.GATHER, nbuffers_per_subtable),
            tasks=[(cptask_insert, st, ht, fa) for st in range(nsubtables)],
            noutbuffers_per_worker=1,
            specific_outbuffers_per_worker=True,
            datatype=np.int64,
            dataitems_per_buffer=(maxwalk + 12),
            dataitemsize=1,
            )
        # in0 = [actual_jobs.inbuffers, actual_jobs.incontrol, actual_jobs.ininfos]
        # out0 = [actual_jobs.outbuffers[0], actual_jobs.outcontrol[0], actual_jobs.outinfos[0]]
    elif stage == 2:
        # count k-mers
        constant_value = countvalue
        cptask_insert = compile_cptask_update_existing_subkeys(h, constant_value)
        ht = h.hashtable
        actual_jobs = ConsumerProducer(
            name='kmer_counter',
            input=splitter_jobs,
            input_mode=(CPInputMode.GATHER, nbuffers_per_subtable),
            tasks=[(cptask_insert, st, ht) for st in range(nsubtables)],
            noutbuffers_per_worker=0,
            )
        # in0 = [actual_jobs.inbuffers, actual_jobs.incontrol, actual_jobs.ininfos]
        # out0 = [actual_jobs.outbuffers, actual_jobs.outcontrol, actual_jobs.outinfos]
    else:
        debugprint0(f"- Error: illegal {stage=}")
        sys.exit(1)

    # pre-compilation attempt (job 0 only)
    # make sure that find_buffer_for_reading(incontrol, nactive) immediately returns -1
    # tprec = timestamp1(msg="- hackgap count process_files: precompiling...")
    # f0, a0 = actual_jobs._funcs[0], actual_jobs._args[0]
    # _BC_FINISHED = 4
    # in0[1] = np.full_like(in0[1], _BC_FINISHED)
    # out0[1] = np.full_like(out0[1], _BC_FINISHED)
    # _ = f0(0, 0, *a0, *in0, *out0)
    # timestamp1(tprec, "- hackgap count process_files: done precompiling")

    # run the ConsumerProducers together
    debugprint1("- hackgap count process_files: will now run several ConsumerProducers")
    failures = run_cps(read_jobs, splitter_jobs, actual_jobs)
    debugprint1(f"- hackgap count process_files: done; {failures=}")
    diagnose_wait_times(read_jobs, splitter_jobs, actual_jobs)
    return (failures == 0) if stage == 1 else True


# main #########################################

def main(args):
    global debugprint0, debugprint1, debugprint2
    global timestamp0, timestamp1, timestamp2
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp
    starttime = timestamp0(msg="\n# hackgap count")

    if "index" in args:
        # pre-load an existing index
        (h, fltr, values, valueinfo, mask, rcmode, infotup) = load_exisiting_hash(args.index)
        (hashinfo, valueinfo, optinfo, appinfo) = infotup
        maxfailures = np.uint64(np.iinfo(np.uint64).max)  # is this a dummy?
        maxwalk = 0
        walkseed = optinfo["walkseed"]
        args.subtables = h.subtables
        nsubtables, threads_read, threads_split = check_threads(args)
        debugprint1(f"- threads: {nsubtables=}, {threads_read=}, {threads_split=}")
        show_values = False
    else:
        # create a new index
        nsubtables, threads_read, threads_split = check_threads(args)
        debugprint1(f"- threads: {nsubtables=}, {threads_read=}, {threads_split=}")
        (h, fltr, values, valueinfo, mask, rcmode) = create_new_index(nsubtables, args)
        maxfailures, maxwalk = args.maxfailures, args.maxwalk
        walkseed = args.walkseed
        show_values = True

    countvalue = getattr(values, "countvalue", 1)
    assert isinstance(rcmode, str), "ERROR: rcmode is not a str."

    if fltr is not None:
        # Populate filters, and then count with filters
        filterstart = timestamp0(msg="\n## Filtering")
        files = args.filterfiles if args.filterfiles is not None else args.files
        debugprint0(f"- populating {fltr.nlevels}-level filter ({fltr.nsubfilters} subfilters)")
        debugprint0(f"- files for filtering: {files}")
        sys.stdout.flush()
        success = process_files(1, fltr, h, files, mask, rcmode,
            maxfailures=maxfailures, maxwalk=maxwalk,
            threads_read=threads_read, threads_split=threads_split,
            countvalue=countvalue)
        timestamp0(filterstart, msg="- Filtering wall time [sec]")
        timestamp0(filterstart, msg="- Filtering wall time [min]", minutes=True)
        sys.stdout.flush()
        if args.statistics in ("details", "full"):
            filterstatsstart = timestamp0(msg="- collecting filter statistics...")
            fullstats = (args.statistics == "full")
            fills, absfills, *details = fltr.get_fill_levels(fltr.array, fullstats=fullstats)
            debugprint0(f"- filter load factors: {fills[0]:.4f}, {fills[1]:.4f}, {fills[2]:.4f}")
            debugprint0(f"- filter one bits: {absfills}")
            if fullstats:
                rowhist, colfills = details
                print_histogram(rowhist, title="\n### Filter row load statistics", shorttitle="filterrowfill", fractions="%")
                for lvl, colfill in enumerate(colfills):
                    if fills[lvl] == 0.0:
                        continue
                    debugprint0(f"### Filter level {lvl} column load factors")
                    for col, load in enumerate(colfill):
                        debugprint0(f"- column {col}: {load:.1%}")
                    debugprint0()
            timestamp0(filterstatsstart, msg="- time for collecting filter statistics [sec]")
            sys.stdout.flush()

        if not success:
            debugprint0("- filtering FAILED.")
            debugprint0(f"- output file '{args.out}' was NOT written.")
            timestamp0(starttime, msg="- FAILED; total time [sec]")
            timestamp0(starttime, msg="- FAILED; total time [min]", minutes=True)
            sys.exit(1)

        # DEBUG:
        # print_statistics(h, level=args.statistics, show_values=show_values)

        # Count k-mers in files
        countstart = timestamp0(msg="\n## Counting")
        files = args.files
        debugprint0(f"- counting {(mask.k, mask.w)}-mers with mask '{mask.mask}' using {h.subtables} subtables,")
        debugprint0(f"- files for counting: {files}")
        sys.stdout.flush()
        process_files(2, fltr, h, files, mask, rcmode,
            maxfailures=maxfailures, maxwalk=maxwalk,
            threads_read=threads_read, threads_split=threads_split,
            countvalue=countvalue)
        timestamp0(countstart, msg="- filtered counting: wall time [sec]")
        timestamp0(countstart, msg="- filtered counting: wall time [min]", minutes=True)
    else:
        stage = 2 if "index" in args else 1
        # Count directly
        debugprint0("- Running without filters")
        countstart = timestamp0(msg="\n## Counting")
        debugprint0(f"- counting {(mask.k, mask.w)}-mers with mask '{mask.mask}' using {h.subtables} subtables,")
        files = args.files
        debugprint0(f"- files for counting: {files}")
        sys.stdout.flush()
        if files is None:
            debugprint0("- nothing to do; no files given.")
            sys.exit(0)
        success = process_files(stage, None, h, files, mask, rcmode,
            maxfailures=maxfailures, maxwalk=maxwalk,
            threads_read=threads_read, threads_split=threads_split,
            countvalue=countvalue)
        timestamp0(countstart, msg="- unfiltered counting: wall time [sec]")
        timestamp0(countstart, msg="- unfiltered counting: wall time [min]", minutes=True)
        if not success:
            debugprint0("- counting FAILED.")
            debugprint0(f"- output file '{args.out}' was NOT written.")
            timestamp0(starttime, msg="- FAILED; total time [sec]")
            timestamp0(starttime, msg="- FAILED; total time [min]", minutes=True)
            sys.exit(1)
    sys.stdout.flush()

    # mark weak k-mers if desired
    k = mask.k
    if "index" not in args and args.markweak:
        startweak = timestamp0(msg='\n## Weak k-mers')
        group_prefix_length, nextchars = 2, 2
        sys.stdout.flush()
        calculate_weak_set(h, k, group_prefix_length, nextchars, rcmode=rcmode, threads=args.subtables)
        timestamp0(startweak, msg="- weak k-mers: wall time [sec]")
        timestamp0(startweak, msg="- weak k-mers: wall time [min]", minutes=True)
        sys.stdout.flush()

    # calculate shortcut bits
    # scb = args.shortcutbits
    # if scb > 0:
    #     startshort = timestamp0(msg=f'## Shortcut bits (level {scb})...')
    #     h.compute_shortcut_bits(h.hashtable)
    #     timestamp0(startshort, msg="- Shortcut bits: wall time [sec]")
    #     timestamp0(startshort, msg="- Shortcut bits: wall time [min]", minutes=True)

    # write output file
    optinfo = dict(walkseed=walkseed, maxwalk=maxwalk, maxfailures=maxfailures)
    appinfo = dict(rcmode=rcmode, mask=mask.tuple, k=k)
    save_hash(args.out, h, valueinfo, optinfo, appinfo)

    # compute and show statistics if desired
    print_statistics(h, level=args.statistics, show_values=show_values)

    # that's it; successfully exit the program
    timestamp0(starttime, msg="- SUCCESS; total time")
    timestamp0(starttime, msg="- SUCCESS; total time", minutes=True)
