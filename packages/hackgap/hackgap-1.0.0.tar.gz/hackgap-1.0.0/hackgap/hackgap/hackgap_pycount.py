"""
fastcash/hackgap_debug.py:
count k-mers in FASTQ file(s) using a Python Counter
"""

import datetime
from collections import Counter

from ..io.fastqio import fastq_reads


_RCTABLE = bytes.maketrans(b"ACGT", b"TGCA")
def compile_canonical_kmer(rcmode, table=_RCTABLE):
    if rcmode == "max":
        def canonical_kmer(kmer):
            rc = kmer[::-1].translate(table)
            return max(kmer, rc)
    elif rcmode == "min":
        def canonical_kmer(kmer):
            rc = kmer[::-1].translate(table)
            return min(kmer, rc)
    else:
        raise NotImplementedError(f"rcmode {rcmode} not implemented")
    return canonical_kmer

# main #########################################

def main(args):
    starttime = datetime.datetime.now()
    print(f"# {starttime:%Y-%m-%d %H:%M:%S}: hackgap debug")
    source = f"FASTQ(s): {args.fastq}"
    print(f"# {starttime:%Y-%m-%d %H:%M:%S}: Using source {source}.")
    k = args.kmersize
    canonical_kmer = compile_canonical_kmer(args.rcmode)
    cnt = Counter()

    for seq in fastq_reads(args.fastq, sequences_only=True):
        n = len(seq)
        for i in range(n-k+1):
            kmer = seq[i:i+k]
            canonical = canonical_kmer(kmer)
            assert len(canonical) == k
            if len(canonical.translate(None, b"ACGT")) != 0:
                continue
            cnt[canonical] += 1
    hist = Counter(cnt.values())
    print("\nValue statistics:")
    for c in sorted(hist.keys()):
        print(f"{c}: {hist[c]}")

    endtime = datetime.datetime.now()
    elapsed = (endtime - starttime).total_seconds()
    print()
    print(f"# time sec: {elapsed:.1f}")
    print(f"# time min: {elapsed/60:.3f}")
    print(f"# {endtime:%Y-%m-%d %H:%M:%S}: Done.")
