---
title: Pangenome inference with Cactus-minigraph
---

<style>
/* FAQ styles */
    details > h5 {
        display: none;
    }
</style>

For aligning genome assemblies from the same species for population genomic analyses, the [Cactus genome alignment software](https://github.com/ComparativeGenomicsToolkit/cactus) has [implemented a workflow](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/pangenome.md) using [minigraph](https://github.com/lh3/minigraph). However, this can still be technically difficult to run. Here we have developed a [Snakemake](https://snakemake.readthedocs.io/en/stable/) pipeline to facilitate running Cactus-minigraph on a computing cluster. For more details on how Snakemake breaks up Cactus-minigraph's steps, expand the box below.

??? example "The cactus-minigraph snakemake pipeline's rulegraph"

    Here is the rulegraph for the pipeline. It is presented in two parts because the **split** rule breaks up the workflow by chromosome/scaffold for efficient submission of **align** steps. Even though it is presented here as two rulegraphs, the pipeline does all steps in one command, with **align** picking up where **split** left off.

    <center>
        <img src="../../img/minigraph-rulegraph-1.png" alt="A directed acyclic graph showing the rules up to split for the pipeline.'">
        <img src="../../img/minigraph-rulegraph-2.png" alt="A directed acyclic graph showing the rules starting from align for the pipeline.'">
    </center>

!!! tip "This pipeline is suitable for aligning and constructing pangenomes from samples of the same species"

    For whole genome alignment between different species, see our [Cactus whole genome alignment tutorial](whole-genome-alignment-cactus.md)

## Getting started

You will need several things to be able to run this pipeline:

1. A computing cluster that uses [SLURM](https://slurm.schedmd.com/overview.html), though it should be possible to extend it to [any job scheduler that Snakemake supports](https://github.com/snakemake?q=executor&type=all&language=&sort=).
2. conda or mamba to install software. See [Installing command line software](installing-command-line-software-conda-mamba.md) if you don't have conda/mamba installed.
2. [Snakemake](https://snakemake.readthedocs.io/en/stable/) and the [Snakemake SLURM plugin](https://anaconda.org/bioconda/snakemake-executor-plugin-slurm)
3. Singularity - **The pipeline itself will automatically download the latest version of the Cactus singularity container for you.**
4. The [Harvard Informatics cactus-snakemake pipeline](https://github.com/harvardinformatics/cactus-snakemake/)

Below we walk you through our recommended way for getting this all set up.

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

1. The assembled genome [FASTA](https://en.wikipedia.org/wiki/FASTA_format) files for each sample.
2. A reference sample.

You will use these to create the input file for Cactus-minigraph.

### Preparing the Cactus-minigraph input file

The various Cactus-minigraph commands depend on a single input file with information about the genomes to align. This file is a simple tab delimited file with two columns. 

Each line contains in the first column one sample label and in the second column the path to the genome FASTA file for that sample. 

!!! note "Unlike regular Cactus, Cactus-minigraph does not require the input sequences to be softmasked"

    However, the FASTA files should still **not** be **hard** masked, meaning masked bases are replaced with Ns.

For example, if one were running this pipeline on 5 samples named A, B, C, D, and E, the input file may look something like this:

```
A   seqdir/a.fa
B   seqdir/b.fa
C   seqdir/c.fa
D   seqdir/d.fa
E   seqdir/e.fa
```

There is much more information about the Cactus-minigraph input file in the [official documentation for cactus-minigraph](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/pangenome.md#interface), including how to run the pipeline with diploid assemblies. There is also an example input file for a small test dataset [here](https://github.com/harvardinformatics/cactus-snakemake/blob/main/tests/yeast-minigraph/yeastPangenome-local.txt) or at `tests/yeast-minigraph/yeastPangenome-local.txt`. For more info, see section: [Test dataset](#test-dataset).

### Reference sample

Cactus-minigraph requires that you select one sample as a reference sample [for a variety of reasons](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/pangenome.md#reference-sample). Keep these in mind as you prepare your inputs. The reference sample will be indicated in the Snakemake config file (outlined below). For instance, if I wanted my reference sample in the above file to be **C**, I would put the string `C` in the `reference:` line of the Snakemake config file.

### Preparing the Snakemake config file

!!! tip "Be sure to start with the example config file as a template!"

    The config for the Cactus-minigraph test data can be found at [here](https://github.com/harvardinformatics/cactus-snakemake/blob/main/tests/yeast-minigraph/yeast-minigraph-cfg.yaml) or at `tests/yeast-minigraph/yeast-minigraph-cfg.yaml` in your downloaded cactus-snakemake repo. Be sure to use this as the template for your project since it has all the options needed! **Note: the partitions set in this config file are specific to the Harvard cluster. Be sure to update them if you are running this pipeline elsewhere.**

    Additionally, a blank template file is located [here](https://github.com/harvardinformatics/cactus-snakemake/blob/main/minigraph-config-template.yaml) or at `minigraph-config-template.yaml` in your downloaded cactus-snakemake repo.

Besides the sequence input, the pipeline needs some extra configuration to know where to look for files and write output. That is done in the Snakemake configuration file for a given run. It contains 2 sections, one for specifying the input and output options, and one for specifying resources for the various rules (see [below](#specifying-resources-for-each-rule)). The first part should look something like this:

```
cactus_path: <path/to/cactus-singularity-image OR download>

input_file: <path/to/cactus-input-file>

output_dir: <path/to/desired/output-directory>

overwrite_output_dir: <True/False>

reference: <Sample ID from input_file>

prefix: <string>

tmp_dir: <path/to/tmp-dir/>

use_gpu: <True/False>
```

Simply replace the string surrounded by <> with the path or option desired. Below is a table summarizing these options:

| Option                 | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `cactus_path`          | Path to the Cactus Singularity image. If blank or 'download', the image of the latest Cactus version will be downloaded and used. |
| `input_file`           | Path to the input file containing the species tree and genome paths (described above). |
| `output_dir`           | Directory where the all output will be written. |
| `overwrite_output_dir` | Whether to overwrite the output directory if it already exists (True/False). |
| `reference`            | The sample ID from the input file to serve as the reference for pangenome creation. |
| `prefix`               | A string that will be appended to all files created by the pipeline. |
| `tmp_dir`              | A temporary directory for Snakemake and Cactus to use. Should have lots of space. |
| `use_gpu`              | Whether to use the GPU version of Cactus for the alignment (True/False). |

#### Specifying resources for each rule

Below these options in the config file are further options for specifying resource usage for each rule that the pipeline will run. For example:

```
minigraph_partition: "shared"
minigraph_cpu: 8
minigraph_mem: 25000
minigraph_time: 30
```

!!! warning "Notes on resource allocation"

    * Be sure to use partition names appropriate your cluster. Several examples in this tutorial have partition names that are specific to the Harvard cluster, so be sure to change them.
    * **Allocate the proper partitions based on `use_gpu`.** If you want to use the GPU version of cactus (*i.e.* you have set `use_gpu: True` in the config file), the partition for the rule **align** must be GPU enabled. If not, the pipeline will fail to run.
    * The `gpu:` option for rule **align** will be ignored if `use_gpu: False` is set.
    * **mem is in MB** and **time is in minutes**.

You will have to determine the proper resource usage for your dataset. Generally, the larger the genomes, the more time and memory each job will need, and the more you will benefit from providing more CPUs and GPUs.

## Running the pipeline

With [everything installed](#getting-started), the [Cactus input file](#preparing-the-cactus-input-file), and the [Snakemake configuration file](#preparing-the-snakemake-config-file) setup, you are now ready to run the pipeline.

### Do a `--dryrun` first

First, we want to make sure everything is setup properly by using the `--dryrun` option. This tells Snakemake to display what jobs it is going to run without actually submitting them. This is important to do before actually submitting the jobs so we can catch any setup errors beforehand.

This is done with the following command, changing the snakefile `-s` and `--configfile` paths to the one you have created for your project:

```bash
snakemake -p -j <# of jobs to submit simultaneously> -e slurm -s </path/to/cactus_minigraph.smk> --configfile <path/to/your/snakmake-config.yml> --dryrun
```

??? info "Command breakdown"

    | Command-line option                               | Description |
    | ------------------------------------------------- | ----------- |
    | `snakemake`                                       | The call to the snakemake workflow program to execute the workflow. |
    | `-p`                                              | Print out the commands that will be executed. |
    | `-j <# of jobs to submit simultaneously>`         | The maximum number of jobs that will be submitted to your SLURM cluster at one time. |
    | `-e slurm`                                        | Specify to use the SLURM executor plugin. See: [Getting started](#getting-started). |
    | `-s </path/to/cactus_minigraph.smk>               | The path to the workflow file. |
    | `--configfile <path/to/your/snakmake-config.yml>` | The path to your config file. See: [Preparing the Snakemake config file](#preparing-the-snakemake-config-file). |
    | `--dryrun`                                        | Do not execute anything, just display what would be done. |

!!! info "This command won't actually submit the pipeline jobs!"

    However even during a `--dryrun` some pre-processing steps will be run, including creation of the output directory if it doesn't exist and downloading the Cactus Singularity image if `cactus_path: download` is set in the config file. These should be relatively fast and not resource intensive tasks.

If this completes successfully, you should see a bunch of blue, yellow, and green text on the screen, ending with something like this (the number of jobs and Reasons: may differ for your project):

```bash
Job stats:
job           count
----------  -------
all               1
copy_input        1
graphmap          1
join              1
minigraph         1
split             1
total             6

Reasons:
    (check individual jobs above for details)
    input files updated by another job:
        all, graphmap, join, minigraph, split
    output files have to be generated:
        copy_input, graphmap, join, minigraph, split

This was a dry-run (flag -n). The order of jobs does not reflect the order of execution.
The run involves checkpoint jobs, which will result in alteration of the DAG of jobs (e.g. adding more jobs) after their completion.
```

If you see any red text, that likely means an error has occurred that must be addressed before you run the pipeline. 

!!! warning "The number of jobs will be higher than indicated by the dryrun!"
    
    Note that rule **align** does not appear in the list of jobs to run. This is because it can't be evaluated until rule **split** is run (in snakemake terms, this is a checkpoint). But it will be run! The total number of jobs will be the number reported during the dryrun + the number of chromosomes in your reference sample (1 align job per chromosome).

### Submitting the jobs

If you're satisfied that the `--dryrun` has completed successfully and you are ready to start submitting Cactus jobs to the cluster, you can do so by simply removing the `--dryrun` option from the command above:

```bash
snakemake -p -j <# of jobs to submit simultaneously> -e slurm -s </path/to/cactus_minigraph.smk> --configfile <path/to/your/snakmake-config.yml>
```

This will start submitting jobs to SLURM. On your screen, you will see continuous updates regarding job status in blue text. In another terminal, you can also check on the status of your jobs by running `squeue -u <your user id>`. 

!!! tip "Be sure you have a way to keep the main Snakemake process running."

    Remember, that some of these steps can take a long time, or your jobs may be stuck in the queue for a while. That means the Snakemake job must have a persistent connection in order to keep running an submitting jobs. There are a few ways this can be accomplished, some better than ~~others~~:

    1. ~~Keep your computer on and connected to the cluster. This may be infeasible and you may still suffer from connection issues.~~

    2. ~~Run the Snakemake job in the background by using `nohup <snakemake command> &`. This will run the command in the background and persist even if you disconnect. However, it makes it difficult to check on the status of your command.~~

    3. Submit the Snakemake command itself as a SLURM job. This will require [preparing and submitting a job script](https://docs.rc.fas.harvard.edu/kb/running-jobs/). This is a good solution.

    4. Use a [terminal multiplexer](https://en.wikipedia.org/wiki/Terminal_multiplexer) like [GNU Screen](https://en.wikipedia.org/wiki/GNU_Screen) or [tmux](https://en.wikipedia.org/wiki/Tmux). These programs allow you to open a sub-terminal within your currently connected terminal that remains even after you disconnect from the server. This is also a good solution.

Depending on the number of genomes, their sizes, and your wait in the queue, you will hopefully have your whole genome alignment within a few days!

### Test dataset

Cactus provides a test dataset which we have setup to run in the `tests/yeast-minigraph/` folder. 

Here is a breakdown of the files so you can investigate them and prepare similar ones for your project:

| File/directory             | Description |
| -------------------------- | ----------- |
| `seq/`                     | This directory contains the input sequence files for the test dataset in FASTA format. |
| `yeast-minigraph-cfg.yaml` | This is the config file for Snakemake and has all of the options you would need to setup for your own project. |
| `yeastPangenome-local.txt` | This is the input file as required by Cactus-minigraph. It has lines containing the location of the sequence files for each sample. |

We recommend running this test dataset before setting up your own project.

First, open the config file, `tests/yeast-minigraph/yeast-minigraph-cfg.yaml` and make sure the partitions are set appropriately for your cluster. For this small test dataset, it is appropriate to use any "test" partitions you may have. Then, update the path to `tmp_dir` to point to a location where you have a lot of temporary space. Even this small dataset will fail if this directory does not have enough space.

After that, run a dryrun of the test dataset by changing into the `tests/` directory and running:

```bash
cd tests/yeast-minigraph/
snakemake -p -j 10 -e slurm -s ../cactus_minigraph.smk --configfile yeast-minigraph-cfg.yaml --dryurun
```

If this completes without error, run the pipeline by removing the `--dryrun` option:

```bash
snakemake -p -j 10 -e slurm -s ../cactus_minigraph.smk --configfile yeast-minigraph-cfg.yaml
```

## Questions/troubleshooting

??? question "1. I want to use a specific version of the Cactus singularity image. How can I do so?"

    ##### 1. Using a specific Cactus version

    If you want to use a specific Cactus version, search [the available versions in the repository](https://quay.io/repository/comparative-genomics-toolkit/cactus?tab=tags) and run the following command, substituting `<desired version>` for the string of the version you want, *e.g.* "v2.9.3":

    ```bash
    singularity pull --disable-cache docker://quay.io/comparative-genomics-toolkit/cactus:<desired version>
    ```

    Then, in the [Snakemake config file](#preparing-the-snakemake-config-file), set `cactus_path:` to be the path to the `.sif` file that was downloaded.

??? question "2. My jobs were running but my Snakemake process crashed because of connection issues/server maintenance! What do I do?"

    ##### 2. Snakemake crashes

    As long as there wasn't an error with one of the jobs, Snakemake is designed to be able to resume and resubmit jobs pretty seamlessly. You just need to run the same command you ran to begin with and it should pickup submitting jobs where it left off. You could also run a `--dryrun` first and it should tell you which jobs are left to be done.

??? question "3. The Cactus-minigraph docs say to not use hardmasked gneomes. How can I tell if my genome FASTA files are hardmasked?"

    ##### 3. How can I tell if my genome FASTA files are hardmasked?

    Hardmasking means you replace low quality or low confidence bases in your assembly with N characters. Unfortunately, there are many reasons for Ns to appear in a genome fasta file, so it is difficult to tell if it is because it is hardmasked based on the presence of Ns alone. Hopefully the source of the file has left some documentation describing how it was prepared...

??? question "4. I want to run this on a cluster with a job scheduler other than SLURM! What do I do?"

    ##### 4. Clusters other than SLURM?

    Generally, it should be relatively easy to update the cluster profile (`profiles/slurm_profile/config.yaml`) and use the appropriate [Snakemake cluster executor](https://github.com/snakemake?q=executor&type=all&language=&sort=).

    If you need help or run into problems, please [create an issue on the pipeline's github](https://github.com/harvardinformatics/cactus-snakemake/issues) and we'll try and help - though it will likely be up to you to test on your own cluster, since we only have easy access to a cluster running SLURM.

??? question "5. I tried to run the pipeline and I ran into an error that I don't understand or can't resolve. What do I do?"

    ##### 5. Encountering errors

    Please [search for or create an issue on the pipeline's github](https://github.com/harvardinformatics/cactus-snakemake/issues) that includes information about your input files, the command you ran, and the error that you are getting. The text of any log files would also be appreciated.

    Additionally, if you are at Harvard, there are [several ways to contact us](../../contact.md) to help you through your errors.

??? question "6. I have an idea to improve or add to the pipeline. What do I do?"

    ##### 6. Pipeline improvements
    
    Great! Please [create an issue on the pipeline's github](https://github.com/harvardinformatics/cactus-snakemake/issues) describing your idea so we can discuss its implementation!
