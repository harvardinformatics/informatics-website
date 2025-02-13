---
title: Whole genome alignment with Cactus
---

Comparative genomics requires alignments between sequences from different populations or species. While alignment of small chunks of sequence (e.g. genes) between many species is relatively straightforward, whole genome alignment has been challenging. The [Cactus genome alignment software](https://github.com/ComparativeGenomicsToolkit/cactus) and its [associated tools](https://github.com/ComparativeGenomicsToolkit) has made this task feasible for up to hundreds of genomes. However, running the whole pipeline can still be difficult. Here we have developed a [Snakemake](https://snakemake.readthedocs.io/en/stable/) pipeline to facilitate running Cactus on a computing cluster. This is done by first running the `cactus-prepare` command to generate the Cactus labeled phylogeny, which is used to guide the submission of jobs to the cluster.

## Getting started

You will need several things to be able to run this pipeline:

1. A computing cluster that uses the [SLURM](https://slurm.schedmd.com/overview.html), though it should be possible to extend it to [any job scheduler that Snakemake supports](https://github.com/snakemake?q=executor&type=all&language=&sort=).
2. conda or mamba to install software. See: [Installing command line software](installing-command-line-software.md) if you don't have conda/mamba installed.
2. [Snakemake](https://snakemake.readthedocs.io/en/stable/) and the [Snakemake SLURM plugin](https://anaconda.org/bioconda/snakemake-executor-plugin-slurm)
3. Singularity - **The pipeline itself will automatically download the latest version of the Cactus singularity container for you.**
4. The [Harvard Informatics cactus-snakemake pipeline](https://github.com/harvardinformatics/cactus-snakemake/)

### Creating an enviornment for the cactus pipeline

We recommend **creating a conda environment** to install software:

```bash
mamba create -n cactus-env
mamba activate cactus-env
mamba install bioconda::snakemake-minimal
mamba install bioconda::snakemake-executor-plugin-slurm # For SLURM clusters
```

Some clusters (such as the Harvard cluster) already have Singularity installed. You should check by running the command:

```bash
singularity
```
If the help menu displays, you already have Singularity installed. If not, you will need to install it yourself into your cactus-env environment:

```bash
mamba install conda-forge::singularity
```

### Downloading the cactus-snakemake pipeline

The [pipeline](https://github.com/harvardinformatics/cactus-snakemake/) is currently available on github. You can install it on the Harvard cluster or any computer that has `git` installed by navigating to the directory in which you want to download it and doing one of the following:

#### Using git with HTTPS

```bash
git clone https://github.com/harvardinformatics/cactus-snakemake.git
```

#### Using git with SSH

Alternatively, if you have SSH setup on github, you would type:

```bash
git clone git@github.com:harvardinformatics/cactus-snakemake.git
```

#### Using wget (without git)

If you don't have or don't wish to use git, you can directly download a ZIP archive of the repository:

```bash
wget https://github.com/harvardinformatics/cactus-snakemake/archive/refs/heads/main.zip
unzip cactus-snakemake
```

With that, you should be ready to set-up your data for the pipeline!

## Inputs you need to prepare

To run this pipeline, you will need:

1. A **rooted** phylogenetic tree of all species to align, with or without branch lengths, in [Newick format](https://en.wikipedia.org/wiki/Newick_format).
2. The genome [FASTA](https://en.wikipedia.org/wiki/FASTA_format) files for each species.

You will use these to creat the input file for Cactus.

### Preparing the Cactus input file

The various Cactus commands depend on a single input file with information about the genomes to align. This file is a simple tab delimited file. 

The first line of the file contains the **rooted** input species tree in [Newick format](https://en.wikipedia.org/wiki/Newick_format) and nothing else (be sure to remember the semi-colon at the end of the Newick tree!).

Each subsequent line contains in the first column one tip label from the tree and in the second column the path to the genome FASTA file for that species. 

!!! warning "The FASTA files must be decompressed for Cactus to read them"

    If you provide compressed FASTA files, Cactus will not be able to run and you will get an error. Be sure to decompress the FASTA files with the appropriate decomrpession tool (e.g. `gunzip` for .gz files).

For example, if one were running this pipeline on 5 species named A, B, C, D, and E, the input file may look something like this:

```
(((A,B),(C,D)),E);
A   seqdir/a.fa
B   seqdir/b.fa
C   seqdir/c.fa
D   seqdir/d.fa
E   seqdir/e.fa
```

Cactus provides a small chunk of a mammal chromosome (human chromosome 6) as test data, and you can find that data, along with the input file in the `tests/` folder of the cactus-snakemake repository.

### Preparing the Snakemake config file

Besides the sequence input, the pipeline needs some extra configuration to know where to look for files and write output. That is done in the Snakemake configuration file for a given run. An example configuration file for some test data is [here](). It should look something like this:

```
working_dir: <working_dir>

cactus_path: <cactus_path>

input_file: <input_file>

output_dir: <output_dir>

overwrite_output_dir: <True/False>

final_hal: <final .hal file with all genomes appended>

tmp_dir: <tmp_dir>

use_gpu: <True/False>
```

Simply replace the string surrounded by <> with the path or option desired. Below is a table summarizing these options:

| Option               | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `working_dir`        | Directory where cactus will be downloaded and run                           |
| `cactus_path`        | Path to the Cactus Singularity image. If blank or 'download', the image of the latest Cactus version will be downloaded and used. |
| `input_file`         | Path to the input file containing the species tree and genome paths (described above) |
| `output_dir`         | Directory where the all output will be written                            |
| `overwrite_output_dir` | Whether to overwrite the output directory if it already exists (True/False) |
| `final_hal`          | Path to the final .hal file with all genomes appended                       |
| `tmp_dir`            | A temporary directory for Snakemake and Cactus to use. Should have lots of space.|
| `use_gpu`            | Whether to use the GPU version of Cactus for the alignment (True/False)     |

#### Specifying resources for each rule

Below these options in the config file are further options for specifying resource usage for each rule that the pipeline will run. For example:

```
mask_partition: "gpu_test"
mask_gpu: 3
mask_cpu: 8
mask_mem: 25000
mask_time: 30
```

!!! warning "Allocate the proper partitions based on `use_gpu`"

    If you want to use the GPU version of cactus (*i.e.* you have set `use_gpu: True` in the config file), the partition for the rules **mask**, **blast**, and **align** must be GPU enabled. If not, the pipeline will fail to run.

!!! info "The gpu options will be ignored if `use_gpu: False` is set."

!!! info "**mem is in MB** and **time is in minutes**"

You will have to determine the proper resource usage for your dataset. Generally, the larger the data set (either more genomes or bigger genomes), the more time and memory you will need, and the more you will benefit from providing more CPUs and GPUs.

??? example "Resource usage on a dataset of 22 turtle genomes"

    We have run an earlier version of the pipeline on 22 turtle genomes. The average genome size is 2200 Mb (2.2 Gb). We allocated the following resources for the Cactus rules:

    | Step    | Partition | Memory | CPUs | GPUs | Time |
    |---------|-----------|--------|------|------|------|
    | Mask    | gpu       | 100g   | 64   | 4    | 2h   |
    | Blast   | gpu       | 400g   | 64   | 4    | 48h  |
    | Align   | bigmem    | 450g   | 64   | NA   | 48h  |

    **Note: At this time, the Align step was not GPU enabled. That has changed in the current version.**

    This resulted in the following real run times:

    <center>
        <img src="../../img/cactus-runtime-turtles.png" alt="A figure with multiple boxplots titled 'Cactus run time on 22 turtle genomes'">
    </center>

    In general, increasing or decreasing CPUs GPUs available will decrease runtime.

    And max memory usages:

    <center>
        <img src="../../img/cactus-maxmem-turtles.png" alt="A figure with multiple boxplots titled 'Cactus max memory usage on 22 turtle genomes'">
    </center>

    Increasing available memory may also decrease runtime.
    

## Questions/troubleshooting

How can I tell if my Newick tree is rooted?

However, if you want to use a specific version, search [the available versions in the repository](https://quay.io/repository/comparative-genomics-toolkit/cactus?tab=tags) and run the following command, substitution `<desired version>` for the string of the version you want, *e.g.* "v2.9.3":

```bash
singularity pull --disable-cache docker://quay.io/comparative-genomics-toolkit/cactus:<desired version>
```

