??? question "My jobs were running but my Snakemake process crashed because of connection issues/server maintenance! What do I do?"

    ##### Snakemake crashes

    As long as there wasn't an error with one of the jobs, Snakemake is designed to be able to resume and resubmit jobs pretty seamlessly. You just need to run the same `./cactus_snakemake run` command you ran to begin with and it should pick up submitting jobs where it left off. You don't need to run prep again. You could also run a `--dryrun` first and it should tell you which jobs are left to be done.

??? question "My run stopped with an error about prep. What do I do?"

    ##### Prep errors

    Every run reads the record prep wrote, `<output_dir>/prep-manifest.yaml`, and stops if:

    * **prep hasn't been run for this output directory.** Run the prep command given in the error, then run the pipeline again.
    * **the config or input files that prep depended on have changed since prep was run,** or a file prep wrote has been changed. The error lists what changed. If you didn't mean to make those changes, undo them. If you did, run prep again with `--force`:

        ```bash
        ./cactus_snakemake prep <pipeline> --configfile my-config.yaml --force
        ```

        Files already in the output directory were made from the earlier prep and are not deleted. If the change affects the tree, starting over in a new output directory is usually the safer choice.

    See [Prep](#prep) for more information.

??? question "I want to run this on a cluster with a job scheduler other than SLURM! What do I do?"

    ##### Clusters other than SLURM?

    Generally, it should be relatively easy to install and use the appropriate [Snakemake cluster executor :octicons-link-external-24:](https://github.com/snakemake?q=executor&type=all&language=&sort=){:target="_blank"}.

    If you need help or run into problems, please [create an issue on the pipeline's github :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/issues){:target="_blank"} and we'll try and help - though it will likely be up to you to test on your own cluster, since we only have easy access to a cluster running SLURM.

??? question "I tried to run the pipeline and I ran into an error that I don't understand or can't resolve. What do I do?"

    ##### Encountering errors

    Please [search for or create an issue on the pipeline's github :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/issues){:target="_blank"} that includes information about your input files, the command you ran, and the error that you are getting. The text of any log files would also be appreciated.

    Additionally, if you are at Harvard, there are [several ways to contact us](../../contact/index.md) to help you through your errors.

??? question "I have an idea to improve or add to the pipeline. What do I do?"

    ##### Pipeline improvements

    Great! Please [create an issue on the pipeline's github :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/issues){:target="_blank"} describing your idea so we can discuss its implementation!

??? question "Can I run the pipelines without the `cactus_snakemake` wrapper?"

    ##### Running without the wrapper

    Yes, though we recommend the wrapper for most users. The wrapper only runs Snakemake for you, so the same steps work with Snakemake directly, from a conda environment that has the packages listed in `envs/environment.yml` in the `cactus-snakemake` folder.

    Without the wrapper, you give the pipeline's workflow file (Snakefile) with `-s`:

    | Pipeline         | Snakefile                   |
    | ---------------- | --------------------------- |
    | `align`          | `cactus.smk`                |
    | `add-genome`     | `cactus_add_genome.smk`     |
    | `replace-genome` | `cactus_replace_genome.smk` |
    | `add-outgroup`   | `cactus_add_outgroup.smk`   |
    | `minigraph`      | `cactus_minigraph.smk`      |

    The prep, dry-run, and run steps are then, shown here for the `align` pipeline from inside the `cactus-snakemake` folder:

    ```bash
    snakemake -s cactus.smk --configfile my-config.yaml --config prep=T
    snakemake -s cactus.smk --configfile my-config.yaml -j 20 -e slurm --dryrun
    snakemake -s cactus.smk --configfile my-config.yaml -j 20 -e slurm
    ```

    As with the wrapper, the prep step is required once per output directory before the pipeline can run. These options can be given with `--config`:

    | Command line flag              | Description |
    | ------------------------------ | ----------- |
    | `--config prep=T`              | Run the prep step and exit. Required once per output directory before the pipeline can run. |
    | `--config prep=T prep_force=T` | Run prep again even though the config or input files have changed since the last prep. |
    | `--config debug=T`             | The same as prep, but display extra information about the pre-processing steps. |
    | `--config display=T`           | Print the current config settings and exit. |
    | `--config info=T`              | Display some information about the pipelines, including version and last commit date. |
    | `--config version=T`           | Display the version of the pipeline. |
