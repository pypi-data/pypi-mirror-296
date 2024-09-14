"""
hackgap_main.py
Define subcommands for hackgap
"""

import argparse
from importlib import import_module  # dynamically import subcommand

from ..lowlevel.debug import set_debugfunctions
from ..fastcash_main import info, get_name_version_description


def count(p):
    p.add_argument("--files", "-f", metavar="FAST[AQ]", nargs="+",
        help="file(s) in which to count k-mers ([gzipped] FASTA or FASTQ)")
    p.add_argument("-o", "--out", metavar="OUTPUT_PREFIX", required=True,
        help="path/prefix of output file with k-mer count hash (required; use '/dev/null' or 'null' or 'none' to avoid output)")

    k_group = p.add_mutually_exclusive_group(required=True)
    k_group.add_argument('-k', '--kmersize', dest="mask", metavar="INT",
        type=int, help="k-mer size")
    k_group.add_argument('--mask', metavar="MASK",
        help="gapped k-mer mask (quoted string like '#__##_##__#')")
    p.add_argument("-n", "--nobjects", type=int,
        metavar="INT", required=True,
        help="number of objects to be stored")
    p.add_argument('--maxcount', '-M', type=int,
        default=65535, metavar="INT",
        help="maximum count value [65535]; should be 2**N - 1 for some N")

    p.add_argument("--filtersizes", "-s", nargs="+",
        metavar="GB", type=float,  # no default!
        help="size of filter(s) in gigabytes, up to 3 filter levels. "
            "For counting without filtering, do not specify this option.")
    p.add_argument("--filterfiles", "-F", metavar="FAST[AQ]", nargs="+",
        help="optionally, different file(s) to populate filters ([gzipped] FASTA or FASTQ); "
            "the default and typical use case is to use the same files as for counting, "
            "so usually, you do not want to use this option.")

    p.add_argument("--rcmode", metavar="MODE", default="max",
        choices=("f", "r", "both", "min", "max"),
        help="mode specifying how to encode k-mers")
    p.add_argument("--markweak", action="store_true",
        help="mark weak vs. strong k-mers after counting (slow)")
    p.add_argument("--statistics", "--stats",
        choices=("none", "summary", "details", "full"), default="summary",
        help="statistics level of detail (none, *summary*, details, full (all subtables))")
    p.add_argument("--shortcutbits", "-S", metavar="INT", type=int,
        choices=(0, 1, 2), default=0,
        # help="number of shortcut bits (0,1,2), default: 0")
        help=argparse.SUPPRESS)
    p.add_argument("--type", default="default",
        # help="hash type (e.g. [s]3c_fbcbvb, 2v_fbcbvb), implemented in hash_{TYPE}.py")
        help=argparse.SUPPRESS)
    p.add_argument("--unaligned", action="store_const",
        const=False, dest="aligned", default=None,
        help="use unaligned buckets (smaller, slightly slower; default)")
    p.add_argument("--aligned", action="store_const",
        const=True, dest="aligned", default=None,
        help="use power-of-two aligned buckets (faster, but larger)")
    p.add_argument("--hashfunctions", "--functions", default="random",
        help="hash functions: 'default', 'random', or func0:func1:func2:func3")
    p.add_argument("--bucketsize", "-b", "-p", type=int, default=6, metavar="INT",
        help="bucket size, i.e. number of elements on a bucket")
    p.add_argument("--fill", type=float, default=0.9, metavar="FLOAT",
        help="desired fill rate of the hash table")
    p.add_argument("--subtables", type=int, metavar="INT",  # 9?
        help="number of subtables used; subtables+1 threads are used")
    p.add_argument("--threads-read", type=int, metavar="INT",  # 2?
        help="number of reader threads")
    p.add_argument("--threads-split", type=int, metavar="INT",  # 4?
        help="number of splitter threads")

    # less important hash options
    p.add_argument("--maxwalk", metavar="INT", type=int, default=500,
        help="maximum length of random walk through hash table before failing [500]")
    p.add_argument("--walkseed", type=int, default=7, metavar="INT",
        help="seed for random walks while inserting elements [7]")
    p.add_argument("--maxfailures", metavar="INT", type=int, default=0,
        help="continue even after this many failures [default:0; forever:-1]")


