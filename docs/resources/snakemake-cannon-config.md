---
title: "Snakemake Cannon Config"
description: "Information on how to use the config file for automatic partition selection with Snakemake on the Cannon cluster."
authors:
    - Gregg Thomas
author_header: Page maintainer
---

# Snakemake configuration for Cannon partition selection

<div style="text-align:center;">
    <img src="../../img/software-logos/cannon-snakemake-cfg.png" alt="Cannon Snakemake configuration" />
</div>

[Snakemake's :octicons-link-external-24:](https://snakemake.readthedocs.io/en/stable/){:target="_blank"} [SLURM executor plugin :octicons-link-external-24:](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html){:target="_blank"} can perform [automatic partition selection on SLURM clusters :octicons-link-external-24:](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html#automatic-partition-selection){:target="_blank"} if provided with a properly formatted configuration file. We host and maintain a configuration file for Harvard's Cannon cluster here:

```bash
/n/holylfs05/LABS/informatics/Everyone/internal-share/cannon-snakemake-cfg/cannon-snakemake.yml
```

## Usage

To use this configuration file, other resources (`threads`, `mem_mb`, `runtime`) must be defined for your rules, either with a `resources:` definition within the rules or with a [workflow profile :octicons-link-external-24:](https://snakemake.readthedocs.io/en/stable/executing/cli.html#executing-profiles){:target="_blank"} (provided with `--workflow-profile`). The plugin will analyze the requested resources for each rule along with the available resources per partition provided in this config file to determine the most suitable partition for the rule.

When the resources in your Snakemake workflow are setup, provide the path to the partition config file with `--slurm-partition-config` option:

```bash
snakemake ... --slurm-partition-config /n/holylfs05/LABS/informatics/Everyone/internal-share/cannon-snakemake-cfg/cannon-snakemake.yml
```

It may be easiest to store this path as an environment variable, so you can more easily reference it:

```bash
SMK_PART_CFG=/n/holylfs05/LABS/informatics/Everyone/internal-share/cannon-snakemake-cfg/cannon-snakemake.yml
snakemake ... --slurm-partition-config $SMK_PART_CFG
```

To permanently store this environment variable, add it to your `.bashrc` file in your home directory by adding this line of text:

```
export SMK_PART_CFG=/n/holylfs05/LABS/informatics/Everyone/internal-share/cannon-snakemake-cfg/cannon-snakemake.yml
```

Now, the `SMK_PART_CFG` will be loaded automatically everytime you log in. **NOTE:** If you want to see the variable immediately after adding it to `.bashrc`, you will have to either close the terminal and reconnect, or manually reload `.bashrc` with `source ~/.bashrc`.

!!! tip "Confirm the `SMK_PART_CFG` environment variable is loaded"

    You can always confirm that that `SMK_PART_CFG` environment variable is loaded by typing `echo $SMK_PART_CFG`. It should print out the path to the profile. If it displays nothing (or some other data), the config won't work properly with that variable.

## Modifying the configuration file

There may be some instances where one might want to modify the configuration file, for instance to exclude certain partitions from being considered, or for adding lab-specific partitions to the config file.

In both cases, the first step will be to *copy* the configuration file:

```bash
cp /n/holylfs05/LABS/informatics/Everyone/internal-share/cannon-snakemake-cfg/cannon-snakemake.yml cannon-snakemake.cfg
```

This will make a copy of the file in your current directory. You could also rename the file by changing the second file name in the `cp` command, say to `cannon-snakemake-<project>.cfg` or `cannon-snakemake-<lab name>.cfg`, depending on the circumstances.

### Adding lab-specific partitions

After you've made your copy of the config file, you can edit it in any text editor to add a partition. Simply add an entry under `partitions:`:

```yaml
partitions:
  <PARTITION NAME>:
    max_runtime: <INT; MINUTES>
    max_mem_mb: <INT; MEGABYTES>
    max_cpus_per_task: <INT>
    max_nodes: <INT>
    max_threads: <INT; NUMBER OF CPUS ON A GIVEN NODE>
```

Replace <PARTITION NAME> with the real name of your lab's partition.

In most cases, `max_cpus_per_task` can equal `max_threads` and `max_nodes` will be 1.

For the other resources, you likely already have them documented internally. If not, you may be able to get max runtime with:

```bash
scontrol show partition <PARTITION NAME> | grep -o "MaxTime=[^ ]*"
```

and max CPUS and memory with:

```bash
sinfo -p <PARTITION NAME> -N -o "%c %m" | awk 'NR>1 { 
    if ($1 > max_cpus) max_cpus=$1; 
    if ($2 > max_mem)  max_mem=$2 
} END { 
    printf "MaxCPUsPerNode=%d  MaxMemPerNode=%dMB\n", max_cpus, max_mem 
}'
```

Again, replacing <PARTITION NAME> with the real name of your lab's partition.

### Exclude a partition from consideration

To exclude a partition from being considered for submission, simply comment that partition out in your copy of the config file by adding `#` symbols to the beginning of each line referencing that partition. For example, if one wanted to exclude the **shared** partition, they would edit that section in the config to look like this:

```yaml
  # shared:
  #  max_runtime: 4320  # 3 days
  #  max_mem_mb: 184000  # 184 GB
  #  max_cpus_per_task: 48
  #  max_nodes: 1
  #  max_threads: 48
```

---

{{ author_row(page) }}
