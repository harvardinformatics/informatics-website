!!! warning "Notes on resource allocation"

    * Be sure to use partition names appropriate for your cluster. Several examples in this tutorial have partition names that are specific to the Harvard cluster, so be sure to change them.
    * **If you run with `-e slurm --slurm-partition-config <path to your cluster's partition config>`, you can leave the `partition:` fields blank** and one will be selected for each job based on its other resources. On the Harvard Cannon cluster, you can use [our partition config :material-arrow-top-right:](../snakemake-cannon-config.md){:target="_blank"}.
    * The `default:` entry fills in any value that a rule's own entry leaves blank, and is used in full for rules that have no entry of their own. If neither a rule's entry nor `default:` gives a value, the run stops with a "Missing resource ... no default set" error. The one exception is `partition`, which may be left blank when running with `-e slurm`.
    * **mem_mb is in MB** and **time is in minutes**.

!!! tip "Scale resources on retry"

    Any resource except `gpus` and `gres` can be given as a list of per-attempt values instead of a single value. Attempt 1 uses the first value, attempt 2 uses the second, and later attempts reuse the last value. This way, failed jobs can be resubmitted with more memory or time without editing the config between restarts. For example, for the rule `align`, you could scale memory and runtime as follows:

    ```yaml
    rule_resources:
      align:
        mem_mb: [80000, 160000, 200000]
        time: [1660, 3320, 6640, 7200]
    ```

    Retries only happen when you add `--retries N` to the `run` command, for example:

    ```bash
    ./cactus_snakemake run <pipeline> --configfile my-config.yaml -j 20 -e slurm --retries 3
    ```

    `gpus` and `gres` can't be lists. A list there stops the run with an error.
