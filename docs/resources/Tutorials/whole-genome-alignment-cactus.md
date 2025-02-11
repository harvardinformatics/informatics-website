---
title: Whole genome alignment with Cactus
---

Comparative genomics requires alignments between sequences from different populations or species. While alignment of small chunks of sequence (e.g. genes) between many species is relatively straightforward, whole genome alignment has been challenging. The [Cactus genome alignment software](https://github.com/ComparativeGenomicsToolkit/cactus) and its [associated tools](https://github.com/ComparativeGenomicsToolkit) has made this task feasible for up to hundreds of genomes. However, running the whole pipeline can still be difficult. Here we have developed a [Snakemake](https://snakemake.readthedocs.io/en/stable/) pipeline to facilitate running Cactus on a computing cluster. This is done by first running the `cactus-prepare` command to generate the Cactus labeled phylogeny, which is used to guide the submission of jobs to the cluster.

## Pre-requisuites

1. A computing cluster (default: SLURM)

Computing clusters manage the resources available to large numbers of people through a job submission and scheduling system. [SLURM](https://slurm.schedmd.com/overview.html) is one such job scheduling program and is the one used by [Harvard's cluster](https://docs.rc.fas.harvard.edu/kb/running-jobs/). Because of this, this pipeline was developed around a SLURM profile, though it should be possible to extend it to [any job scheduler that Snakemake supports](https://github.com/snakemake?q=executor&type=all&language=&sort=).

2. Snakemake

[Snakemake](https://snakemake.readthedocs.io/en/stable/) is a workflow management tool. Since Cactus is comprised of several steps, we use Snakemake to make sure those steps are run automatically and efficiently. You can install Snakemake using conda. See: [Installing command line software](installing-command-line-softwaremd).

3. Cactus (singularity image)

