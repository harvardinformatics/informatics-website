---
title: Whole genome alignment with Cactus
authors: 
    - Gregg Thomas
---

{{ author_row(page) }}

Comparative genomics requires alignments between sequences from different populations or species. While alignment of small chunks of sequence (e.g. genes) between many species is relatively straightforward, whole genome alignment has been challenging. The [Cactus genome alignment software :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus){:target="_blank"} and its [associated tools :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit){:target="_blank"} has made this task feasible for up to hundreds of genomes. However, this can still be technically difficult to run. Here we have developed a [Snakemake :octicons-link-external-24:](https://snakemake.readthedocs.io/en/stable/){:target="_blank"} pipeline to facilitate running Cactus on a computing cluster. This is done by first running the `cactus-prepare` command to generate the Cactus labeled phylogeny, which is used to guide the submission of jobs to the cluster. For more details on how Snakemake breaks up Cactus's steps, expand the box below.

??? example "The cactus-snakemake pipeline's rulegraph"

    Here is the rulegraph for the pipeline. It works in rounds based on the shape of the input phylogeny (hence the cycle). First, genomes at the tips are masked and then all internal nodes are aligned.

    <center>
        <img src="../../img/cactus-rulegraph.png" alt="A directed cyclic graph showing the rules for the pipeline.'">
    </center>

!!! tip "This pipeline is suitable for aligning genomes from different species"

    For pangenome inference and whole genome alignment between samples of the same species, see our [Cactus-minigraph tutorial](pangenome-cactus-minigraph.md)

## Getting started

You will need several things to be able to run this pipeline:

1. A computing cluster that uses [SLURM :octicons-link-external-24:](https://slurm.schedmd.com/overview.html){:target="_blank"}, though it should be possible to extend it to [any job scheduler that Snakemake supports :octicons-link-external-24:](https://github.com/snakemake?q=executor&type=all&language=&sort=){:target="_blank"}.
2. conda or mamba to install software. See [Installing command line software](installing-command-line-software-conda-mamba.md) if you don't have conda/mamba installed.
2. [Snakemake :octicons-link-external-24:](https://snakemake.readthedocs.io/en/stable/){:target="_blank"} and the [Snakemake SLURM plugin :octicons-link-external-24:](https://anaconda.org/bioconda/snakemake-executor-plugin-slurm){:target="_blank"}
3. Singularity - **The pipeline itself will automatically download the latest version of the Cactus singularity container for you.**
4. The [Harvard Informatics cactus-snakemake pipeline :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/){:target="_blank"}

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

!!! tip "Cannon cluster Snakemake plugin"

    If you are on the Harvard Cannon cluster, instead of the generic snakemake-executor-plugin-slurm, you can use our specific plugin for the Cannon cluster: [snakemake-executor-plugin-cannon :octicons-link-external-24:](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/cannon.html){:target="_blank"}. This facilitates *automatic partition selection* based on requested resources. Install this in your environment with:

    ```bash
    mamba install bioconda::snakemake-executor-plugin-cannon
    ```

    Then, when running the workflow, specify the cannon executor with `-e cannon` instead of `-e slurm`.

    If you are not on the Harvard Cannon cluster, stick with the generic SLURM plugin. You will just need to directly specify the partitions for each rule in the config file ([see below](#specifying-resources-for-each-rule)).

### Downloading the cactus-snakemake pipeline

The [pipeline :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/){:target="_blank"} is currently available on github. You can install it on the Harvard cluster or any computer that has `git` installed by navigating to the directory in which you want to download it and doing one of the following:

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

!!! warning "Important! cactus-snakemake v3.0.0 and later requires Cactus v2.9.9 or later."

    Due to bug fixes in Cactus, v3.0.0+ of cactus-snakemake is only compatibile with Cactus v2.9.9 or later. Don't worry, cactus-snakemake will always use the latest version of Cactus available unless you specify otherwise in your config file. However, if you do wish to use an older version of Cactus, you can use [cactus-snakemake v2.1.0  :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/releases/tag/v2.1.0){:target="_blank"}.

## Inputs you need to prepare

To run this pipeline, you will need (corresponding Snakemake config option given in parentheses):

1. A [**rooted**](#2-how-can-i-tell-if-my-input-newick-tree-is-rooted) phylogenetic tree of all species to align, with or without branch lengths, in [Newick format :octicons-link-external-24:](https://en.wikipedia.org/wiki/Newick_format){:target="_blank"} (specified in `input_file`).
2. The [**softmasked**](#3-how-can-i-tell-if-my-genome-fasta-files-are-softmasked) genome [FASTA :octicons-link-external-24:](https://en.wikipedia.org/wiki/FASTA_format){:target="_blank"} files for each species (specified in `input_file`).
3. A reference genome to project the alignment to MAF format (`maf_reference`).

You will use these to create the input file for Cactus.

### Preparing the Cactus input file

The various Cactus commands depend on a single input file with information about the genomes to align. This file is a simple tab delimited file. 

The first line of the file contains the **rooted** input species tree in [Newick format :octicons-link-external-24:](https://en.wikipedia.org/wiki/Newick_format){:target="_blank"} and nothing else (be sure to remember the semi-colon at the end of the Newick tree!).

Each subsequent line contains in the first column one tip label from the tree and in the second column the path to the genome FASTA file for that species. 

!!! warning "[The FASTA files must softmasked!](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/progressive.md#interface)"

    The genomes you provide in FASTA format must be softmasked before running Cactus, otherwise the the program will likely not complete. You can tell if a genome FASTA file is masked by the presence of lower-case nucleotides: a, t, c, or g. If your FASTA file has these lower-case characters, it has likely been softmasked. If not, you will have to mask the genome with a tool like [RepeatMasker :octicons-link-external-24:](https://www.repeatmasker.org/){:target="_blank"}. Also importantly, the FASTA files should **not** be **hard** masked, meaning the masked bases are replaced with Ns.

For example, if one were running this pipeline on 5 species named A, B, C, D, and E, the input file may look something like this:

```
(((A,B),(C,D)),E);
A   seqdir/a.fa
B   seqdir/b.fa
C   seqdir/c.fa
D   seqdir/d.fa
E   seqdir/e.fa
```

For more information about the Cactus input file, see their [official documentation :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/progressive.md#interface){:target="_blank"}. There is also an example input file for a small test dataset [here :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/blob/main/tests/evolverMammals/evolverMammals.txt){:target="_blank"} or at `tests/evolverMammals/evolverMammals.txt`. For more info, see section: [Test dataset](#test-dataset).

### Reference sample

In order to run the last step of the workflow that converts the HAL format to a readable MAF format (See [pipeline outputs](#pipeline-outputs) for more info), you will need to select one assembly as a reference assembly. The reference assembly's coordinate system will be used for projection to MAF format. You should indicate the reference assembly in the Snakemake config file (outlined below). For instance, if I wanted my reference sample in the above file to be **C**, I would put the string `C` in the `maf_reference:` line of the Snakemake config file.

### Preparing the Snakemake config file

!!! tip "Be sure to start with the example config file as a template!"

    The config for the Cactus test data can be found at [here :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/blob/main/tests/evolverMammals/evolverMammals-cfg.yaml){:target="_blank"} or at `tests/evolverMammals/evolverMammals-cfg.yaml` in your downloaded cactus-snakemake repo. Be sure to use this as the template for your project since it has all the options needed! **Note: the partitions set in this config file are specific to the Harvard cluster. Be sure to update them if you are running this pipeline elsewhere.**

    Additionally, a blank template file is located [here :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/blob/main/config-templates/config-template.yaml){:target="_blank"} or at `config-templates/config-template.yaml` in your downloaded cactus-snakemake repo.

Besides the sequence input, the pipeline needs some extra configuration to know where to look for files and write output. That is done in the Snakemake configuration file for a given run. It contains 2 sections, one for specifying the input and output options, and one for specifying resources for the various rules (see [below](#specifying-resources-for-each-rule)). The first part should look something like this:

```
cactus_path: <path/to/cactus-singularity-image OR download OR version string>

cactus_gpu_path: <path/to/cactus-GPU-singularity-image OR download OR version string>

input_file: <path/to/cactus-input-file>

output_dir: <path/to/desired/output-directory>

final_prefix: <desired name of final .hal and .maf files with all genomes appended>

maf_reference: <Genome ID from input_file>

tmp_dir: <path/to/tmp-dir/>

use_gpu: <True/False>
```

Simply replace the string surrounded by <> with the path or option desired. Below is a table summarizing these options:

| Option                 | Description                                                                 |
|----------------------- | ----------------------------------------------------------------------------|
| `cactus_path`          | Path to the Cactus Singularity image. If blank or 'download', the image of the latest Cactus version will be downloaded and used. If a version string is provided (e.g. 2.9.5), then that version will be downloaded and used. This will be used whether `use_gpu` is True or False. |
| `cactus_gpu_path`      | Path to the Cactus GPU Singularity image. If blank or 'download', the image of the latest Cactus version will be downloaded and used. If a version string is provided (e.g. 2.9.5), then that version will be downloaded and used. This will only be used if `use_gpu` is True. |
| `input_file`           | Path to the input file containing the species tree and genome paths (described above). |
| `output_dir`           | Directory where the all output will be written. |
| `final_prefix`         | The name of the final .hal and .maf files with all aligned genomes appended. The final files will be `<final_prefix>.hal` and `<final_prefix>.maf`. These files will be placed within `output_dir`. |
| `maf_reference`        | The label for the genome to use when converting from HAL to MAF. This means that the MAF alignment will be projected on to that genome's coordinate system. |
| `tmp_dir`              | A temporary directory for Snakemake and Cactus to use. Should have lots of space. |
| `use_gpu`              | Whether to use the GPU version of Cactus for the alignment (True/False). |

#### Specifying resources for each rule

Below these options in the config file are further options for specifying resource usage for each rule that the pipeline will run. For example:

```
rule_resources:
  preprocess:
    partition: shared
    mem_mb: 25000
    cpus: 8
    time: 30

  blast:
    partition: shared  # If use_gpu is True, this must be a partition with GPUs
    mem_mb: 50000
    cpus: 48
    gpus: 2            # If use_gpu is False, this will be ignored
    time: 120
```

**The rule _blast_ is the only one that uses GPUs if `use_gpu` is True.**

!!! warning "Notes on resource allocation"

    * Be sure to use partition names appropriate your cluster. Several examples in this tutorial have partition names that are specific to the Harvard cluster, so be sure to change them.
    * **Allocate the proper partitions based on `use_gpu`.** If you want to use the GPU version of cactus (*i.e.* you have set `use_gpu: True` in the config file), the partition for the rule **blast** must be GPU enabled. If not, the pipeline will fail to run.
    * The `blast: gpus:` option will be ignored if `use_gpu: False` is set.
    * **mem_mb is in MB** and **time is in minutes**.
    * **If using the [snakemake-executor-plugin-cannon :octicons-link-external-24:](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/cannon.html){:target="_blank"} specifically for the Harvard Cannon cluster, you can leave the `partition:` fields blank and one will be selected automatically based on the other resources requested!**

You will have to determine the proper resource usage for your dataset. Generally, the larger the genomes, the more time and memory each job will need, and the more you will benefit from providing more CPUs and GPUs.

Click below to take a look at an example to get a sense for how many resources you will need to allot, adjusting for the genome size of your organisms. :material-arrow-down-right:

??? example "Example: Resource usage on a dataset of 22 turtle genomes"

    ##### Example: Resource usage on a dataset of 22 turtle genomes

    We have run the pipeline on 22 turtle genomes. The average genome size is 2210 Mb (2.2 Gb):
    
    <center>
        <img src="../../img/turtles-genome-sizes.png" alt="A boxplot showing a distribution of genome sizes for 22 turtles">
    </center>    
    
    We allocated the following resources for the Cactus rules:

    <center>

    | Step       | Partition | Memory | CPUs | GPUs | Time |
    |------------|-----------|--------|------|------|------|
    | Preprocess | gpu       | 100g   | 8    | 2    | 1h   |
    | Blast      | gpu       | 400g   | 64   | 1    | 12h  |
    | Align      | gpu       | 450g   | 64   | 2    | 12h  |

    </center>

    This resulted in the following real run times:

    <center>
        <img src="../../img/turtles-cactus-runtime.png" alt="A figure with multiple boxplots showing  the distribution of run time on 22 turtle genomes">
    </center>

    In general, increasing or decreasing CPUs or GPUs available will decrease runtime.

    And max memory usages:

    <center>
        <img src="../../img/turtles-cactus-maxmem.png" alt="A figure with multiple boxplots showing the distribution of max memory usage on 22 turtle genomes">
    </center>

    Increasing available memory may also decrease runtime.

## Running the pipeline

With [everything installed](#getting-started), the [Cactus input file](#preparing-the-cactus-input-file), and the [Snakemake configuration file](#preparing-the-snakemake-config-file) setup, you are now ready to run the pipeline.

### Do a `--dryrun` first

First, we want to make sure everything is setup properly by using the `--dryrun` option. This tells Snakemake to display what jobs it is going to run without actually submitting them. This is important to do before actually submitting the jobs so we can catch any setup errors beforehand.

This is done with the following command, changing the snakefile `-s` and `--configfile` paths to the one you have created for your project:

```bash
snakemake -j <# of jobs to submit simultaneously> -e slurm -s </path/to/cactus.smk> --configfile <path/to/your/snakmake-config.yml> --dryrun
```

??? info "Command breakdown"

    | Command-line option                               | Description |
    | ------------------------------------------------- | ----------- |
    | `snakemake`                                       | The call to the snakemake workflow program to execute the workflow. |
    | `-j <# of jobs to submit simultaneously>`         | The maximum number of jobs that will be submitted to your SLURM cluster at one time. |
    | `-e slurm`                                        | Specify to use the SLURM executor plugin, or use `-e cannon` if using the Cannon specific plugin.  See: [Getting started](#getting-started) |
    | `-s </path/to/cactus.smk>`                        | The path to the workflow file. |
    | `--configfile <path/to/your/snakmake-config.yml>` | The path to your config file. See: [Preparing the Snakemake config file](#preparing-the-snakemake-config-file). |
    | `--dryrun`                                        | Do not execute anything, just display what would be done. |

!!! info "This command won't actually submit the pipeline jobs!"

    However even during a `--dryrun` some pre-processing steps will be run, including creation of the output directory if it doesn't exist, downloading the Cactus Singularity image if `cactus_path: download` is set in the config file, and running `cactus-prepare`. These should all be relatively fast and not resource intensive tasks.

If this completes successfully, you should see a bunch of blue, yellow, and green text on the screen, ending with something like this (the number of jobs and Reasons: may differ for your project):

```bash
Job stats:
job         count
--------  -------
align           4
all             1
append          1
blast           4
convert         4
copy_hal        1
preprocess      5
total          20

Reasons:
    (check individual jobs above for details)
    input files updated by another job:
        align, all, append, blast, convert, copy_hal
    output files have to be generated:
        align, append, blast, convert, copy_hal, preprocess

This was a dry-run (flag -n). The order of jobs does not reflect the order of execution.
```

If you see any red text, that likely means an error has occurred that must be addressed before you run the pipeline.

### Submitting the jobs

If you're satisfied that the `--dryrun` has completed successfully and you are ready to start submitting Cactus jobs to the cluster, you can do so by simply removing the `--dryrun` option from the command above:

```bash
snakemake -j <# of jobs to submit simultaneously> -e slurm -s </path/to/cactus.smk> --configfile <path/to/your/snakmake-config.yml>
```

This will start submitting jobs to SLURM. On your screen, you will see continuous updates regarding job status in blue text. In another terminal, you can also check on the status of your jobs by running `squeue -u <your user id>`. 

!!! tip "Be sure you have a way to keep the main Snakemake process running."

    Remember, that some of these steps can take a long time, or your jobs may be stuck in the queue for a while. That means the Snakemake job must have a persistent connection in order to keep running an submitting jobs. There are a few ways this can be accomplished, some better than ~~others~~:

    1. ~~Keep your computer on and connected to the cluster. This may be infeasible and you may still suffer from connection issues.~~

    2. ~~Run the Snakemake job in the background by using `nohup <snakemake command> &`. This will run the command in the background and persist even if you disconnect. However, it makes it difficult to check on the status of your command.~~

    3. Submit the Snakemake command itself as a SLURM job. This will require [preparing and submitting a job script :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/running-jobs/){:target="_blank"}. This is a good solution.

    4. Use a [terminal multiplexer :octicons-link-external-24:](https://en.wikipedia.org/wiki/Terminal_multiplexer){:target="_blank"} like [GNU Screen :octicons-link-external-24:](https://en.wikipedia.org/wiki/GNU_Screen){:target="_blank"} or [tmux :octicons-link-external-24:](https://en.wikipedia.org/wiki/Tmux){:target="_blank"}. These programs allow you to open a sub-terminal within your currently connected terminal that remains even after you disconnect from the server. This is also a good solution.

Depending on the number of genomes, their sizes, and your wait in the queue, you will hopefully have your whole genome alignment within a few days!

### Test dataset

Cactus provides a test dataset which we have setup to run in the `tests/evolverMammals/` folder. 

Here is a breakdown of the files so you can investigate them and prepare similar ones for your project:

| File/directory            | Description |
| ------------------------- | ----------- |
| `evolverMammals-seq/`     | This directory contains the input sequence files for the test dataset in FASTA format. |
| `evolverMammals-cfg.yaml` | This is the config file for Snakemake and has all of the options you would need to setup for your own project. |
| `evolverMammals.txt`      | This is the input file as required by Cactus. It has the rooted Newick tree on the first line, followed by lines containing the location of the sequence files for each tip in the tree. |

We recommend running this test dataset before setting up your own project.

First, open the config file, `tests/evolverMammals/evolverMammals-cfg.yaml` and make sure the partitions are set appropriately for your cluster. For this small test dataset, it is appropriate to use any "test" partitions you may have. Then, update the path to `tmp_dir` to point to a location where you have a lot of temporary space. Even this small dataset will fail if this directory does not have enough space.

After that, run a dryrun of the test dataset by changing into the `tests/` directory and running:

```bash
cd tests/evolverMammals/
snakemake -j 10 -e slurm -s ../../cactus.smk --configfile evolverMammals-cfg.yaml --dryurun
```

If this completes without error, run the pipeline by removing the `--dryrun` option:

```bash
snakemake -j 10 -e slurm -s ../../cactus.smk --configfile evolverMammals-cfg.yaml
```

## Pipeline outputs

The pipeline will output a [.paf :octicons-link-external-24:](https://github.com/lh3/miniasm/blob/master/PAF.md){:target="_blank"}, a [.hal :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/hal/blob/master/README.md){:target="_blank"}, and a [.fa :octicons-link-external-24:](https://en.wikipedia.org/wiki/FASTA_format){:target="_blank"} file for every node in the input tree (including ancestral sequences). The final alignment file will be `<final_prefix>.hal`, where `<final_prefix>` is whatever you specified in the Snakemake config file. 

The final alignment will also be presented in MAF format as `<final_prefix>.<maf_reference>.maf`, again where `<maf_reference>` is whatever you set in the Snakemake config. This file will include all sequences. Another MAF file, `<final_prefix>.<maf_reference>.nodupes.maf` will also be generated, which is the alignment in MAF format with no duplicate sequences. The de-duplicated MAF file is generated with `--dupeMode single`. See the [Cactus documentation regarding MAF export :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/progressive.md#maf-export){:target="_blank"} for more info.

A suite of tools called [HAL tools :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/Hal){:target="_blank"} is included with the Cactus singularity image if you need to manipulate or analyze .hal files. There are many tools for manipulating MAF files, though they are not always easy to use. The makers of Cactus also develop [taffy :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/taffy){:target="_blank"}, which can manipulate MAF files by converting them to TAF files.

## Questions/troubleshooting

??? question "1. My jobs were running but my Snakemake process crashed because of connection issues/server maintenance! What do I do?"

    ##### 1. Snakemake crashes

    As long as there wasn't an error with one of the jobs, Snakemake is designed to be able to resume and resubmit jobs pretty seamlessly. You just need to run the same command you ran to begin with and it should pickup submitting jobs where it left off. You could also run a `--dryrun` first and it should tell you which jobs are left to be done.

??? question "2. How can I tell if my input Newick tree is rooted? If it isn't rooted, how can I root it? Or if it is rooted, how can I re-root it?"

    ##### 2. How can I tell if my input Newick tree is rooted?

    The easiest way to check if your tree is rooted is probably to load the tree into [R :octicons-link-external-24:](https://www.r-project.org/){:target="_blank"} with the `ape` package. This can be done with the following commands:

    ```r
    install.packages("ape") # Only if you don't have it installed already
    library(ape)
    tree <- read.tree("your-tree.nwk")
    is.rooted(tree)
    ```

    If the result of this text is `TRUE` then your tree is rooted. If it is `FALSE` your tree is unrooted.

    If the tree is unrooted, or you want to re-root it, you can also do this in R with the `root()` function. Make sure `ape` is installed and loaded as above, and then:

    Root by a tip label:

    ```r
    rooted_tree <- root(tree, outgroup = "TipName", resolve.root = TRUE)
    ```

    Or root by an internal node number:

    ```r
    rooted_tree <- root(tree, outgroup = 5, resolve.root = TRUE)
    ```

    In the second case, using the internal node number, if you need to know how R has labeled the nodes, you can view the tree with the node labels by doing:

    ```r
    plot(tree) # Basic tree plot
    nodelabels() # Adds default node labels (node numbers)
    ```

    After the tree has been rooted/re-rooted, you can write it to a file:

    ```r
     write.tree(tree, file="your-rooted-tree.nwk")
    ```

??? question "3. How can I tell if my genome FASTA files are softmasked? How can I mask them if they aren't already?"

    ##### 3. How can I tell if my genome FASTA files are softmasked?

    Cactus requires the input genomes to be softmasked. This means that masked bases appear as lower case letters: a, t, c, g. Hopefully the source of your genome FASTA file has given you some information about how it was prepared, including how it was masked. If not, a very quick method to check for the occurrence of any lower case letter in the sequence is:

    ```bash
    if grep -q '^[^>]*[a-z]' your-genome-file.fa; then echo "The FASTA file is soft-masked."; else echo "The FASTA file is NOT soft-masked."; fi
    ```

    This is fast, but only detects the occurrence of a single lower case character. To count all the lower case characters at the cost of taking a couple of minutes, you can run:

    ```bash
    awk 'BEGIN{count=0} !/^>/{for(i=1;i<=length($0);i++) if (substr($0,i,1) ~ /[acgt]/) count++} END{print count}' your-genome-file.fa
    ```

    Importantly, your genomes [should not be **hard** masked :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/progressive.md#interface){:target="_blank"}, which means that masked bases are replaced by Ns. Unfortunately, there are many reasons for Ns to appear in a genome fasta file, so it is difficult to tell if it is because it is hardmasked based on the presence of Ns alone. Hopefully the source of the file has left some documentation describing how it was prepared...

    If your genomes are not softmasked and you wish to do so, you will have to run a program like [RepeatMasker :octicons-link-external-24:](https://www.repeatmasker.org/){:target="_blank"} or [RepeatModeler :octicons-link-external-24:](https://github.com/Dfam-consortium/RepeatModeler){:target="_blank"} on it. Please consult the documentation for these tools.

??? question "4. I want to run this on a cluster with a job scheduler other than SLURM! What do I do?"

    ##### 4. Clusters other than SLURM?

    Generally, it should be relatively easy install and use the appropriate [Snakemake cluster executor :octicons-link-external-24:](https://github.com/snakemake?q=executor&type=all&language=&sort=){:target="_blank"}.

    If you need help or run into problems, please [create an issue on the pipeline's github :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/issues){:target="_blank"} and we'll try and help - though it will likely be up to you to test on your own cluster, since we only have easy access to a cluster running SLURM.

??? question "5. I got an error related to InsufficientSystemResources regarding GPUs during run_lastz in the `blast` rule. What do I do?"

    ##### 5. `blast` GPU error

    If the text of the error is somewhat similar to:

    ```bash
    toil.batchSystems.abstractBatchSystem.InsufficientSystemResources: The job 'run_lastz' kind-run_lastz/instance-tqdjs4tj v1 is requesting [{'count': 4, 'kind': 'gpu', 'api': 'cuda', 'brand': 'nvidia'}] accelerators, more than the maximum of [{'kind': 'gpu', 'brand': 'nvidia', 'api': 'cuda', 'count': 1}, {'kind': 'gpu', 'brand': 'nvidia', 'api': 'cuda', 'count': 1}] accelerators that SingleMachineBatchSystem was configured with. The accelerator {'count': 4, 'kind': 'gpu', 'api': 'cuda', 'brand': 'nvidia'} could not be provided. Scale is set to 1.
    ```

    it may be because your GPU partition is set up to use [MIGs (Multi-instance GPUs) :octicons-link-external-24:](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/){:target="_blank"}. This is essentially like a multi-core CPU, except for GPUs. The problem is that Cactus isn't setup to recognize these as of the last update of this tutorial. It only recognizes physical GPU devices. For instance, let's say you've requested 4 GPUs for your `blast` rule by setting `blast_gpu: 4` in your config file. The BLAST job is submitted to your GPU node, which allocates 2 physical GPUs set up as MIGs, each with 2 instances, which is the equivalent of 4 GPUs. However, cactus only sees the 2 physical GPUs and thinks there aren't enough to accomodate your request for 4, resulting in the error.

    To resolve this, check your cluster documentation to see if there is a way to use only physical GPUs instead of MIGs. If not, you will have to set `blast_gpu: 1` in your config. That is the only way to guarantee that the number of physical GPUs aligns with your request.

    Read more about this [here :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/issues/2){:target="_blank"} and [here :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/issues/1618){:target="_blank"}.

??? question "6. I tried to run the pipeline and I ran into an error that I don't understand or can't resolve. What do I do?"

    ##### 6. Encountering errors

    Please [search for or create an issue on the pipeline's github :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/issues){:target="_blank"} that includes information about your input files, the command you ran, and the error that you are getting. The text of any log files would also be appreciated.

    Additionally, if you are at Harvard, there are [several ways to contact us](../../contact.md) to help you through your errors.

??? question "7. I have an idea to improve or add to the pipeline. What do I do?"

    ##### 7. Pipeline improvements
    
    Great! Please [create an issue on the pipeline's github :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/issues){:target="_blank"} describing your idea so we can discuss its implementation!

---

<style>
    h2 {
        text-align: center !important;
        border-bottom: 2px solid #333333 !important;
        border-top: 2px solid #333333 !important;
        font-weight: 500 !important;
    }
    
    details > h5 {
        font-size: 0.01em !important;       /* almost invisible but still present! */
        color: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Hide all 2nd-level navs */
    .md-nav--secondary .md-nav__item .md-nav {
        display: none !important;
    }

    /* Show when parent has .expanded class */
    .md-nav--secondary .md-nav__item.expanded > .md-nav {
        display: block !important;
    }    
</style>
