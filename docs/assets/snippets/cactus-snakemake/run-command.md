??? info "Command breakdown"

    | Command-line option                       | Description |
    | ----------------------------------------- | ----------- |
    | `./cactus_snakemake run`                  | Activates the pipelines' conda environment and runs Snakemake. Everything after the pipeline name is passed to Snakemake unchanged. |
    | `<pipeline>`                              | The pipeline to run: `align`, `add-genome`, `replace-genome`, `add-outgroup`, or `minigraph`. This picks the workflow file (Snakefile), so don't give `-s` or `--snakefile`. |
    | `--configfile my-config.yaml`             | The path to your config file. See: [Preparing the Snakemake config file](#preparing-the-snakemake-config-file). |
    | `-j 20`                                   | The maximum number of jobs that will be submitted to your cluster at one time. Always give it with `-e slurm`: recent Snakemake versions require it, even for a dry-run. |
    | `-e slurm`                                | Use the SLURM executor plugin to submit jobs to the cluster. If you leave out `-e` and aren't in a SLURM allocation, the wrapper warns that everything will run on the current node. |
    | `--dryrun`                                | Do not execute anything, just display what would be done. |
    | `--slurm-partition-config <path>`         | Optional. Lets the SLURM plugin choose a partition for each job, so the `partition:` entries in your config can be left blank. On the Harvard Cannon cluster, see [our partition config](../snakemake-cannon-config.md). |
    | `--retries N`                             | Optional. Resubmit failed jobs up to N times, using per-attempt resources if you've set them (see [Specifying resources for each rule](#specifying-resources-for-each-rule)). |
