# DESCRIPTION

hackgap (**ha**sh-based **c**ounting of **k**-mers with **gap**s) provides a fast jit-compiled *k*-kmer counter which supports gapped *k*-mers.


# INSTALLATION

### Installation via Conda or PyPi

The hackgap package is available via conda or PyPi. To install it run one of the following commands:
**PyPi**
`pip install hackgap`
**Conda**
`conda install -c bioconda hackgap`

### Manual installation
#### Install the conda package manager (miniforge)
Go to https://conda-forge.org/miniforge/ and download the Miniforge installer:
Follow the instructions of the installer and append the mamba executable to your PATH (even if the installer does not recommend it).
You can let the installer do it, or do it manually by editing your ``.bashrc`` or similar file under Linux or MacOS, or by editing the environment variables under Windows.
To verify that the installation works, open a new terminal and execute
```
mamba --version
python --version
```

#### Obtain or update hackgap
You can obtain hackgap by cloning this public git repository:
```
git clone https://gitlab.com/rahmannlab/hackgap.git
```

If you need to update hackgap later, you can do so by just executing
```
git pull
```
within the cloned directory tree.


#### Create and activate a conda environment
To run our software, a conda environment with the required libraries needs to be created.
A list of needed libraries is provided in the ``environment.yml`` file in the cloned repository;
it can be used to create a new environment:
```
cd hackgap  # the directory of the cloned repository
mamba env create
```
which will create an environment named ``hackgap`` with the required dependencies,
using the provided ``environment.yml`` file in the same directory.

To activate the newly created environment run
```
mamba activate hackgap
```

#### Install hackgap
To install hackgap we use the package installer for Python pip.

Run the following command to install hackgap.
```
pip install -e .
```

To check if the installation was a success execute
```
hackgap -v # should be 1.0.0 or higher
```
# Usage guide

hackgap is a command line tool which has multiple parameters you can adjust.
You can get a list of all parameters by running `hackgap count --help`.

## The required parameters are:
- `-o` or `--output`: This parameter specifies the index name and the path at which it is stored.
- `-n` or `--nobjects`: hackgap uses a in memory hash table to store the *k*-mers and the corresponding counts. For this you have to provide an estimated number of distinct *k*-mers. If the table is too small, you have to rerun the counting using a bigger table.
- `-k` or `--mask`: hackgap is the only *k*-mer counter which supports gapped *k*-mers (or spaced seeds). The corresponding masks can be provided via the `--mask` parameter. A significant position is defined by a `#` and a insignificant position by an `_`. An example mask with k=25 (significant positions) and w=31 (window size) would be `--mask "####_####_###_###_###_####_####"`. We only support masks with $k\leq 31$. If you want to count contiguous *k*-mers you can specify the *k* by using the `-k` parameter.
- `--files`: This parameter specifies the input files in which the *k*-mers are counted. We support reading FASTA and FASTQ files uncompressed or compressed via `gzip`, `xz` or `bzip2` (The required tools for decompressing the files are dependencies in the environment).

## Parameters for parallelization:
To improve the speed of hackgap, we implemented a producer-consumer method in addition to our parallelized hash table. You can modify multiple parameter depending on your hardware and the number of files you want to count.
- `--subtables`: Defines how many threads are used to insert *k*-mers into the table. If you have enough cores it scales well for up to 15 subtables.
- `--threads-split`: The number of threads which translates the sequence data into 2 bit encoding and splits it into *k*-mers. 2-3 threads are recommended.
- `--threads-read`: The number of threads used to read the input files. If you count more than one file, you can increase the number of reads. Normally at most 2-3 readers are enough to provide enough data to the threads splitting to sequence into *k*-mers and inserting the *k*-mers into the table.

## Parameters for filtering:
With version 1.0 we introduced a hierarchical 3 level bloom-filter which can be used to exclude *k*-mers which only occurs less than 3 times. For this the input files are processed twice. First to create the filter and in the second run only *k*-mers are counted which passed through the filter.
For this you have to provide two parameters:
- `--filtersize`: This parameter takes up to 3 integer values. Each describes the size of one level of a filter in GB. The first one should be larger than the second one and the third one should be the smallest.
- `--filterfiles`: These are sequence files which are used to fill the filter. These are usually the same files which are used to count the *kk*-mers, but can also be different data.

## Additional parameters:
- `--maxcount`: defines the maximal counter value.
- `--markweak`: This marks all *k*-mers with a HAmming distance of one. This is done after counting the *k*-mers and needs additional time and memory.



# Example

Here we will provide a small example how to run hackgap on the t2t reference.

## Download reference genome

First we need to download the t2t reference (https://s3-us-west-2.amazonaws.com/human-pangenomics/T2T/CHM13/assemblies/analysis_set/chm13v2.0.fa.gz)

```
mkdir data # create data folder
cd data
wget https://s3-us-west-2.amazonaws.com/human-pangenomics/T2T/CHM13/assemblies/analysis_set/chm13v2.0.fa.gz
cd ..
```

## Run hackgap
To execute hackgap we need to provide:
- `-n`: the expected number of distinct *k*-mers
- `-k`: for contiguous or `-mask` for gapped: the *k*-mer shape
- `--fasta`: the uncompressed input file using `pigz` or `zcat`
- `-o`: the output file in `zarr` format

```
hackgap count -n 2391456540 -k 25 --files data/chm13v2.0.fa.gz -o t2t-k25
```

```
hackgap count -n 2416328905 --mask "####_####_###_###_###_####_####" --files data/chm13v2.0.fa.gz -o t2t-m2
```

# Citation
If you use hackgap, please cite the article in the WABI 2022 proceedings:
```
@inproceedings{DBLP:conf/wabi/ZentgrafR22,
  author       = {Jens Zentgraf and
                  Sven Rahmann},
  editor       = {Christina Boucher and
                  Sven Rahmann},
  title        = {Fast Gapped k-mer Counting with Subdivided Multi-Way Bucketed Cuckoo
                  Hash Tables},
  booktitle    = {22nd International Workshop on Algorithms in Bioinformatics, {WABI}
                  2022, September 5-7, 2022, Potsdam, Germany},
  series       = {LIPIcs},
  volume       = {242},
  pages        = {12:1--12:20},
  publisher    = {Schloss Dagstuhl - Leibniz-Zentrum f{\"{u}}r Informatik},
  year         = {2022},
  url          = {https://doi.org/10.4230/LIPIcs.WABI.2022.12},
  doi          = {10.4230/LIPICS.WABI.2022.12},
  timestamp    = {Wed, 21 Aug 2024 22:46:00 +0200},
  biburl       = {https://dblp.org/rec/conf/wabi/ZentgrafR22.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}


```