def countwith(p):
    p.add_argument("--files", "-f", metavar="FAST[AQ]", nargs="+",
        help="file(s) in which to count k-mers ([gzipped] FASTA or FASTQ)")
    p.add_argument("-o", "--out", metavar="OUTPUT_PREFIX", required=True,
        help="path/prefix of output file with k-mer count hash (required; use '/dev/null' or 'null' or 'none' to avoid output)")
    p.add_argument("--index", metavar="INPUT_PREFIX", required=True,
        help="path/prefix of the existing index which should be used for counting")
    p.add_argument("--threads-read", type=int, metavar="INT",  # 2?
        help="number of reader threads")
    p.add_argument("--threads-split", type=int, metavar="INT",  # 4?
        help="number of splitter threads")
    p.add_argument("--statistics", "--stats",
        choices=("none", "summary", "details", "full"), default="summary",
        help="statistics level of detail (none, *summary*, details, full (all subtables))")


def pycount(p):
    p.add_argument('-k', '--kmersize', metavar="INT", type=int, default=27,
        help="k-mer size")
    p.add_argument("--rcmode", metavar="MODE", default="max",
        choices=("f", "r", "both", "min", "max"),
        help="mode specifying how to encode k-mers")
    p.add_argument("--fastq", "-q", metavar="FASTQ", nargs="+",
        help="FASTQ file(s) to index and count",
        required=True)
    p.add_argument("-o", "--out", metavar="OUTPUT_PREFIX",
        help="name of output file (dummy, unused)")


# main argument parser ################################

SUBCOMMANDS = [
    ("count",
     "count (possibly filtered) k-mers in (possibly compressed) FASTA or FASTQ files",
     count,
     ".hackgap_count", "main",
     ),
    ("countwith",
     "count k-mers using an existing precomputed index",
     countwith,
     ".hackgap_count", "main"),
    ("pycount",
     "count k-mers in FASTQ files using pure Python",
     pycount,
     ".hackgap_pycount", "main",
     ),
    ("info",
     "collect and show information about saved hash tables with k-mer counts",
     info,
     "..fastcash_info", "main",
     ),
]


def get_argument_parser():
    """
    return an ArgumentParser object
    that describes the command line interface (CLI)
    of this application
    """
    NAME, VERSION, DESCRIPTION = get_name_version_description(__package__, __file__)
    p = argparse.ArgumentParser(
        description=DESCRIPTION,
        epilog="by Algorithmic Bioinformatics, Saarland University."
        )
    p.add_argument("--version", action="version", version=VERSION,
        help="show version and exit")
    p.add_argument("--debug", "-D", action="count", default=0,
        help="output debugging information (repeat for more)")

    # add subcommands to parser
    subcommands = SUBCOMMANDS
    sps = p.add_subparsers(
        description=f"The {NAME} application supports the commands below. "
            f"Run '{NAME} COMMAND --help' for detailed information on each command.",
        metavar="COMMAND")
    sps.required = True
    sps.dest = 'subcommand'
    for (name, helptext, f_parser, module, f_main) in subcommands:
        if name.endswith('!'):
            name = name[:-1]
            chandler = 'resolve'
        else:
            chandler = 'error'
        sp = sps.add_parser(name, help=helptext,
            description=f_parser.__doc__, conflict_handler=chandler)
        sp.set_defaults(func=(module, f_main))
        f_parser(sp)
    return p


def main(args=None):
    p = get_argument_parser()
    pargs = p.parse_args() if args is None else p.parse_args(args)
    set_debugfunctions(debug=pargs.debug, timestamps=pargs.debug)
    # set_threads(pargs, "threads")  # limit number of threads in numba/prange
    (module, f_main) = pargs.func
    m = import_module(module, __package__)
    mymain = getattr(m, f_main)
    mymain(pargs)


if __name__ == "__main__":
    main()
