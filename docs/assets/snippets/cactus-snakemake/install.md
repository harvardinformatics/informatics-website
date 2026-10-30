### Requirements

You will need several things to be able to run this pipeline:

1. A computing cluster that uses [SLURM :octicons-link-external-24:](https://slurm.schedmd.com/overview.html){:target="_blank"}, which most datasets will need. It should be possible to extend the pipelines to [any job scheduler that Snakemake supports :octicons-link-external-24:](https://github.com/snakemake?q=executor&type=all&language=&sort=){:target="_blank"}.
2. conda or mamba to install software. See [Installing command line software](installing-command-line-software-conda-mamba.md) if you don't have conda/mamba installed.
3. Singularity, installed on your system. The pipelines run Cactus with `singularity exec`, and conda can't install Singularity for you. Apptainer installs usually provide a `singularity` command too. Some clusters (such as the Harvard cluster) already have it installed.
4. The [Harvard Informatics cactus-snakemake pipelines :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/){:target="_blank"}.

You don't need to install Snakemake or its SLURM plugin yourself. The pipelines come with a wrapper script, `cactus_snakemake`, that creates a conda environment with everything they need except Singularity.

### Installing cactus-snakemake

The [pipelines :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/){:target="_blank"} are available on GitHub. Navigate to the directory in which you want to download them, then clone the repository, move into it, and use the wrapper to create the conda environment:

```bash
git clone https://github.com/harvardinformatics/cactus-snakemake.git
cd cactus-snakemake
./cactus_snakemake setup    # create the conda environment from envs/environment.yml
./cactus_snakemake check    # confirm the environment and singularity are ready (read-only)
```

If you have SSH set up on GitHub, you can clone with `git clone git@github.com:harvardinformatics/cactus-snakemake.git` instead. If you don't have or don't wish to use git, you can download the [latest release :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/releases/latest){:target="_blank"}, unzip it, and run the same `setup` and `check` commands from inside the unzipped folder.

`setup` creates a conda environment named `cactus-snakemake`. `check` reports whether that environment exists and is up to date, and whether `singularity` is on your `PATH`. It never creates, updates, or deletes anything. You don't need to activate the environment yourself: the wrapper activates it when it runs a pipeline.

The commands in this tutorial are run from inside the `cactus-snakemake` folder. To run them from somewhere else, give the path to the wrapper instead of `./cactus_snakemake`, for example `/path/to/cactus-snakemake/cactus_snakemake`. Run `./cactus_snakemake help` to see every command and option.

!!! tip "Using a different environment name"

    To use a conda environment with a different name, give `--env-name NAME` **before** the command, for example `./cactus_snakemake --env-name my-cactus-env setup`, or set the environment variable `CACTUS_SMK_ENV_NAME`. If you don't use the default name, you must give it every time you run the wrapper.

!!! warning "Important! cactus-snakemake v3.0.0 and later requires Cactus v3.0.0 or later."

    Due to bug fixes in Cactus, v3.0.0+ of cactus-snakemake is only compatible with Cactus v3.0.0 or later. Don't worry, cactus-snakemake will always use the latest version of Cactus available unless you specify otherwise in your config file. However, if you do wish to use an older version of Cactus, you can use [cactus-snakemake v2.1.0 :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/releases/tag/v2.1.0){:target="_blank"}.

!!! tip "Automatic partition selection"

    Snakemake's SLURM executor plugin can choose a partition for each job based on its resource requests, if you give it a partition config for your cluster with `--slurm-partition-config <path>`. You can then leave the `partition:` entries blank in your pipeline's config file.

    If you are on the Harvard Cannon cluster, we maintain a partition config you can use. See [Snakemake configuration for Cannon partition selection](../snakemake-cannon-config.md) for its location and how to use it.

    If you are not on the Harvard Cannon cluster, you can still directly specify the partitions for each rule in the config file ([see below](#specifying-resources-for-each-rule)), or you may take it upon yourself to [make a partition config :octicons-link-external-24:](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html#automatic-partition-selection){:target="_blank"} for your own cluster.

??? warning "Upgrading from cactus-snakemake v3"

    The way the pipelines are installed and run has changed. If you used cactus-snakemake v3:

    * **Set up the environment with the wrapper.** Run `./cactus_snakemake setup` as shown above. You no longer install Snakemake yourself, and you run the pipelines with `./cactus_snakemake run` instead of `snakemake -s`.
    * **Prep is now a separate, required step.** v3 ran `cactus-prepare` (or `cactus-update-prepare`) every time Snakemake was invoked. Now it runs only during [prep](#prep), and every other run stops until prep has been done for its output directory. For an output directory from v3, run prep once with the same config and input files, then run the pipeline as before.
    * **Two pipelines were renamed.** `cactus_update.smk` is now `cactus_add_genome.smk` (the `add-genome` pipeline) and `cactus_replace.smk` is now `cactus_replace_genome.smk` (the `replace-genome` pipeline), with their config templates renamed to match. Config keys are unchanged.
    * **`skip_prepare` is no longer used.** If it's set, the pipelines log a warning and otherwise ignore it.
