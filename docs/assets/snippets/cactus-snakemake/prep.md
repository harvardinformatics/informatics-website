Prep runs on the node you start it from, not as a cluster job. It records what it did in `<output_dir>/prep-manifest.yaml`. Every later run, including each job submitted to the cluster, reads that manifest instead of repeating prep, and stops with an error if:

* prep hasn't been run for the output directory yet. The error gives the command to run.
* the config or input files that prep depended on have changed since (for example the tree in `input_file`, `cactus_path`, or where a new genome goes), or a file prep wrote has been changed. The error lists what changed.

If a change is intended, run prep again with `--force`:

```bash
./cactus_snakemake prep <pipeline> --configfile my-config.yaml --force
```

Files already in the output directory were made from the earlier prep and are not deleted, so for anything that changes the tree, a new output directory is usually the safer choice.
