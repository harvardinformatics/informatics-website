---
title: "[Tutorial] Cactus whole genome alignment"
description: "A tutorial and associated Snakemake workflow to generate a whole genome alignment (.hal file) with Cactus."
authors: 
    - Gregg Thomas
---

# Whole genome alignment with Cactus

{{ author_row(page) }}

Comparative genomics requires alignments between sequences from different populations or species. While alignment of small chunks of sequence (e.g. genes) between many species is relatively straightforward, whole genome alignment has been challenging. The [Cactus genome alignment software :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus){:target="_blank"} and its [associated tools :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit){:target="_blank"} has made this task feasible for up to hundreds of genomes. However, this can still be technically difficult to run. Here we have developed a [Snakemake :octicons-link-external-24:](https://snakemake.readthedocs.io/en/stable/){:target="_blank"} pipeline to facilitate running Cactus on a computing cluster. This is done by first running a prep step that uses the `cactus-prepare` command to generate the Cactus labeled phylogeny, which is used to guide the submission of jobs to the cluster. For more details on how Snakemake breaks up Cactus's steps, expand the box below.

??? example "The align pipeline's rulegraph"

    Here is the rulegraph for the pipeline. It works in rounds based on the shape of the input phylogeny (hence the cycle). First, genomes at the tips are masked and then all internal nodes are aligned.

    <center>
        <img src="https://raw.githubusercontent.com/harvardinformatics/cactus-snakemake/main/tests/evolverMammals/rulegraphs-dags/cactus-rulegraph.png" alt="A directed cyclic graph showing the rules for the pipeline.">
    </center>

!!! tip "This pipeline is suitable for aligning genomes from different species"

    For pangenome inference and whole genome alignment between samples of the same species, see our [Cactus-minigraph tutorial](pangenome-cactus-minigraph.md)

## Getting started

<!-- Shared text: docs/assets/snippets/cactus-snakemake/install.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/install.md"

With that, you should be ready to set-up your data for the pipeline!

## Inputs you need to prepare

To run this pipeline, you will need (corresponding config option given in parentheses):

1. A [**rooted**](#how-can-i-tell-if-my-input-newick-tree-is-rooted) phylogenetic tree of all species to align, with or without branch lengths, in [Newick format :octicons-link-external-24:](https://en.wikipedia.org/wiki/Newick_format){:target="_blank"} (specified in `input_file`).
2. The [**softmasked**](#how-can-i-tell-if-my-genome-fasta-files-are-softmasked) genome [FASTA :octicons-link-external-24:](https://en.wikipedia.org/wiki/FASTA_format){:target="_blank"} files for each species (specified in `input_file`).
3. A reference genome to project the alignment to MAF format (`maf_reference`).

You will use these to create the input file for Cactus.

### Preparing the Cactus input file

The various Cactus commands depend on a single input file with information about the genomes to align. This file is a simple tab delimited file. 

The first line of the file contains the **rooted** input species tree in [Newick format :octicons-link-external-24:](https://en.wikipedia.org/wiki/Newick_format){:target="_blank"} and nothing else (be sure to remember the semi-colon at the end of the Newick tree!).

Each subsequent line contains in the first column one tip label from the tree and in the second column the path to the genome FASTA file for that species. 

!!! warning "[The FASTA files must be softmasked!](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/progressive.md#interface)"

    The genomes you provide in FASTA format must be softmasked before running Cactus, otherwise the program will likely not complete. You can tell if a genome FASTA file is masked by the presence of lower-case nucleotides: a, t, c, or g. If your FASTA file has these lower-case characters, it has likely been softmasked. If not, you will have to mask the genome with a tool like [RepeatMasker :octicons-link-external-24:](https://www.repeatmasker.org/){:target="_blank"}. Also importantly, the FASTA files should **not** be **hard** masked, meaning the masked bases are replaced with Ns.

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

In order to run the last step of the workflow that converts the HAL format to a readable MAF format (See [pipeline outputs](#pipeline-outputs) for more info), you will need to select one assembly as a reference assembly. The reference assembly's coordinate system will be used for projection to MAF format. You should indicate the reference assembly in the config file (outlined below). For instance, if I wanted my reference sample in the above file to be **C**, I would put the string `C` in the `maf_reference:` line of the config file.

### Preparing the Snakemake config file

Besides the sequence input, the pipeline needs some extra configuration to know where to look for files and write output. That is done in the config file for a given run. Create a starter config file from the pipeline's template with `init`:

```bash
./cactus_snakemake init align -o my-config.yaml
```

This copies the pipeline's [config template :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/blob/main/config-templates/config-template.yaml){:target="_blank"} (`config-templates/config-template.yaml` in your cactus-snakemake folder) to `my-config.yaml`. Without `-o`, it's written to `./align-config.yaml`. `init` won't overwrite an existing file unless you add `--force`. Fill in the blank fields before running [prep](#prep).

!!! tip "See an example config file"

    The config for the Cactus test data can be found [here :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/blob/main/tests/evolverMammals/evolverMammals-cfg.yaml){:target="_blank"} or at `tests/evolverMammals/evolverMammals-cfg.yaml` in your cactus-snakemake folder.

The config file contains 3 sections: one for specifying the input and output options, one for specifying resources for the various rules (see [below](#specifying-resources-for-each-rule)), and one for optional settings that most runs can leave blank. The first part should look something like this:

```
cactus_path: <path/to/cactus-singularity-image OR download OR version tag (e.g. v3.3.0)>

input_file: <path/to/cactus-input-file>

output_dir: <path/to/desired/output-directory>

final_prefix: <desired name of final .hal and .maf files with all genomes appended>

maf_reference: <Genome ID from input_file>

maf_include_anc: <True/False>

tmp_dir: <path/to/tmp-dir/>

use_gpu: <True/False>
```

Simply replace the string surrounded by <> with the path or option desired. Below is a table summarizing these options, along with the optional setting at the bottom of the config file:

| Option                   | Description                                                                 |
|------------------------- | ----------------------------------------------------------------------------|
| `cactus_path`            | The Cactus Singularity image to use: a file path, a version tag (e.g. `v3.3.0`), or `download` for the latest release. This is needed whether `use_gpu` is True or False. See the box below the table. |
| `input_file`             | Path to the input file containing the species tree and genome paths (described above). |
| `output_dir`             | Directory where all the output will be written. It will be created if it doesn't exist. |
| `final_prefix`           | The name of the final .hal and .maf files with all aligned genomes appended. The final files will be `<final_prefix>.hal` and `<final_prefix>.<maf_reference>.maf` (see [Pipeline outputs](#pipeline-outputs)). These files will be placed within `output_dir`. |
| `maf_reference`          | The label for the genome to use when converting from HAL to MAF. This means that the MAF alignment will be projected on to that genome's coordinate system. |
| `maf_include_anc`        | Whether to include the ancestral genomes in the MAF files (True/False). If `False` (the default), they are left out. |
| `tmp_dir`                | A temporary directory for Snakemake and Cactus to use. Should have lots of space. |
| `use_gpu`                | Whether to use the GPU version of Cactus for the alignment (True/False). |
| `singularity_bind_paths` | **Optional.** A YAML list of extra Singularity bind paths to add to every container command, each in `src[:dest[:opts]]` format, e.g. `/nfs6:/nfs6` or `/scratch:/scratch:rw`. Only needed if some of your files are on a filesystem that isn't available inside the container by default; jobs failing to find files that do exist are the usual sign. Leave blank or set to `[]` to use the cluster defaults only. |

<!-- Shared text: docs/assets/snippets/cactus-snakemake/cactus-image.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/cactus-image.md"

#### Specifying resources for each rule

Below these options in the config file are further options for specifying resource usage for each rule that the pipeline will run, starting with a `default:` entry. For example:

```
rule_resources:
  default:
    partition: shared
    mem_mb: 10000
    cpus: 1
    gpus: 0
    time: 30

  preprocess:
    partition: shared
    mem_mb: 25000
    cpus: 8
    time: 30

  blast:
    partition: gpu     # If use_gpu is True, this must be a partition with GPUs
    mem_mb: 50000
    cpus: 48
    gpus: 2            # Set gpus or gres, not both. Both are ignored if use_gpu is False
    time: 120
```

**The rule _blast_ is the only one that uses GPUs if `use_gpu` is True.**

<!-- Shared text: docs/assets/snippets/cactus-snakemake/resources-gpu.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/resources-gpu.md"

<!-- Shared text: docs/assets/snippets/cactus-snakemake/resources-common.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/resources-common.md"

You will have to determine the proper resource usage for your dataset. Generally, the larger the genomes, the more time and memory each job will need, and the more you will benefit from providing more CPUs and GPUs.

Click below to take a look at an example to get a sense for how many resources you will need to allot, adjusting for the genome size of your organisms. :material-arrow-down-right:

??? example "Example: Resource usage on a dataset of 22 turtle genomes"

    ##### Example: Resource usage on a dataset of 22 turtle genomes

    We have run the pipeline on 22 turtle genomes. The average genome size is 2210 Mb (2.2 Gb):
    
    <center>
        <img src="../../../../img/tutorials/turtles-genome-sizes.png" alt="A boxplot showing a distribution of genome sizes for 22 turtles">
    </center>    
    
    We allocated the following resources for the Cactus rules:

    !!! warning "GPU usage in Cactus has changed over time"

        Note that in this example GPUs were used for 3 rules: **Preprocess**, **Blast**, and **Align**. Current versions of cactus only use GPUs for the **Blast** rule, so you will only see GPU usage and improvements for that rule. See [this issue in the Cactus github repo   :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/issues/1652){:target="_blank"} for more information.

    <center>

    | Step       | Partition | Memory | CPUs | GPUs | Time |
    |------------|-----------|--------|------|------|------|
    | Preprocess | gpu       | 100g   | 8    | 2    | 1h   |
    | Blast      | gpu       | 400g   | 64   | 1    | 12h  |
    | Align      | gpu       | 450g   | 64   | 2    | 12h  |

    </center>

    This resulted in the following real run times:

    <center>
        <img src="../../../../img/tutorials/turtles-cactus-runtime.png" alt="A figure with multiple boxplots showing  the distribution of run time on 22 turtle genomes">
    </center>

    In general, increasing or decreasing CPUs or GPUs available will decrease runtime.

    And max memory usages:

    <center>
        <img src="../../../../img/tutorials/turtles-cactus-maxmem.png" alt="A figure with multiple boxplots showing the distribution of max memory usage on 22 turtle genomes">
    </center>

    Increasing available memory may also decrease runtime.

## Running the pipeline

With [everything installed](#getting-started), the [Cactus input file](#preparing-the-cactus-input-file), and the [config file](#preparing-the-snakemake-config-file) set up, you are now ready to run the pipeline. This takes three steps: prep, a dry-run, and then the real run.

### Prep

Prep is run once for each output directory, before the pipeline itself:

```bash
./cactus_snakemake prep align --configfile my-config.yaml
```

For this pipeline, prep resolves the Cactus image (downloading it if `cactus_path` is `download` or a version tag) and runs `cactus-prepare` to generate the labeled phylogeny that guides the submission of jobs. Its log is written to `<output_dir>/logs/cactus-prepare.log`. `cactus-prepare` also leaves an empty `jobstore/` directory where it's run. It's harmless.

<!-- Shared text: docs/assets/snippets/cactus-snakemake/prep.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/prep.md"

### Do a `--dryrun` first

Next, we want to make sure everything is set up properly by using the `--dryrun` option. This tells Snakemake to display what jobs it is going to run without actually submitting them. This is important to do before actually submitting the jobs so we can catch any setup errors beforehand.

```bash
./cactus_snakemake run align --configfile my-config.yaml -j 20 -e slurm --dryrun
```

<!-- Shared text: docs/assets/snippets/cactus-snakemake/run-command.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/run-command.md"

If this completes successfully, you should see a bunch of blue, yellow, and green text on the screen, ending with a summary of the jobs to be run. For the repo's [test dataset](#test-dataset) (5 genomes and 4 ancestors), it looks like this:

```
Job stats:
job           count
----------  -------
preprocess        5
blast             4
align             4
convert           4
copy_hal          1
append            1
maf               1
all               1
total            21
```

The job counts depend on your data, here on the number of genomes and internal nodes in the tree. The order of the rows can differ between Snakemake versions.

If you see any red text, that likely means an error has occurred that must be addressed before you run the pipeline.

### Submitting the jobs

If you're satisfied that the `--dryrun` has completed successfully and you are ready to start submitting Cactus jobs to the cluster, you can do so by simply removing the `--dryrun` option from the command above:

```bash
./cactus_snakemake run align --configfile my-config.yaml -j 20 -e slurm
```

This will start submitting jobs to SLURM. On your screen, you will see continuous updates regarding job status in blue text. In another terminal, you can also check on the status of your jobs by running `squeue -u <your user id>`. 

<!-- Shared text: docs/assets/snippets/cactus-snakemake/keep-running.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/keep-running.md"

Depending on the number of genomes, their sizes, and your wait in the queue, you will hopefully have your whole genome alignment within a few days!

### Test dataset

Cactus provides a test dataset which we have set up to run in the `tests/evolverMammals/` folder of the cactus-snakemake repo. 

Here is a breakdown of the files so you can investigate them and prepare similar ones for your project:

| File/directory            | Description |
| ------------------------- | ----------- |
| `evolverMammals-seq/`     | This directory contains the input sequence files for the test dataset in FASTA format. |
| `evolverMammals-cfg.yaml` | This is the config file for this pipeline and has all of the options you would need to set up for your own project. |
| `evolverMammals.txt`      | This is the input file as required by Cactus. It has the rooted Newick tree on the first line, followed by lines containing the location of the sequence files for each tip in the tree. |

We recommend running this test dataset before setting up your own project. The config file doesn't need any edits: it downloads the latest Cactus image, uses its own temporary directory inside `tests/evolverMammals/`, and leaves the partitions blank. Its output is written to `tests/evolverMammals/evolverMammals-align-out/`.

The paths in the config file are relative to the dataset's folder, so the test is run from there. Change into `tests/evolverMammals/`, then run prep and a dry-run:

```bash
cd tests/evolverMammals/
../../cactus_snakemake prep align --configfile evolverMammals-cfg.yaml
../../cactus_snakemake run align --configfile evolverMammals-cfg.yaml -j 20 -e slurm --dryrun
```

Prep downloads the Cactus image once, into `tests/evolverMammals/`. If the dry-run completes without error, run the pipeline by removing the `--dryrun` option:

```bash
../../cactus_snakemake run align --configfile evolverMammals-cfg.yaml -j 20 -e slurm
```

Since the partitions are blank, you can optionally add `--slurm-partition-config <path>` to these commands to have partitions selected automatically.

## Pipeline outputs

The pipeline will output a [.paf :octicons-link-external-24:](https://github.com/lh3/miniasm/blob/master/PAF.md){:target="_blank"}, a [.hal :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/hal/blob/master/README.md){:target="_blank"}, and a [.fa :octicons-link-external-24:](https://en.wikipedia.org/wiki/FASTA_format){:target="_blank"} file for every node in the input tree (including ancestral sequences). The final alignment file will be `<final_prefix>.hal`, where `<final_prefix>` is whatever you specified in the config file. 

The final alignment will also be presented in MAF format as `<final_prefix>.<maf_reference>.maf`, again where `<maf_reference>` is whatever you set in the config file. This file will include duplicate sequences. Another MAF file, `<final_prefix>.<maf_reference>.nodupes.maf` will also be generated, which is the alignment in MAF format with no duplicate sequences. The de-duplicated MAF file is generated with `--dupeMode single`. By default (`maf_include_anc: False`), the ancestral genomes are left out of the MAF files (`cactus-hal2maf --noAncestors`). Set `maf_include_anc: True` to include them. See the [Cactus documentation regarding MAF export :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/progressive.md#maf-export){:target="_blank"} for more info.

Prep also writes `<output_dir>/prep-manifest.yaml`, its record of what it did. The `<output_dir>/logs/` folder holds `cactus-prepare.log` and, for each preprocess job, a `<genome>.preprocess.seqfile.txt`: the copy of the input file given to `cactus-preprocess`, kept for reference.

A suite of tools called [HAL tools :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/Hal){:target="_blank"} is included with the Cactus singularity image if you need to manipulate or analyze .hal files. There are many tools for manipulating MAF files, though they are not always easy to use. The makers of Cactus also develop [taffy :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/taffy){:target="_blank"}, which can manipulate MAF files by converting them to TAF files.

## Questions/troubleshooting

??? question "How can I tell if my input Newick tree is rooted? If it isn't rooted, how can I root it? Or if it is rooted, how can I re-root it?"

    ##### How can I tell if my input Newick tree is rooted?

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
    write.tree(rooted_tree, file="your-rooted-tree.nwk")
    ```

<!-- Shared text: docs/assets/snippets/cactus-snakemake/troubleshooting-cactus.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/troubleshooting-cactus.md"

<!-- Shared text: docs/assets/snippets/cactus-snakemake/troubleshooting-common.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/troubleshooting-common.md"

---

<!-- --------------------------------- -->
<!-- Page specfic CSS -->

<style>
    /* ----- */
    /* Section headers */
    h2 {
        text-align: center !important;
        border-bottom: 2px solid #333333 !important;
        border-top: 2px solid #333333 !important;
        font-weight: 500 !important;
    }
    
    /* ----- */
    /* For the admonitions, so they have an entry in the toc that doesn't show up on the page */
    details > h5 {
        font-size: 0.01em !important;       /* almost invisible but still present! */
        color: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* ----- */
    /* Hide all 2nd-level navs */
    .md-nav--secondary .md-nav__item .md-nav {
        display: none !important;
    }

    /* Show when parent has .expanded class, which is added by js/collapse_toc.js */
    .md-nav--secondary .md-nav__item.expanded > .md-nav {
        display: block !important;
    }    
</style>

