---
title: Whole genome alignment with Cactus
---

<style>
/* FAQ styles */
    details > h5 {
        display: none;
    }
</style>

Comparative genomics requires alignments between sequences from different populations or species. While alignment of small chunks of sequence (e.g. genes) between many species is relatively straightforward, whole genome alignment has been challenging. The [Cactus genome alignment software](https://github.com/ComparativeGenomicsToolkit/cactus) and its [associated tools](https://github.com/ComparativeGenomicsToolkit) has made this task feasible for up to hundreds of genomes. However, this can still be technically difficult to run. Here we have developed a [Snakemake](https://snakemake.readthedocs.io/en/stable/) pipeline to facilitate running Cactus on a computing cluster. This is done by first running the `cactus-prepare` command to generate the Cactus labeled phylogeny, which is used to guide the submission of jobs to the cluster.

## Getting started

You will need several things to be able to run this pipeline:

1. A computing cluster that uses [SLURM](https://slurm.schedmd.com/overview.html), though it should be possible to extend it to [any job scheduler that Snakemake supports](https://github.com/snakemake?q=executor&type=all&language=&sort=).
2. conda or mamba to install software. See [Installing command line software](installing-command-line-software.md) if you don't have conda/mamba installed.
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

1. A [**rooted**](#3-how-can-i-tell-if-my-input-newick-tree-is-rooted) phylogenetic tree of all species to align, with or without branch lengths, in [Newick format](https://en.wikipedia.org/wiki/Newick_format).
2. The [**softmasked**](#4-how-can-i-tell-if-my-genome-fasta-files-are-softmasked) genome [FASTA](https://en.wikipedia.org/wiki/FASTA_format) files for each species.

You will use these to create the input file for Cactus.

### Preparing the Cactus input file

The various Cactus commands depend on a single input file with information about the genomes to align. This file is a simple tab delimited file. 

The first line of the file contains the **rooted** input species tree in [Newick format](https://en.wikipedia.org/wiki/Newick_format) and nothing else (be sure to remember the semi-colon at the end of the Newick tree!).

Each subsequent line contains in the first column one tip label from the tree and in the second column the path to the genome FASTA file for that species. 

!!! warning "[The FASTA files must softmasked!](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/progressive.md#interface)"

    The genomes you provide in FASTA format must be softmasked before running Cactus, otherwise the the program will likely not complete. You can tell if a genome FASTA file is masked by the presence of lower-case nucleotides: a, t, c, or g. If your FASTA file has these lower-case characters, it has likely been softmasked. If not, you will have to mask the genome with a tool like [RepeatMasker](https://www.repeatmasker.org/). Also importantly, the FASTA files should **not** be **hard** masked, meaning the masked bases are replaced with Ns.

For example, if one were running this pipeline on 5 species named A, B, C, D, and E, the input file may look something like this:

```
(((A,B),(C,D)),E);
A   seqdir/a.fa
B   seqdir/b.fa
C   seqdir/c.fa
D   seqdir/d.fa
E   seqdir/e.fa
```

For more information about the Cactus input file, see their [official documentation](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/progressive.md#interface). There is also an example input file for a small test dataset [here](https://github.com/harvardinformatics/cactus-snakemake/blob/main/tests/evolverMammals.txt) or at `tests/evolverMammals.txt`.


### Preparing the Snakemake config file

!!! tip "Be sure to start with the example config file as a template!"

    The config for the Cactus test data can be found at [here](https://github.com/harvardinformatics/cactus-snakemake/blob/main/tests/evolverMammals-cfg.yaml) or at `tests/evolverMammals-cfg.yaml` in your downloaded cactus-snakemake repo. Be sure to use this as the template for your project since it has all the options needed!

Besides the sequence input, the pipeline needs some extra configuration to know where to look for files and write output. That is done in the Snakemake configuration file for a given run. It contains 2 sections, one for specifying the input and output options, and one for specifying resources for the various rules (see [below](#specifying-resources-for-each-rule)). The first part should look something like this:

```
working_dir: <path/to/working-directory/>

cactus_path: <path/to/cactus-singularity-image OR download>

input_file: <path/to/cactus-input-file>

output_dir: <path/to/desired/output-directory>

overwrite_output_dir: <True/False>

final_hal: <desired name of final .hal file with all genomes appended>

tmp_dir: <path/to/tmp-dir/>

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
| `final_hal`          | The name of the final .hal file with all aligned genomes appended. Will be placed within `output_dir` |
| `tmp_dir`            | A temporary directory for Snakemake and Cactus to use. Should have lots of space.|
| `use_gpu`            | Whether to use the GPU version of Cactus for the alignment (True/False)     |

#### Specifying resources for each rule

Below these options in the config file are further options for specifying resource usage for each rule that the pipeline will run. For example:

```
mask_partition: "gpu_test"
mask_gpu: 1
mask_cpu: 8
mask_mem: 25000
mask_time: 30
```

!!! warning "Notes on resource allocation"

    * **Allocate the proper partitions based on `use_gpu`.** If you want to use the GPU version of cactus (*i.e.* you have set `use_gpu: True` in the config file), the partition for the rules **mask**, **blast**, and **align** must be GPU enabled. If not, the pipeline will fail to run.
    * The `gpu:` options will be ignored if `use_gpu: False` is set.
    * **mem is in MB** and **time is in minutes**.

You will have to determine the proper resource usage for your dataset. Generally, the larger the genomes, the more time and memory each job will need, and the more you will benefit from providing more CPUs and GPUs.

Click below to take a look at an example to get a sense for how many resources you will need to allot, adjusting for the genome size of your organisms. :material-arrow-down-right:

??? example "Example: Resource usage on a dataset of 22 turtle genomes"

    ##### Example: Resource usage on a dataset of 22 turtle genomes

    We have run an earlier version of the pipeline on 22 turtle genomes. The average genome size is 2200 Mb (2.2 Gb). We allocated the following resources for the Cactus rules:

    | Step    | Partition | Memory | CPUs | GPUs | Time |
    |---------|-----------|--------|------|------|------|
    | Mask    | gpu       | 100g   | 64   | 4    | 2h   |
    | Blast   | gpu       | 400g   | 64   | 4    | 48h  |
    | Align   | bigmem    | 450g   | 64   | NA   | 48h  |

    !!! note "**Note: At the time we ran this dataset, the Align step was not GPU enabled.**"

        That has changed in the current version, so the align step probably won't take as long or require as much memory.

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
    
### The SLURM config file

Another required file is the one that configures Snakemake for SLURM. This is located in `profiles/slurm_profile/config.yaml` and looks like this:

```
jobs: 40
executor: slurm
default-resources:
  - slurm_partition='shared'
  - cpus_per_task=8
  - mem_mb=100000
  - runtime=1440
restart-times: 0
latency-wait: 15
verbose: true 
```

In general, you won't need to worry about changing anything in this file unless you want to. The exception being the `jobs` parameter, which controls the max number of jobs that are submitted to SLURM simultaneously.

## Running the pipeline

With [everything installed](#getting-started), the [Cactus input file](#preparing-the-cactus-input-file), and the [Snakemake configuration file](#preparing-the-snakemake-config-file) setup, you are now ready to run the pipeline.

### Do a `--dryrun` first

First, we want to make sure everything is setup properly by using the `--dryrun` option. This tells Snakemake to display what jobs it is going to run without actually submitting them. This is important to do before actually submitting the jobs so we can catch any setup errors beforehand.

This is done with the following command from within the `cactus-snakemake` repo directory, changing the `--configfile` path to the one you have created for your project:

```bash
snakemake -p -s cactus_gpu.smk --configfile <path/to/your/snakmake-config.yml> --profile profiles/slurm_profile/ --dryrun
```

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
mask            5
total          20

Reasons:
    (check individual jobs above for details)
    input files updated by another job:
        align, all, append, blast, convert, copy_hal
    output files have to be generated:
        align, append, blast, convert, copy_hal, mask

This was a dry-run (flag -n). The order of jobs does not reflect the order of execution.
```

If you see any red text, that likely means an error has occurred that must be addressed before you run the pipeline.

### Submitting the jobs

If you're satisfied that the `--dryrun` has completed successfully and you are ready to start submitting Cactus jobs to the cluster, you can do so by simply removing the `--dryrun` option from the command above:

```bash
snakemake -p -s cactus_gpu.smk --configfile <path/to/your/snakmake-config.yml> --profile profiles/slurm_profile/
```

This will start submitting jobs to SLURM. On your screen, you will see continuous updates regarding job status in blue text. In another terminal, you can also check on the status of your jobs by running `squeue -u <your user id>`. 

!!! tip "Be sure you have a way to keep the main Snakemake process running."

    Remember, that some of these steps can take a long time, or your jobs may be stuck in the queue for a while. That means the Snakemake job must have a persistent connection in order to keep running an submitting jobs. There are a few ways this can be accomplished, some better than ~~others~~:

    1. ~~Keep your computer on and connected to the cluster. This may be infeasible and you may still suffer from connection issues.~~

    2. ~~Run the Snakemake job in the background by using `nohup <snakemake command> &`. This will run the command in the background and persist even if you disconnect. However, it makes it difficult to check on the status of your command.~~

    3. Submit the Snakemake command itself as a SLURM job. This will require [preparing and submitting a job script](https://docs.rc.fas.harvard.edu/kb/running-jobs/). This is a good solution.

    4. Use a [terminal multiplexer](https://en.wikipedia.org/wiki/Terminal_multiplexer) like [GNU Screen](https://en.wikipedia.org/wiki/GNU_Screen) or [tmux](https://en.wikipedia.org/wiki/Tmux). These programs allow you to open a sub-terminal within your currently connected terminal that remains even after you disconnect from the server. This is also a good solution.

Depending on the number of genomes, their sizes, and your wait in the queue, you will hopefully have your whole genome alignment within a few days!

??? example "The cactus-snakemake pipeline's rulegraph"

    Here is the rulegraph for the pipeline. It works in rounds based on the shape of the input phylogeny (hence the cycle). First, genomes at the tips are masked and then all internal nodes are aligned.

    <center>
        <img src="../../img/cactus-snakemake-rulegraph.png" alt="A directed cyclic graph showing the rules for the pipeline.'">
    </center>

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

??? question "3. How can I tell if my input Newick tree is rooted? If it isn't rooted, how can I root it? Or if it is rooted, how can I re-root it?"

    ##### 3. How can I tell if my input Newick tree is rooted?

    The easiest way to check if your tree is rooted is probably to load the tree into [R](https://www.r-project.org/) with the `ape` package. This can be done with the following commands:

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

??? question "4. How can I tell if my genome FASTA files are softmasked? How can I mask them if they aren't already?"

    ##### 4. How can I tell if my genome FASTA files are softmasked?

    Cactus requires the input genomes to be softmasked. This means that masked bases appear as lower case letters: a, t, c, g. Hopefully the source of your genome FASTA file has given you some information about how it was prepared, including how it was masked. If not, a very quick method to check for the occurrence of any lower case letter in the sequence is:

    ```bash
    if grep -q '^[^>]*[a-z]' your-genome-file.fa; then echo "The FASTA file is soft-masked."; else echo "The FASTA file is NOT soft-masked."; fi
    ```

    This is fast, but only detects the occurrence of a single lower case character. To count all the lower case characters at the cost of taking a couple of minutes, you can run:

    ```bash
    awk 'BEGIN{count=0} !/^>/{for(i=1;i<=length($0);i++) if (substr($0,i,1) ~ /[acgt]/) count++} END{print count}' your-genome-file.fa
    ```

    Importantly, your genomes [should not be **hard** masked](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/progressive.md#interface), which means that masked bases are replaced by Ns. Unfortunately, there are many reasons for Ns to appear in a genome fasta file, so it is difficult to tell if it is because it is hardmasked based on the presence of Ns alone. Hopefully the source of the file has left some documentation describing how it was prepared...

    If your genomes are not softmasked and you wish to do so, you will have to run a program like [RepeatMasker](https://www.repeatmasker.org/) or [RepeatModeler](https://github.com/Dfam-consortium/RepeatModeler) on it. Please consult the documentation for these tools.

??? question "5. I want to run this on a cluster with a job scheduler other than SLURM! What do I do?"

    ##### 5. Clusters other than SLURM?

    Generally, it should be relatively easy to update the cluster profile (`profiles/slurm_profile/config.yaml`) and use the appropriate [Snakemake cluster executor](https://github.com/snakemake?q=executor&type=all&language=&sort=).

    If you need help or run into problems, please [create an issue on the pipeline's github](https://github.com/harvardinformatics/cactus-snakemake/issues) and we'll try and help - though it will likely be up to you to test on your own cluster, since we only have easy access to a cluster running SLURM.

??? question "6. I tried to run the pipeline and I ran into an error that I don't understand or can't resolve. What do I do?"

    ##### 6. Encountering errors

    Please [search for or create an issue on the pipeline's github](https://github.com/harvardinformatics/cactus-snakemake/issues) that includes information about your input files, the command you ran, and the error that you are getting. The text of any log files would also be appreciated.

    Additionally, if you are at Harvard, there are [several ways to contact us](../../contact.md) to help you through your errors.

??? question "7. I have an idea to improve or add to the pipeline. What do I do?"

    ##### 7. Pipeline improvements
    
    Great! Please [create an issue on the pipeline's github](https://github.com/harvardinformatics/cactus-snakemake/issues) describing your idea so we can discuss its implementation!
