---
title: Genome annotation
---

<style>
/* FAQ styles */
    details > h5 {
        display: none;
    }
</style>

With the rapid increase in the number of new genomes being assembled, the strigent input data requirements for publicly available resources for automating genome annotation (e.g. Ensembl and NCBI), and inevitable increasing wait times for the production of new annotations by those resources, researchers will be increasingly faced with having to generate annotations for their new genome builds themselves. The two immediate challenges they face are:

1. Deciding which tools are best suited for generating a high-quality annotation, and 
2. Actually running those tools on an HPC cluster.

Here, we provide a brief overview of the three dominant flavors of genome annotation represented by current state-of-the-art tools, provide guidance for picking the right tools, and briefly describe and point to [Snakemake](https://snakemake.readthedocs.io/en/stable/) worfklows that can, with a modest amount of parameter specification, automate the generation of genome annotations in gff/gtf format. If you are unfamiliar with this file format, take a look at [this file format definition](http://useast.ensembl.org/info/website/upload/gff.html) found at *Ensembl*.
