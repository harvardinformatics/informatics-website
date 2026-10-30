??? question "How can I tell if my genome FASTA files are softmasked? How can I mask them if they aren't already?"

    ##### How can I tell if my genome FASTA files are softmasked?

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

??? question "I got an error related to InsufficientSystemResources regarding GPUs during run_lastz in a blast rule. What do I do?"

    ##### `blast` GPU error

    If the text of the error is somewhat similar to:

    ```bash
    toil.batchSystems.abstractBatchSystem.InsufficientSystemResources: The job 'run_lastz' kind-run_lastz/instance-tqdjs4tj v1 is requesting [{'count': 4, 'kind': 'gpu', 'api': 'cuda', 'brand': 'nvidia'}] accelerators, more than the maximum of [{'kind': 'gpu', 'brand': 'nvidia', 'api': 'cuda', 'count': 1}, {'kind': 'gpu', 'brand': 'nvidia', 'api': 'cuda', 'count': 1}] accelerators that SingleMachineBatchSystem was configured with. The accelerator {'count': 4, 'kind': 'gpu', 'api': 'cuda', 'brand': 'nvidia'} could not be provided. Scale is set to 1.
    ```

    it may be because your GPU partition is set up to use [MIGs (Multi-instance GPUs) :octicons-link-external-24:](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/){:target="_blank"}. This is essentially like a multi-core CPU, except for GPUs. The problem is that Cactus isn't set up to recognize these as of the last update of this tutorial. It only recognizes physical GPU devices. For instance, let's say you've requested 4 GPUs for the blast rules by setting `gpus: 4` (or `gres: 4`) in the `blast` entry of `rule_resources` in your config file. The blast job is submitted to your GPU node, which allocates 2 physical GPUs set up as MIGs, each with 2 instances, which is the equivalent of 4 GPUs. However, Cactus only sees the 2 physical GPUs and thinks there aren't enough to accommodate your request for 4, resulting in the error.

    To resolve this, check your cluster documentation to see if there is a way to use only physical GPUs instead of MIGs. If not, you will have to request a single GPU (`gpus: 1` or `gres: 1`) in the `blast` entry. That is the only way to guarantee that the number of physical GPUs aligns with your request.

    Read more about this [here :octicons-link-external-24:](https://github.com/harvardinformatics/cactus-snakemake/issues/2){:target="_blank"} and [here :octicons-link-external-24:](https://github.com/ComparativeGenomicsToolkit/cactus/issues/1618){:target="_blank"}.
