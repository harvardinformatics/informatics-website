---
title: "[Tutorial] Pangenomes with Minigraph-Cactus"
description: "A tutorial and associated Snakemake workflow for infering a pangenome with Minigraph-Cactus."
authors: 
    - Gregg Thomas
---

# Pangenome inference with Minigraph-Cactus

{{ author_row(page) }}

For aligning genome assemblies from the same species for population genomic analyses, the [Cactus genome alignment software :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus){:target="_blank"} has [implemented a workflow :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/pangenome.md){:target="_blank"} using [minigraph :octicons-link-external-24:](https://github.com/lh3/minigraph){:target="_blank"}. However, this can still be technically difficult to run. Here we have developed a [Snakemake :octicons-link-external-24:](https://snakemake.readthedocs.io/en/stable/){:target="_blank"} pipeline to facilitate running Minigraph-Cactus on a computing cluster. For more details on how Snakemake breaks up Minigraph-Cactus's steps, expand the box below.

??? example "The minigraph pipeline's rulegraph"

    Here is the rulegraph for the pipeline. The **split** rule breaks up the workflow by chromosome/scaffold for efficient submission of **align** steps, with **align** picking up where **split** left off.

    <center>
        <img src="https://raw.githubusercontent.com/harvardinformatics/cactus-snakemake/main/tests/yeast-minigraph/rulegraphs-dags/cactus-minigraph-rulegraph.png" alt="A directed acyclic graph showing the rules for the pipeline.">
    </center>

!!! tip "This pipeline is suitable for aligning and constructing pangenomes from samples of the same species"

    For whole genome alignment between different species, see our [Cactus whole genome alignment tutorial](whole-genome-alignment-cactus.md)

## Getting started

<!-- Shared text: docs/assets/snippets/cactus-snakemake/install.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/install.md"

With that, you should be ready to set-up your data for the pipeline!

## Inputs you need to prepare

To run this pipeline, you will need (corresponding config option given in parentheses):

1. The assembled genome [FASTA :octicons-link-external-24:](https://en.wikipedia.org/wiki/FASTA_format){:target="_blank"} files for each sample (specified in `input_file`).
2. A reference sample (`reference`).

You will use these to create the input file for Minigraph-Cactus.

### Preparing the Minigraph-Cactus input file

The various Minigraph-Cactus commands depend on a single input file with information about the genomes to align. This file is a simple tab delimited file with two columns. 

Each line contains in the first column one sample label and in the second column the path to the genome FASTA file for that sample. 

!!! note "Unlike regular Cactus, Minigraph-Cactus does not require the input sequences to be softmasked"

    However, the FASTA files should still **not** be **hard** masked, meaning masked bases are replaced with Ns.

For example, if one were running this pipeline on 5 samples named A, B, C, D, and E, the input file may look something like this:

```
A   seqdir/a.fa
B   seqdir/b.fa
C   seqdir/c.fa
D   seqdir/d.fa
E   seqdir/e.fa
```

There is much more information about the Minigraph-Cactus input file in the [official documentation for Minigraph-Cactus :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/pangenome.md#interface){:target="_blank"}, including how to run the pipeline with diploid assemblies. There is also an example input file for a small test dataset [here :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/blob/main/tests/yeast-minigraph/yeastPangenome-local.txt){:target="_blank"} or at `tests/yeast-minigraph/yeastPangenome-local.txt`. For more info, see section: [Test dataset](#test-dataset).

### Reference sample

Minigraph-Cactus requires that you select one sample as a reference sample [for a variety of reasons :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/pangenome.md#reference-sample){:target="_blank"}. Keep these in mind as you prepare your inputs. The reference sample will be indicated in the config file (outlined below). For instance, if I wanted my reference sample in the above file to be **C**, I would put the string `C` in the `reference:` line of the config file.

### Preparing the Snakemake config file

Besides the sequence input, the pipeline needs some extra configuration to know where to look for files and write output. That is done in the config file for a given run. Create a starter config file from the pipeline's template with `init`:

```bash
./cactus_snakemake init minigraph -o my-config.yaml
```

This copies the pipeline's [config template :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/blob/main/config-templates/minigraph-config-template.yaml){:target="_blank"} (`config-templates/minigraph-config-template.yaml` in your cactus-snakemake folder) to `my-config.yaml`. Without `-o`, it's written to `./minigraph-config.yaml`. `init` won't overwrite an existing file unless you add `--force`. Fill in the blank fields before running [prep](#prep).

!!! tip "See an example config file"

    The config for the Minigraph-Cactus test data can be found [here :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/blob/main/tests/yeast-minigraph/yeast-minigraph-cfg.yaml){:target="_blank"} or at `tests/yeast-minigraph/yeast-minigraph-cfg.yaml` in your cactus-snakemake folder.

The config file contains 3 sections: one for specifying the input and output options, one for specifying resources for the various rules (see [below](#specifying-resources-for-each-rule)), and one for optional settings that most runs can leave blank. The first part should look something like this:

```
cactus_path: <path/to/cactus-singularity-image OR download OR version tag (e.g. v3.3.0)>

input_file: <path/to/cactus-input-file>

output_dir: <path/to/desired/output-directory>

reference: <Sample ID from input_file>

prefix: <string>

join_graph_type: <string. options: full, clip, filter>

join_filter: <integer>

tmp_dir: <path/to/tmp-dir/>
```

Simply replace the string surrounded by <> with the path or option desired. Below is a table summarizing these options, along with the optional setting at the bottom of the config file:

| Option                   | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `cactus_path`            | The Cactus Singularity image to use: a file path, a version tag (e.g. `v3.3.0`), or `download` for the latest release. See the box below the table. |
| `input_file`             | Path to the input file containing the sample IDs and genome paths (described above). |
| `output_dir`             | Directory where all the output will be written. It will be created if it doesn't exist. |
| `reference`              | The sample ID from the input file to serve as the reference for pangenome creation. |
| `prefix`                 | A string that will be appended to all files created by the pipeline. |
| `join_graph_type`        | Controls the level of filtering on the final files. One of "full", "clip", or "filter". |
| `join_filter`            | Only applicable for `join_graph_type: filter`. The minimum number of haplotypes that must be present in a node for it to be retained. |
| `tmp_dir`                | A temporary directory for Snakemake and Cactus to use. It will be created if it doesn't exist, but should be somewhere with lots of space. |
| `singularity_bind_paths` | **Optional.** A YAML list of extra Singularity bind paths to add to every container command, each in `src[:dest[:opts]]` format, e.g. `/nfs6:/nfs6` or `/scratch:/scratch:rw`. Only needed if some of your files are on a filesystem that isn't available inside the container by default; jobs failing to find files that do exist are the usual sign. Leave blank or set to `[]` to use the cluster defaults only. |

For `join_graph_type` and `join_filter`, see [the Cactus docs :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/pangenome.md#clipping-filtering-and-indexing){:target="_blank"} for more info.

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
    time: 30

  minigraph:
    partition: shared
    mem_mb: 25000
    cpus: 8
    time: 30
```

**The steps in the Minigraph-Cactus pipeline are not GPU compatible, so there are no GPU options in this pipeline.**

<!-- Shared text: docs/assets/snippets/cactus-snakemake/resources-common.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/resources-common.md"

You will have to determine the proper resource usage for your dataset. Generally, the larger the genomes, the more time and memory each job will need, and the more you will benefit from providing more CPUs.

## Running the pipeline

With [everything installed](#getting-started), the [Minigraph-Cactus input file](#preparing-the-minigraph-cactus-input-file), and the [config file](#preparing-the-snakemake-config-file) set up, you are now ready to run the pipeline. This takes three steps: prep, a dry-run, and then the real run.

### Prep

Prep is run once for each output directory, before the pipeline itself:

```bash
./cactus_snakemake prep minigraph --configfile my-config.yaml
```

For this pipeline, prep only resolves the Cactus image, downloading it if `cactus_path` is `download` or a version tag. Minigraph-Cactus has no prepare command.

<!-- Shared text: docs/assets/snippets/cactus-snakemake/prep.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/prep.md"

### Do a `--dryrun` first

Next, we want to make sure everything is set up properly by using the `--dryrun` option. This tells Snakemake to display what jobs it is going to run without actually submitting them. This is important to do before actually submitting the jobs so we can catch any setup errors beforehand.

```bash
./cactus_snakemake run minigraph --configfile my-config.yaml -j 20 -e slurm --dryrun
```

<!-- Shared text: docs/assets/snippets/cactus-snakemake/run-command.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/run-command.md"

If this completes successfully, you should see a bunch of blue, yellow, and green text on the screen, ending with a summary of the jobs to be run. For the repo's [test dataset](#test-dataset) (6 yeast genomes, with S288C as the reference), it looks like this:

```
Job stats:
job           count
----------  -------
copy_input        1
minigraph         1
graphmap          1
split             1
join              1
all               1
total             6
```

The order of the rows can differ between Snakemake versions.

!!! warning "The number of jobs will be higher than indicated by the dryrun!"
    
    Note that rule **align** does not appear in the list of jobs to run. The dry-run stops at rule **split**, which is a checkpoint in Snakemake terms, and Snakemake prints: "The run involves checkpoint jobs, which will result in alteration of the DAG of jobs (e.g. adding more jobs) after their completion." The **align** jobs are added once **split** has run, so they will be run! The total number of jobs will be the number reported during the dryrun + the number of chromosomes in your reference sample (1 align job per chromosome).

If you see any red text, that likely means an error has occurred that must be addressed before you run the pipeline. 

### Submitting the jobs

If you're satisfied that the `--dryrun` has completed successfully and you are ready to start submitting Cactus jobs to the cluster, you can do so by simply removing the `--dryrun` option from the command above:

```bash
./cactus_snakemake run minigraph --configfile my-config.yaml -j 20 -e slurm
```

This will start submitting jobs to SLURM. On your screen, you will see continuous updates regarding job status in blue text. In another terminal, you can also check on the status of your jobs by running `squeue -u <your user id>`. 

<!-- Shared text: docs/assets/snippets/cactus-snakemake/keep-running.md -->

--8<-- "docs/assets/snippets/cactus-snakemake/keep-running.md"

Depending on the number of genomes, their sizes, and your wait in the queue, you will hopefully have your whole genome alignment within a few days!

### Test dataset

Cactus provides a test dataset which we have set up to run in the `tests/yeast-minigraph/` folder of the cactus-snakemake repo. 

Here is a breakdown of the files so you can investigate them and prepare similar ones for your project:

| File/directory             | Description |
| -------------------------- | ----------- |
| `seq/`                     | This directory contains the input sequence files for the test dataset in FASTA format. |
| `yeast-minigraph-cfg.yaml` | This is the config file for this pipeline and has all of the options you would need to set up for your own project. |
| `yeastPangenome-local.txt` | This is the input file as required by Minigraph-Cactus. It has lines containing the location of the sequence files for each sample. |

We recommend running this test dataset before setting up your own project. The config file doesn't need any edits: it downloads the latest Cactus image, uses its own temporary directory inside `tests/yeast-minigraph/`, and leaves the partitions blank. Its output is written to `tests/yeast-minigraph/yeast-minigraph-out/`.

The paths in the config file are relative to the dataset's folder, so the test is run from there. Change into `tests/yeast-minigraph/`, then run prep and a dry-run:

```bash
cd tests/yeast-minigraph/
../../cactus_snakemake prep minigraph --configfile yeast-minigraph-cfg.yaml
../../cactus_snakemake run minigraph --configfile yeast-minigraph-cfg.yaml -j 20 -e slurm --dryrun
```

Prep downloads the Cactus image once, into `tests/yeast-minigraph/`. If the dry-run completes without error, run the pipeline by removing the `--dryrun` option:

```bash
../../cactus_snakemake run minigraph --configfile yeast-minigraph-cfg.yaml -j 20 -e slurm
```

Since the partitions are blank, you can optionally add `--slurm-partition-config <path>` to these commands to have partitions selected automatically.

## Pipeline outputs

The pipeline produces many output files including `.hal`, the Cactus alignment format, `.gfa`, the graphical fragment assembly format, `.vcf`, the variant call format, and `.vg`, the variation graph format.

For more information about all outputs, see [Cactus's minigraph documentation section about output :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/pangenome.md#output){:target="_blank"}.

## Questions/troubleshooting

??? question "The Minigraph-Cactus docs say to not use hardmasked genomes. How can I tell if my genome FASTA files are hardmasked?"

    ##### How can I tell if my genome FASTA files are hardmasked?

    Hardmasking means you replace low quality or low confidence bases in your assembly with N characters. Unfortunately, there are many reasons for Ns to appear in a genome fasta file, so it is difficult to tell if it is because it is hardmasked based on the presence of Ns alone. Hopefully the source of the file has left some documentation describing how it was prepared...

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
